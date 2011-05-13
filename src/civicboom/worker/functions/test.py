
from civicboom.model.meta import Session
from civicboom.model import Content

def test():
    print "test():"
    print Session.query(Content).first()
    print _("This is a test of i18n in the worker")
