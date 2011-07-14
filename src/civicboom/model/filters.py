#!/usr/bin/env python

"""
A generic-ish library for creating search programs, which can be turned into
SQLAlchemy python fragments, SQL fragments, HTML, or string representations
of themselves

>>> query = AndFilter([
...     OrFilter([
...         TextFilter("terrorists"),
...         AndFilter([
...             LocationFilter([1, 51], 10),
...             TagFilter("Science & Nature")
...         ]),
...         AuthorIDFilter(1)
...     ]),
...     NotFilter(OrFilter([
...         TextFilter("waffles"),
...         TagFilter("Business")
...     ]))
... ])

>>> print unicode(query) # doctest: +NORMALIZE_WHITESPACE
and_(or_(
    Content.content.matches('terrorists'),
    and_(Content.location.near('[1, 51]', 10), Content.tags.contains('Science & Nature')),
    Content.creator_id = 1
), not_(or_(
    Content.content.matches('waffles'),
    Content.tags.contains('Business')
)))

>>> print repr(query) # doctest: +NORMALIZE_WHITESPACE
AndFilter([OrFilter([
    TextFilter('terrorists'),
    AndFilter([LocationFilter([1, 51]), TagFilter('Science & Nature')]),
    AuthorFilter(1)
]), NotFilter(OrFilter([
    TextFilter('waffles'),
    TagFilter('Business')
]))])

>>> print html(query)
<div class='and'>all of:<p><div class='or'>any of:<p><div class='fil'>TextFilter('terrorists')</div><p>or<p><div class='and'>all of:<p><div class='fil'>LocationFilter([1, 51])</div><p>and<p><div class='fil'>TagFilter('Science & Nature')</div></div><p>or<p><div class='fil'>AuthorFilter(1)</div></div><p>and<p><div class='not'>but not:<p><div class='or'>any of:<p><div class='fil'>TextFilter('waffles')</div><p>or<p><div class='fil'>TagFilter('Business')</div></div></div></div>

>>> print sql(query)
((to_tsvector(content.content) @@ to_tsquery('terrorists')) OR ((ST_DWithin(content.location, 'SRID=4326;POINT(1 51)', 10)) AND (content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = 'Science & Nature'))) OR (content.creator_id = 1)) AND (NOT ((to_tsvector(content.content) @@ to_tsquery('waffles')) OR (content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = 'Business'))))


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
        return "(" + (") AND (".join([sql(s) for s in self.subs])) + ")"


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


class TextFilter(Filter):
    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        return "Content.content.matches('%s')" % self.text

    def __repr__(self):
        return "TextFilter(%s)" % repr(self.text)

    def __sql__(self):
        return "to_tsvector(content.content) @@ to_tsquery('%s')" % self.text


class LocationFilter(Filter):
    def __init__(self, loc, rad=10):
        self.loc = loc
        self.rad = rad

    def __unicode__(self):
        return "Content.location.near('%s', %d)" % (self.loc, self.rad)

    def __repr__(self):
        return "LocationFilter(%s)" % repr(self.loc)

    def __sql__(self):
        return "ST_DWithin(content.location, 'SRID=4326;POINT(%f %f)', %f)" % (self.loc[0], self.loc[1], self.rad)


class AuthorIDFilter(Filter):
    def __init__(self, author_id):
        self.author_id = author_id

    def __unicode__(self):
        return "Content.creator_id = %d" % self.author_id

    def __repr__(self):
        return "AuthorFilter(%d)" % self.author_id

    def __sql__(self):
        return "content.creator_id = %d" % self.author_id


class TagFilter(Filter):
    def __init__(self, tag):
        self.tag = tag

    def __unicode__(self):
        return "Content.tags.contains('%s')" % self.tag

    def __repr__(self):
        return "TagFilter(%s)" % repr(self.tag)

    def __sql__(self):
        return "content.id IN (select content_id from map_content_to_tag join tag on tag_id=tag.id where tag.name = '%s')" % self.tag
