from pylons import config, app_globals
from civicboom.model.meta import Session
from civicboom.model import MemberSetting
from sqlalchemy.orm.exc import NoResultFound
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser
import UserDict
import logging

log = logging.getLogger(__name__)


class MemberSettingsManager(UserDict.DictMixin):
    def __init__(self, member):
        self.member = member

    def __getitem__(self, name):
#        if hasattr(self.member, name):
#            return get(name)
        try:
            q = Session.query(MemberSetting)
            q = q.filter(MemberSetting.member_id==self.member.id)
            q = q.filter(MemberSetting.name==name)
            r = q.one()
            return r.value
        except NoResultFound:
            try:
                user_defaults = SafeConfigParser()
                user_defaults.read("user_defaults.ini")
                return unicode(user_defaults.get("settings", name))
            except NoOptionError:
                raise KeyError(name)

    def get(self, name, default=u''):
#        GregM: DEPRICATED, huge security hole
#        if hasattr(self.member, name):
#            return getattr(self.member, name) or default
        if name in self:
            return self[name]
        else:
            return default

    def __setitem__(self, name, value):
#        GregM: DEPRICATED, huge security hole
#        if hasattr(self.member, name):
#            setattr(self.member,name,value)
#            # remeber this will need to be commited if it's a local property and not a config var
#            return
        if type(value) == type(True):
            if value:
                value = "True"
            else:
                value = "" # blank string evaluates to false
        log.debug("%s:%s = %s" % (self.member.username, name, value))
        try:
            q = Session.query(MemberSetting)
            q = q.filter(MemberSetting.member_id==self.member.id)
            q = q.filter(MemberSetting.name==name)
            r = q.one()
            r.value = unicode(value)
        except NoResultFound:
            ms = MemberSetting()
            ms.member = self.member
            ms.name = name
            ms.value = unicode(value)
            Session.add(ms)
        Session.commit()

    def __delitem__(self, name):
        log.debug(self.member.username+":"+name+" deleted")
        if hasattr(self.member, name):
            setattr(self.member,name,None)
            # remember this will need to be commited
            return
        try:
            q = Session.query(MemberSetting)
            q = q.filter(MemberSetting.member_id==self.member.id)
            q = q.filter(MemberSetting.name==name)
            r = q.one()
            Session.delete(r)
            Session.commit()
        except NoResultFound:
            raise KeyError(name)

    def keys(self):
        q = Session.query(MemberSetting)
        q = q.filter(MemberSetting.member_id==self.member.id)
        r = q.all()
        return [row.name for row in r]
