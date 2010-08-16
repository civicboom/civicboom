"""
Additional run once at startup initalizers
"""

def init():

    from civicboom.model.content import Content, AssignmentContent
    
    from sqlalchemy     import and_, or_, not_
    from sqlalchemy.orm import mapper, dynamic_loader, relationship
    
    Content.responses = relationship(Content, primaryjoin=and_(Content.id==Content.parent_id,
                                                                not_(or_(Content.__type__=='comment',Content.__type__=='draft'))
                                                                )
                                       )