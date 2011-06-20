
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, Integer, PickleType
from sqlalchemy.schema import DDL


class Feed(Base):
    __tablename__ = "feed"
    id            = Column(Integer(),     primary_key=True)
    member_id     = Column(Integer(),     ForeignKey('member.id') , nullable=True, index=True)
    name          = Column(Unicode(),     nullable=False)
    query         = Column(PickleType(),  nullable=False)

DDL("ALTER TABLE feed ADD CHECK (length(name) > 0);").execute_at('after-create', Feed.__table__)
