"""
A colleciton of utils to convert content between various types.

Beacause there is no standard way to change object types,
we need to do some raw SQL processing to change the database level data and then re-query the object form the database
"""

from civicboom.lib.database.get_cached import get_content
from civicboom.model.content import Content, DraftContent, ArticleContent, AssignmentContent, UserVisibleContent, CommentContent

from civicboom.model.meta import Session


#-------------------------------------------------------------------------------
# Create new object types
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# SQL Commands to manually perform the morphing between content types
#-------------------------------------------------------------------------------

# morph_sql is a dictonary(indexed by strings, values as functions)
# the functions return a list of SQL commands to be executed to perform the morph at the database level

morph_sql = {
    "draft:comment": lambda id: [
            # SQL to remove draft record but leave the main Content object still in tact
            DraftContent.__table__.delete().where(DraftContent.__table__.c.id == id),
            
            # SQL to insert blank comment record
            CommentContent.__table__.insert().values(id=id),
            
            # SQL set object content type content.__type__ = "comment"
            Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="comment"),
        ],

    
    "draft:article": lambda id: [
            # SQL to remove draft record but leave the main Content object still in tact
            DraftContent.__table__.delete().where(DraftContent.__table__.c.id == id),
            
            # SQL to insert blank article record
            UserVisibleContent.__table__.insert().values(id=id),
            ArticleContent.__table__.insert().values(id=id),
            
            # SQL set object content type content.__type__ = "article"
            Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="article"),
        ],
        
    "draft:assignment": lambda id: [
            DraftContent.__table__.delete().where(DraftContent.__table__.c.id == id),
            
            UserVisibleContent.__table__.insert().values(id=id),
            AssignmentContent.__table__.insert().values(id=id),
            
            Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="assignment"),
        ],
        
    "assignment:draft": lambda id: [
            AssignmentContent.__table__.delete().where(AssignmentContent.__table__.c.id == id),
            UserVisibleContent.__table__.delete().where(UserVisibleContent.__table__.c.id == id),
            
            DraftContent.__table__.insert().values(id=id),
            
            Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="draft"),
        ],
        
    "article:draft": lambda id: [
            ArticleContent.__table__.delete().where(ArticleContent.__table__.c.id == id),
            UserVisibleContent.__table__.delete().where(UserVisibleContent.__table__.c.id == id),
            
            DraftContent.__table__.insert().values(id=id),
            
            Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="draft"),
        ],
}




#-------------------------------------------------------------------------------
# Morph to - Morph content between content types
#-------------------------------------------------------------------------------

def morph_content_to(content, after_type):
    """
    params:
        content can be a Content object or a string id
            - as this works at the database level, any content data not commited to the DB before this call will be lost
        after_type is a string of the type the object is being transformed too
        
    return:
        the new mophed object from the database
        
    Notes:
    This is a VERY expensive operation as it requires up to 3 calls to get_content,
    each of these calls is joining potentialy over 3 tables
    """
    
    content = get_content(content)
    if not content:
        raise Exception('no content to morph')
    
    if content.__type__ == None:
        return content # If we don't know the source object type then we cant process it
    if content.__type__ == after_type:
        return content # If the before and after types are the same then return the content obj as no processing needs to take place
    
    if content.id == None: #If the content has not been commited to the DB, then return an object of the correct type
        # todo?
        log.warn('content to morph not in DB? investigate')
        pass
    
    id                = content.id
    sql_generator_key = content.__type__+":"+after_type
    
    if sql_generator_key not in morph_sql:
        raise Exception('unable to morph content from %s to %s' % (content.__type__, after_type) )
    
    Session.expunge(content) # Remove content from SQLAlchemys scope
    for sql_cmd in morph_sql[sql_generator_key](id):
        Session.execute(sql_cmd)
    Session.commit()
    
    #content.invalidate_cache() # Invalidate cache for this content and update etag - AllanC unneeded as this is done automatically with SQLa events
    content = get_content(id)
    assert content.__type__ == after_type # If this is not true then something has gone very wrong!
    return content
