
from civicboom.model.meta import Session
from civicboom.model import Content
import cbutils.worker as w

def worker_workout():
    print "worker_workout():"
    print '>>> url(controller="misc", action="about", id="civicboom")'
    print w.url(controller="misc", action="about", id="civicboom")
    print '>>> Session.query(Content).first()'
    print Session.query(Content).first()
    print '>>> _("This is a workout of i18n in the worker")'
    print _("This is a workout of i18n in the worker")
