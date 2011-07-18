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
...         CreatorIDFilter(1)
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
    Content.creator_id = 1
), not_(or_(
    Content.content.matches('waffles'),
    Content.tags.contains('Business')
)))

>>> print repr(query) # doctest: +NORMALIZE_WHITESPACE
AndFilter([OrFilter([
    TextFilter('terrorists'),
    AndFilter([LocationFilter(1.000000, 51.000000, 10.000000), TagFilter('Science & Nature')]),
    CreatorIDFilter(1)
]), NotFilter(OrFilter([
    TextFilter('waffles'),
    TagFilter('Business')
]))])

>>> print html(query)
<div class='and'>all of:<p><div class='or'>any of:<p><div class='fil'>TextFilter('terrorists')</div><p>or<p><div class='and'>all of:<p><div class='fil'>LocationFilter(1.000000, 51.000000, 10.000000)</div><p>and<p><div class='fil'>TagFilter('Science & Nature')</div></div><p>or<p><div class='fil'>CreatorIDFilter(1)</div></div><p>and<p><div class='not'>but not:<p><div class='or'>any of:<p><div class='fil'>TextFilter('waffles')</div><p>or<p><div class='fil'>TagFilter('Business')</div></div></div></div>

>>> print sql(query)
((to_tsvector('english', title || ' ' || content) @@ to_tsquery('terrorists')) OR ((ST_DWithin(content.location, 'SRID=4326;POINT(1.000000 51.000000)', 10.000000)) AND (content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = 'Science & Nature'))) OR (content.creator_id = 1)) AND (NOT ((to_tsvector('english', title || ' ' || content) @@ to_tsquery('waffles')) OR (content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = 'Business'))))


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


##############################################################################
# meta bits
##############################################################################

def html(o):
    return o.__html__()


def sql(o):
    return o.__sql__()


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
        return "(" + (") OR (".join([sql(s) for s in self.subs])) + ")"


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
        if self.subs:
            return "(" + (") AND (".join([sql(s) for s in self.subs])) + ")"
        else:
            return "(1=1)"


class NotFilter(Filter):
    def __init__(self, sub):
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
        self.id_list = ", ".join(["%d" % d for d in id_list])

    def __unicode__(self):
        return "Content.id_list in [%s]" % self.id_list

    def __repr__(self):
        return "ParentIDFilter(%s)" % self.id_list

    def __sql__(self):
        return "content.id IN (%s)" % self.id_list


class TextFilter(Filter):
    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        return "Content.content.matches('%s')" % self.text

    def __repr__(self):
        return "TextFilter(%s)" % repr(self.text)

    def __sql__(self):
        import re

        parts = []
        for word in self.text.split():
            word = re.sub("[^a-zA-Z0-9_-]", "", word)
            if word:
                parts.append(word)

        if parts:
            text = " | ".join(parts)
            return "to_tsvector('english', title || ' ' || content) @@ to_tsquery('%s')" % text
        else:
            return query


class LocationFilter(Filter):
    def __init__(self, lon, lat, rad=10):
        self.lon = float(lon)
        self.lat = float(lat)
        self.rad = float(rad)

    @staticmethod
    def from_string(s):
        if s == "me":
            return LabelFilter("location=me not supported yet") # FIXME

        (lon, lat, radius) = (None, None, 10)
        zoom = 10 # FIXME: inverse of radius? see bug #50

        location = s.replace(",", " ")
        location_tuple = [float(i.strip()) for i in location.split()]
        if   len(location_tuple) == 2:
            (lon, lat        ) = location_tuple
        elif len(location_tuple) == 3:
            (lon, lat, radius) = location_tuple

        if lon and lat and radius:
            return LocationFilter((lon, lat), radius)

    def __unicode__(self):
        return "Content.location.near((%f, %f), %f)" % (self.lon, self.lat, self.rad)

    def __repr__(self):
        return "LocationFilter(%f, %f, %f)" % (self.lon, self.lat, self.rad)

    def __sql__(self):
        return "ST_DWithin(content.location, 'SRID=4326;POINT(%f %f)', %f)" % (self.lon, self.lat, self.rad)


class TypeFilter(Filter):
    def __init__(self, type):
        if type in ['article', 'assignment', 'draft']:
            self.type = type

    def __unicode__(self):
        return "Content.__type__ = '%s'" % self.type

    def __repr__(self):
        return "TypeFilter(%s)" % repr(self.type)

    def __sql__(self):
        return "content.__type__ = '%s'" % self.type


class ParentIDFilter(Filter):
    def __init__(self, parent_id):
        self.parent_id = parent_id

    def __unicode__(self):
        return "Content.parent_id = %d" % self.parent_id

    def __repr__(self):
        return "ParentIDFilter(%d)" % self.parent_id

    def __sql__(self):
        return "content.parent_id = %d" % self.parent_id


class CreatorIDFilter(Filter):
    def __init__(self, creator_id):
        self.creator_id = creator_id

    def __unicode__(self):
        return "Content.creator_id = %d" % self.creator_id

    def __repr__(self):
        return "CreatorIDFilter(%d)" % self.creator_id

    def __sql__(self):
        return "content.creator_id = %d" % self.creator_id


class CreatorFilter(Filter):
    def __init__(self, creator_name):
        self.creator_name = creator_name

    def __unicode__(self):
        return "Content.creator_name = '%s'" % self.creator_name

    def __repr__(self):
        return "CreatorFilter(%s)" % repr(self.creator_name)

    def __sql__(self):
        return "content.creator_id = (SELECT id FROM member WHERE username='%s')" % self.creator_name


class BoomedByFilter(Filter):
    def __init__(self, boomer_id):
        self.boomer_id = boomer_id

    def __unicode__(self):
        return "FIXME" # Content.id in '%s'" % self.boomer_id

    def __repr__(self):
        return "BoomedByFilter(%d)" % repr(self.boomer_id)

    def __sql__(self):
        return "content.id IN (SELECT content_id FROM map_booms WHERE member_id=%d)" % self.boomer_id


class TagFilter(Filter):
    def __init__(self, tag):
        self.tag = tag

    def __unicode__(self):
        return "Content.tags.contains('%s')" % self.tag

    def __repr__(self):
        return "TagFilter(%s)" % repr(self.tag)

    def __sql__(self):
        return "content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = '%s')" % self.tag
