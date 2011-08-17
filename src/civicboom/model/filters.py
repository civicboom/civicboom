#!/usr/bin/env python

"""
A generic-ish library for creating search programs, which can be turned into
SQLAlchemy python fragments, SQL fragments, HTML, or string representations
of themselves

>>> query = AndFilter([
...     OrFilter([
...         TextFilter("terrorists"),
...         AndFilter([
...             LocationFilter(1, 51, 10),
...             TagFilter("Science & Nature")
...         ]),
...         CreatorFilter("unittest")
...     ]),
...     NotFilter(OrFilter([
...         TextFilter("waffles"),
...         TagFilter("Business")
...     ]))
... ])

>>> print unicode(query) # doctest: +NORMALIZE_WHITESPACE
and_(or_(
    Content.content.matches('terrorists'),
    and_(Content.location.near((1.000000, 51.000000), 10.000000), Content.tags.contains('Science & Nature')),
    Content.creator_id = 'unittest'
), not_(or_(
    Content.content.matches('waffles'),
    Content.tags.contains('Business')
)))

>>> print repr(query) # doctest: +NORMALIZE_WHITESPACE
AndFilter([OrFilter([
    TextFilter('terrorists'),
    AndFilter([LocationFilter(1.000000, 51.000000, 10.000000), TagFilter('Science & Nature')]),
    CreatorFilter('unittest')
]), NotFilter(OrFilter([
    TextFilter('waffles'),
    TagFilter('Business')
]))])

>>> print html(query)
<div class='and'>all of:<p><div class='or'>any of:<p><div class='fil'>TextFilter('terrorists')</div><p>or<p><div class='and'>all of:<p><div class='fil'>LocationFilter(1.000000, 51.000000, 10.000000)</div><p>and<p><div class='fil'>TagFilter('Science & Nature')</div></div><p>or<p><div class='fil'>CreatorFilter('unittest')</div></div><p>and<p><div class='not'>but not:<p><div class='or'>any of:<p><div class='fil'>TextFilter('waffles')</div><p>or<p><div class='fil'>TagFilter('Business')</div></div></div></div>

>>> print sql(query)
((to_tsvector('english', title || ' ' || content) @@ to_tsquery('terrorists')) OR ((ST_DWithin(content.location, 'SRID=4326;POINT(1.000000 51.000000)', 10.000000)) AND (content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = 'Science & Nature'))) OR (content.creator_id = 'unittest')) AND (NOT ((to_tsvector('english', title || ' ' || content) @@ to_tsquery('waffles')) OR (content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = 'Business'))))


LabelFilter is a thing to put text into the human-readable output while having
no effect on the query:

>>> q = LabelFilter("waffo")
>>> print unicode(q)
(1=1)
>>> print repr(q)
LabelFilter('waffo')
>>> print html(q)
<div class='label'>waffo</div>
>>> print sql(q)
(1=1)


All classes are children of the stub Filter class:

>>> q = Filter()
>>> print unicode(q)
(1=1)
>>> print repr(q)
Filter()
>>> print html(q)
<div class='fil'>Filter()</div>
>>> print sql(q)
(1=1)
"""

from civicboom.lib.database.get_cached import get_content, get_member
from civicboom.model import Content
from civicboom.model.meta import location_to_string
from cbutils.misc import make_username, debug_type
from pylons import tmpl_context as c
import re
from dateutil.parser import parse
from datetime import datetime
from sqlalchemy import func, Unicode


__all__ = [
    "html", "sql",
    "FilterException",
    "Filter", "LabelFilter",
    "OrFilter", "AndFilter", "NotFilter",
    "IDFilter",
    "TextFilter",
    "LocationFilter",
    "TypeFilter",
    "DueDateFilter", "UpdateDateFilter",
    "ParentIDFilter",
    "CreatorFilter",
    "BoomedByFilter",
    "TagFilter",
]


##############################################################################
# meta bits
##############################################################################

def html(o):
    return o.__html__()


def sql(o):
    return o.__sql__()


class FilterException(Exception):
    pass


class Filter(object):

    def __unicode__(self):
        return "(1=1)"

    def __repr__(self):
        return "Filter()"

    def __html__(self):
        return "<div class='fil'>%s</div>" % self

    def __sql__(self):
        return "(1=1)"


class LabelFilter(Filter):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "LabelFilter(%s)" % repr(self.label)

    def __html__(self):
        return "<div class='label'>%s</div>" % self.label


##############################################################################
# logical operators
##############################################################################

class OrFilter(Filter):
    def __init__(self, subs):
        self.subs = subs

    def __unicode__(self):
        return "or_(\n\t" + ",\n\t".join([unicode(s) for s in self.subs]) + "\n)"

    def __repr__(self):
        return "OrFilter([\n\t" + ",\n\t".join([repr(s) for s in self.subs]) + "\n])"

    def __html__(self):
        return "<div class='or'>any of:<p>" + "<p>or<p>".join([html(s) for s in self.subs]) + "</div>"

    def __sql__(self):
        if len(self.subs) == 1:
            return sql(self.subs[0])
        elif len(self.subs) > 1:
            return "(" + (") OR (".join([sql(s) for s in self.subs])) + ")"
        else:
            return "(1=1)"


