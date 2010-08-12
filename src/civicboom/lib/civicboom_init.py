"""
Additional run once at startup initalizers
"""

def init():

    from civicboom.model.content import Content, AssignmentContent
    
    from sqlalchemy     import and_, or_
    from sqlalchemy.orm import mapper, dynamic_loader, relationship
    
    
    print "init civicboom additonal"
    
    mapper(Content, Content.__table__, non_primary=True, properties={
        'response_test':relationship(Content, primaryjoin=and_(Content.id==Content.parent_id,
                                                                 or_(Content.__type__!='comment',Content.__type__!='draft'))
                                       ),
                                       #sa.and_(t_tipoffs.c.TippedByReporterId==t_reporters.c.id,
                                                                    #t_tipoffs.c.deleted!='Y')),
    })
        
        #responses       = relationship("Content",            backref=backref('parent', remote_side=id, order_by=creation_date)
        #, primaryjoin=and_("Content.id == Content.parent_id") )
                                       #,or_("Content.__type__!='comment'","Content.__type__!='draft'")    # foreign_keys=["Content.id"] 
