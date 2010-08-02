from pylons import config, app_globals
from civicboom.model.meta import Session
from civicboom.model import MemberSetting
from sqlalchemy.orm.exc import NoResultFound
import UserDict
import logging

log = logging.getLogger(__name__)

class MemberSettingsManager(UserDict.DictMixin):
    def __init__(self, member):
        self.member = member

    def __getitem__(self, name):
        try:
            q = Session.query(MemberSetting)
            q = q.filter(MemberSetting.member_id==self.member.id)
            q = q.filter(MemberSetting.name==name)
            r = q.one()
            return r.value
        except NoResultFound:
            return unicode(app_globals.user_defaults.get("settings", name))

    def __setitem__(self, name, value):
        if type(value) == type(True):
            if value:
                value = "True"
            else:
                value = "" # blank string evaluates to false
        log.debug(self.member.username+":"+name+" = "+str(value))
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


