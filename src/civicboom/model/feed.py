
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import UnicodeText, Integer, PickleType

class Feed(Base):
    __tablename__ = "feeds"
    id            = Column(Integer(),     primary_key=True)
    member_id     = Column(Integer(),     ForeignKey('member.id') , nullable=True )
    query         = Column(PickleType(),  nullable=False)
    comment       = Column(UnicodeText(), nullable=True, doc="optional should the user want to add additional details")
