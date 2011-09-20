
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Unicode, Integer, PickleType
from sqlalchemy.schema import CheckConstraint


class Feed(Base):
    __tablename__ = "feed"
    id            = Column(Integer(),     primary_key=True)
    member_id     = Column(String(32),    ForeignKey('member.id', onupdate="cascade") , nullable=True, index=True)
    name          = Column(Unicode(),     nullable=False)
    query         = Column(PickleType(),  nullable=False)

    __table_args__ = (
        CheckConstraint("length(name) > 0"),
        {}
    )
