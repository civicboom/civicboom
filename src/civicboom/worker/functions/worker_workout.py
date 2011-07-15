
from civicboom.model.meta import Session
from civicboom.model import Content
from civicboom.lib.web import url


def worker_workout():
    print "worker_workout():"

    print '*** Session ***'
    print '>>> Session.query(Content).first()'
    print Session.query(Content).first()

    print '*** I18n ***'
    print '>>> _("This is a workout of internationalisation in the worker")'
    print _("This is a workout of internationalisation in the worker")

    print '*** Config ***'
    print '>>> cbutils.worker.config["debug"]'
    import cbutils.worker
    print cbutils.worker.config["debug"]

    print '*** Template ***'
    print '>>> ?'

    print '*** URL Generation ***'
    print '>>> url(controller="misc", action="about", id="civicboom")'
    print url(controller="misc", action="about", id="civicboom")
    print url(host='moo', controller="misc", action="about", id="civicboom")
    print url(protocol='test', host='cake', controller="misc", action="about", id="civicboom")
    print url(protocol='test', controller="misc", action="about", id="civicboom")
    print url(sub_domain='subdom', controller="misc", action="about", id="civicboom")

    return True
