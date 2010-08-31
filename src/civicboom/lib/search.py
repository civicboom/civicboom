#!/usr/bin/env python

def html_base(h):
    return """
<html>
    <head>
        <title>Search Page</title>
        <style>
.and, .or, .not, .fil {
    padding: 16px;
    border: 1px solid black;
}
.and {background: #AFA;}
.or  {background: #AAF;}
.not {background: #FAA;}
.fil {background: #FFF;}
        </style>
    </head>
    <body>"""+h+"""</body>
</html>"""

def html(o):
    if hasattr(o, "__html__"):
        return o.__html__()
    else:
        return str(o)

class Filter(object):
    def __init__(self):
        pass

    def __unicode__(self):
        pass

    def __repr__(self):
        pass

    def __html__(self):
        return "<div class='fil'>" + str(self) + "</div>"


class OrFilter(Filter):
    def __init__(self, subs):
        self.subs = subs

    def __unicode__(self):
        return "or_(\n\t" + ",\n\t".join([unicode(s) for s in self.subs]) + "\n)"

    def __repr__(self):
        return "OrFilter([\n\t" + ",\n\t".join([repr(s) for s in self.subs]) + "\n])"

    def __html__(self):
        return "<div class='or'>any of:<p>" + "<p>or<p>".join([html(s) for s in self.subs]) + "</div>"

class AndFilter(Filter):
    def __init__(self, subs):
        self.subs = subs

    def __unicode__(self):
        return "and_(" + ", ".join([unicode(s) for s in self.subs]) + ")"

    def __repr__(self):
        return "AndFilter([" + ", ".join([repr(s) for s in self.subs]) + "])"

    def __html__(self):
        return "<div class='and'>all of:<p>" + "<p>and<p>".join([html(s) for s in self.subs]) + "</div>"

class NotFilter(Filter):
    def __init__(self, sub):
        self.sub = sub

    def __unicode__(self):
        return "not_(" + unicode(self.sub) + ")"

    def __repr__(self):
        return "NotFilter(" + repr(self.sub) + ")"

    def __html__(self):
        return "<div class='not'>but not:<p>" + html(self.sub) + "</div>"


class TextFilter(Filter):
    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        return "Content.content.matches('"+self.text+"')"

    def __repr__(self):
        return "TextFilter(" + repr(self.text) + ")"

class LocationFilter(Filter):
    def __init__(self, loc, rad=10):
        self.loc = loc
        self.rad = rad

    def __unicode__(self):
        return "Content.location.near('"+self.loc+"', "+str(self.rad)+")"

    def __repr__(self):
        return "LocationFilter(" + repr(self.loc) + ")"

class AuthorFilter(Filter):
    def __init__(self, author):
        self.author = author

    def __unicode__(self):
        return "Content.creator_id = "+self.author

    def __repr__(self):
        return "AuthorFilter(" + repr(self.author) + ")"

class TagFilter(Filter):
    def __init__(self, tag):
        self.tag = tag

    def __unicode__(self):
        return "Content.tags.contains('"+self.tag+"')"

    def __repr__(self):
        return "TagFilter(" + repr(self.tag) + ")"


if __name__ == "__main__":
    query = AndFilter([
        OrFilter([
            TextFilter("terrorists"),
            AndFilter([
                LocationFilter("canterbury"),
                TagFilter("Science & Nature")
            ]),
            AuthorFilter("unittest")
        ]),
        NotFilter(OrFilter([
            TextFilter("waffles"),
            TagFilter("Business")
        ]))
    ])


    import cPickle as pickle
    import zlib

    a = pickle.dumps(query)
    b = pickle.loads(a)

    #print unicode(query)
    print repr(query)
    #print html_base(html(query))

    print "Query  ", len(unicode(query))
    print "ZQuery ", len(zlib.compress(unicode(query)))

    print "Pickle ", len(a)
    print "ZPickle", len(zlib.compress(a))

    print "Repr   ", len(repr(query))
    print "ZRepr  ", len(zlib.compress(repr(query)))

    print "HTML   ", len(html(query))
    print "ZHTML  ", len(zlib.compress(html(query)))

    file("moo.html", "w").write(html_base(html(query)))
