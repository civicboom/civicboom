from civicboom.model.meta import Base

from cbutils.misc import now, debug_type

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String, Enum, Integer, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, backref


class FlaggedEntity(Base):
    __tablename__ = "flagged_content"
    _flag_type = Enum("offensive", "spam", "copyright", "automated", "other", name="flag_type")
    id            = Column(Integer(),     primary_key=True)
    raising_member_id = Column(String(32),    ForeignKey('member.id', onupdate="cascade") , nullable=True )
    timestamp     = Column(DateTime(),    nullable=False, default=now)
    type          = Column(_flag_type,    nullable=False)
    comment       = Column(UnicodeText(), nullable=False, default="", doc="optional should the user want to add additional details")

    offending_content_id = Column(Integer() , ForeignKey('content.id')                   , nullable=True, index=True)
    offending_member_id  = Column(String(32), ForeignKey('member.id', onupdate="cascade"), nullable=True )
    offending_message_id = Column(Integer() , ForeignKey('message.id')                   , nullable=True )

    # AllanC - Shish disabled this because the SQLA was having difficulty dertermining which member relationship to use
    #          We need to specify the relationship mapping manually ... I can get to this at some point
    #          Raised issue #829
    # member:flag is already defined
    #raising_member       = relationship("Member", primaryjoin="FlaggedEntity.raising_member_id==Member.id", backref=backref('flags_raised', cascade="all, delete-orphan"))

    def __str__(self):
        #return "%s - %s (%s)" % (self.raising_member.username if self.raising_member else "System", self.comment, self.type)
        return "%s - %s (%s)" % (self.raising_member_id if self.raising_member_id else "System", self.comment, self.type)

