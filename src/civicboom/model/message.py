
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import Integer, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

import copy

class Message(Base):
    __tablename__ = "message"
    id          = Column(Integer(),     primary_key=True)
    source_id   = Column(Integer(),     ForeignKey('member.id'), nullable=True)
    target_id   = Column(Integer(),     ForeignKey('member.id'), nullable=True)
    timestamp   = Column(DateTime(),    nullable=False, default=func.now())
    subject     = Column(Unicode(),     nullable=False)
    content     = Column(UnicodeText(), nullable=False)

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'list': {
            'id'           : None ,
            'source_id'    : None ,
            'target_id'    : None ,
            'timestamp'    : None ,
            'subject'      : None ,
            'content'      : None ,
        },
    })
    __to_dict__.update({
        'single': copy.deepcopy(__to_dict__['list'])
    })