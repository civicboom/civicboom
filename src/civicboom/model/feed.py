
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, Integer, PickleType

class Feed(Base):
    __tablename__ = "feeds"
    id            = Column(Integer(),     primary_key=True)
    member_id     = Column(Integer(),     ForeignKey('member.id') , nullable=True, index=True)
    name          = Column(Unicode(),     nullable=False)
    query         = Column(PickleType(),  nullable=False)
