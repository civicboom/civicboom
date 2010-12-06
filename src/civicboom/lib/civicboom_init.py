"""
Additional run once at startup initalizers
"""

def init():
    """
    The model uses the string based arguments (because the class may not have been defined yet)
    I'm unsure as to wether the problem was with the version of SQLAlchemy but with the string method it was not possible to specify multiple conditions under the primary join param even though the SQL created was correct
    In the future it may be possible to intigrate these with the main class defentions
    """
    from civicboom.model.content import Content, AssignmentContent, MemberAssignment, Interest
    from civicboom.model.member  import Member
    
    from sqlalchemy     import and_, or_, not_
    from sqlalchemy.orm import mapper, dynamic_loader, relationship

    import datetime
    
    
    # Replaced with contents/index search
    """    
    Content.responses = relationship(Content,
                                     primaryjoin=and_(Content.id==Content.parent_id,
                                                        not_(or_(Content.__type__=='comment',Content.__type__=='draft'))
                                                    ) ,
                                    order_by = Content.id.desc()
                                    )

    Member.content        = relationship(Content, primaryjoin=and_(Member.id==Content.creator_id, Content.__type__!='comment'))
    
    Member.content_public = relationship(Content, primaryjoin=and_(Member.id==Content.creator_id, Content.__type__!='comment', Content.visible==True, Content.private==False)) #Content.__type__!='draft',
    #Member.groups_public  = relationship(Group,   primaryjoin=and_() #AllanC - nice idea, but we need the roles .. maybe a roles public? with the group eagerloaded?
    
    Member.content_assignments_active   = relationship(AssignmentContent, primaryjoin=and_(Member.id==AssignmentContent.creator_id, AssignmentContent.due_date>=datetime.datetime.now()))    
    Member.content_assignments_previous = relationship(AssignmentContent, primaryjoin=and_(Member.id==AssignmentContent.creator_id, AssignmentContent.due_date< datetime.datetime.now()))

    """
    
    period_in_days = 30
    
    Member.active_assignments_period  = relationship(AssignmentContent, primaryjoin=and_(AssignmentContent.creator_id == Member.id, AssignmentContent.creation_date > (datetime.datetime.now() - datetime.timedelta(days=period_in_days))), order_by=AssignmentContent.update_date.desc())
    
    Member.interest = dynamic_loader(Content,
                                        primaryjoin=Member.id==Interest.member_id,
                                        secondary=Interest.__table__,
                                        secondaryjoin=Interest.content_id==Content.id,
                                        foreign_keys=[Interest.member_id,Interest.content_id],
                                        backref='interested_members',
                                    )
    
    AssignmentContent.accepted_by = dynamic_loader(Member,
                                                primaryjoin=and_(AssignmentContent.id==MemberAssignment.content_id,
                                                                 MemberAssignment.status=="accepted",
                                                ),
                                                secondary=MemberAssignment.__table__,
                                                secondaryjoin=MemberAssignment.member_id==Member.id,
                                                foreign_keys=[MemberAssignment.content_id,MemberAssignment.member_id],
                                                backref='assignments_accepted'
                                    )