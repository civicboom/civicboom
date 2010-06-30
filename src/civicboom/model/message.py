
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import UnicodeText
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import relationship

class Message(Base):
    __tablename__ = "message"

    id          = Column(Integer(), primary_key=True)
    source_id   = Column(Integer(), ForeignKey('member.id'), nullable=True)
    target_id   = Column(Integer(), ForeignKey('member.id'), nullable=True)
    timestamp   = Column(DateTime())
    text        = Column(UnicodeText())

    source      = relationship("Member", primaryjoin="source_id==Member.id")
    target      = relationship("Member", primaryjoin="target_id==Member.id")