class AndFilter(Filter):
    def __init__(self, subs):
        self.subs = subs

    def __unicode__(self):
        return "and_(" + ", ".join([unicode(s) for s in self.subs]) + ")"

    def __repr__(self):
        return "AndFilter([" + ", ".join([repr(s) for s in self.subs]) + "])"

    def __html__(self):
        return "<div class='and'>all of:<p>" + "<p>and<p>".join([html(s) for s in self.subs]) + "</div>"

    def __sql__(self):
        if len(self.subs) == 1:
            return sql(self.subs[0])
        elif len(self.subs) > 1:
            return "(" + (") AND (".join([sql(s) for s in self.subs])) + ")"
        else:
            return "(1=1)"


class NotFilter(Filter):
    def __init__(self, sub):
        # FIXME: assert
        self.sub = sub

    def __unicode__(self):
        return "not_(" + unicode(self.sub) + ")"

    def __repr__(self):
        return "NotFilter(" + repr(self.sub) + ")"

    def __html__(self):
        return "<div class='not'>but not:<p>" + html(self.sub) + "</div>"

    def __sql__(self):
        return "NOT ("+sql(self.sub)+")"


##############################################################################
# content filters
##############################################################################

class IDFilter(Filter):
    def __init__(self, id_list):
        assert all([type(n) == int for n in id_list])
        self.id_list = ", ".join(["%d" % d for d in id_list])

    def __unicode__(self):
        return "Content.id in [%s]" % self.id_list

    def __repr__(self):
        return "IDFilter(%s)" % self.id_list

    def __sql__(self):
        return "content.id IN (%s)" % self.id_list


class TextFilter(Filter):
    def __init__(self, text):
        # FIXME: assert?
        self.text = text

    @staticmethod
    def from_string(s):
        parts = []
        for word in s.split():
            word = re.sub("[^a-zA-Z0-9_-]", "", word)
            if word:
                parts.append(word)

        if parts:
            return TextFilter(" | ".join(parts))

        raise FilterException("Invalid text search: %s" % s)

    def mangle(self, results):
        return results.add_columns(
            func.ts_headline('pg_catalog.english',
                func.strip_tags(Content.content),
                func.plainto_tsquery(self.text),
                'MaxFragments=3, FragmentDelimiter=" ... ", StartSel="<b>", StopSel="</b>", MinWords=7, MaxWords=15',
                type_= Unicode
            ).label("content_short")
        )

    def __unicode__(self):
        return "Content.content.matches(%s)" % repr(self.text)

    def __repr__(self):
        return "TextFilter(%s)" % repr(self.text)

    def __sql__(self):
        return "to_tsvector('english', title || ' ' || content) @@ to_tsquery('%s')" % self.text


class LocationFilter(Filter):
    def __init__(self, lon, lat, rad=10):
        self.lon = float(lon)
        self.lat = float(lat)
        self.rad = float(rad)

    @staticmethod
    def from_string(s):
        (lon, lat, radius) = (None, None, 10)

        if s == "me":
            if c.logged_in_user and c.logged_in_user.location:
                (lon, lat) = location_to_string(c.logged_in_user.location).split()
            else:
                raise FilterException("location=me when user has no location")

        zoom = 10 # FIXME: inverse of radius? see bug #50

        location = s.replace(",", " ")
        location_tuple = [float(i.strip()) for i in location.split()]
        if   len(location_tuple) == 2:
            (lon, lat        ) = location_tuple
        elif len(location_tuple) == 3:
            (lon, lat, radius) = location_tuple

        if lon and lat and radius:
            return LocationFilter(lon, lat, radius)

        raise FilterException("Invalid location '%s'" % s)

    def mangle(self, results):
        return results.add_columns(
            func.st_distance_sphere(
                func.st_geomfromwkb(Content.location, 4326),
                'SRID=4326;POINT(%f %f)' % (self.lon, self.lat)
            ).label("distance")
        )

    def __unicode__(self):
        return "Content.location.near((%f, %f), %f)" % (self.lon, self.lat, self.rad)

    def __repr__(self):
        return "LocationFilter(%f, %f, %f)" % (self.lon, self.lat, self.rad)

    def __sql__(self):
        return "ST_DWithin(content.location, 'SRID=4326;POINT(%f %f)', %f)" % (self.lon, self.lat, self.rad)


