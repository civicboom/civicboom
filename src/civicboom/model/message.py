
from civicboom.model.meta import Base

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

    def __unicode__(self):
        if len(self.text) > 50:
            return self.text[0:50]+"..."
        else:
            return self.text


