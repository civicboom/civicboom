from civicboom.model.meta import Session
from civicboom.model import MemberSetting
from sqlalchemy.orm.exc import NoResultFound
import UserDict

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
            raise KeyError(name)

    def __setitem__(self, name, value):
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