class TypeFilter(Filter):
    def __init__(self, type):
        assert type in ['article', 'assignment', 'draft'], debug_type(type)
        self.type = type

    @staticmethod
    def from_string(s):
        return TypeFilter(s)

    def __unicode__(self):
        return "Content.__type__ = '%s'" % self.type

    def __repr__(self):
        return "TypeFilter(%s)" % repr(self.type)

    def __sql__(self):
        return "content.__type__ = '%s'" % self.type


class DueDateFilter(Filter):
    def __init__(self, comparitor, date):
        assert comparitor in ["<", ">", "IS"], debug_type(comparitor)
        # FIXME: validate date
        self.comparitor = comparitor
        self.date = date

    @staticmethod
    def from_string(s):
        c = '='
        d = s
        if s[0] in ['<', '>']:
            c = s[0]
            d = s[1:]
        if d == "now":
            pd = datetime.now()
        else:
            pd = parse(d, dayfirst=True)
        return DueDateFilter(c, pd)

    def __unicode__(self):
        return "AssignmentContent.due_date %s '%s'" % (self.comparitor, self.date)

    def __repr__(self):
        return "DueDateFilter(%s, %s)" % (repr(self.comparitor), repr(self.date))

    def __sql__(self):
        if type(self.date) == str:
            return "content_assignment.due_date %s %s" % (self.comparitor, self.date)
        else:
            return "content_assignment.due_date %s '%s'" % (self.comparitor, self.date)



class UpdateDateFilter(Filter):
    def __init__(self, comparitor, date):
        assert comparitor in ["<", ">", "IS"], debug_type(comparitor)
        # FIXME: validate date
        self.comparitor = comparitor
        self.date = date

    @staticmethod
    def from_string(s):
        c = '='
        d = s
        if s[0] in ['<', '>']:
            c = s[0]
            d = s[1:]
        if d == "now":
            pd = datetime.now()
        else:
            pd = parse(d, dayfirst=True)
        return UpdateDateFilter(c, pd)

    def __unicode__(self):
        return "Content.update_date %s '%s'" % (self.comparitor, self.date)

    def __repr__(self):
        return "UpdateDateFilter(%s, %s)" % (repr(self.comparitor), repr(self.date))

    def __sql__(self):
        if type(self.date) == str:
            return "content.update_date %s %s" % (self.comparitor, self.date)
        else:
            return "content.update_date %s '%s'" % (self.comparitor, self.date)


class ParentIDFilter(Filter):
    def __init__(self, parent_id):
        assert type(parent_id) in [int, bool], debug_type(parent_id)
        self.parent_id = parent_id

    @staticmethod
    def from_string(s):
        if s.isdigit():
            return ParentIDFilter(int(s))

        raise FilterException("Content not found: %s" % s)

    def __unicode__(self):
        return "Content.parent_id = %d" % self.parent_id

    def __repr__(self):
        return "ParentIDFilter(%d)" % self.parent_id

    def __sql__(self):
        if self.parent_id == False:
            return "content.parent_id IS NULL"
        elif self.parent_id == True:
            return "content.parent_id IS NOT NULL"
        else:
            return "content.parent_id = %d" % self.parent_id


class CreatorFilter(Filter):
    def __init__(self, creator_id):
        assert type(creator_id) in [str, unicode], debug_type(creator_id)
        self.creator_id = make_username(creator_id)

    @staticmethod
    def from_string(s):
        if s == "me":
            m = c.logged_in_persona
        else:
            m = get_member(s)
        if m:
            return CreatorFilter(m.id)

        raise FilterException("Member not found: %s" % s)

    def __unicode__(self):
        return "Content.creator_id = '%s'" % self.creator_id

    def __repr__(self):
        return "CreatorFilter(%s)" % repr(self.creator_id)

    def __sql__(self):
        return "content.creator_id = '%s'" % self.creator_id


class BoomedByFilter(Filter):
    def __init__(self, boomer_id):
        assert type(boomer_id) in [str, unicode], debug_type(boomer_id)
        self.boomer_id = make_username(boomer_id)

    @staticmethod
    def from_string(s):
        m = get_member(s)
        if m:
            return BoomedByFilter(m.id)

        raise FilterException("Member not found: %s" % s)

    def __unicode__(self):
        return "FIXME" # Content.id in '%s'" % self.boomer_id

    def __repr__(self):
        return "BoomedByFilter(%s)" % repr(self.boomer_id)

    def __sql__(self):
        return "content.id IN (SELECT content_id FROM map_booms WHERE member_id='%s')" % self.boomer_id


class TagFilter(Filter):
    def __init__(self, tag):
        # FIXME: assert validity
        self.tag = tag

    @staticmethod
    def from_string(s):
        # FIXME: validate as a-z0-9
        return TagFilter(s)

    def __unicode__(self):
        return "Content.tags.contains(%s)" % repr(self.tag)

    def __repr__(self):
        return "TagFilter(%s)" % repr(self.tag)

    def __sql__(self):
        return "content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = '%s')" % self.tag
