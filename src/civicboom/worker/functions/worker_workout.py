
from civicboom.model.meta import Session
from civicboom.model import Content
from civicboom.lib.web import url

def worker_workout():
    print "worker_workout():"
    print '>>> url(controller="misc", action="about", id="civicboom")'
    print url(controller="misc", action="about", id="civicboom")
    print url(host='moo', controller="misc", action="about", id="civicboom")
    print url(protocol='test', host='cake', controller="misc", action="about", id="civicboom")
    print url(protocol='test', controller="misc", action="about", id="civicboom")
    print url(sub_domain='subdom', controller="misc", action="about", id="civicboom")
    print '>>> Session.query(Content).first()'
    print Session.query(Content).first()
    print '>>> _("This is a workout of i18n in the worker")'
    print _("This is a workout of i18n in the worker")
