
from civicboom.model.meta import Base
from civicboom.model.member import Member

from sqlalchemy import Column, ForeignKey
from sqlalchemy import UnicodeText
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import relationship, backref

class Message(Base):
    __tablename__ = "message"
    id          = Column(Integer(),     primary_key=True)
    source_id   = Column(Integer(),     ForeignKey('member.id'), nullable=True)
    target_id   = Column(Integer(),     ForeignKey('member.id'), nullable=True)
    timestamp   = Column(DateTime(),    nullable=False, default="now()")
    text        = Column(UnicodeText(), nullable=False)
    source      = relationship("Member", primaryjoin=source_id==Member.id, backref=backref('messages_from', order_by=id))
    target      = relationship("Member", primaryjoin=target_id==Member.id, backref=backref('messages_to', order_by=id))



