
from civicboom.model.meta import Session
from civicboom.model import Content

def worker_workout():
    print "worker_workout():"
    print Session.query(Content).first()
    print _("This is a workout of i18n in the worker")
