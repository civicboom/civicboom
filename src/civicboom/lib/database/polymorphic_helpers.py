"""
A colleciton of utils to convert content between various types.

Beacause there is no standard way to change object types,
we need to do some raw SQL processing to change the database level data and then re-query the object form the database
"""

from civicboom.lib.database.get_cached import get_content, update_content
from civicboom.model.content import Content, DraftContent, ArticleContent, AssignmentContent, UserVisibleContent

from civicboom.model.meta import Session


def morph_to_draft(content):
    """
    Downgrade content from a published article back to a basic draft
    """
    pass

def morph_to_article(content):
    """
    Publish an Article
    by
     - removing the draft record
     - inserting a new blank article record with the same id as the draft
     - get new modifyed object from database
    """
    content = get_content(content)
    if not content or content.__type__ != "draft": raise Exception('unable to morph content that is not a draft')
    
    id = content.id
    
    sql_cmds = [
        # SQL to remove draft record but leave the main Content object still in tact
        DraftContent.__table__.delete().where(DraftContent.__table__.c.id == id),
        
        # SQL to insert blank article record
        UserVisibleContent.__table__.insert().values(id=id),
        ArticleContent.__table__.insert().values(id=id),
    
        # SQL set object content type content.__type__ = "article"
        Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="article"),
    ]
    
    for sql_cmd in sql_cmds:
        Session.execute(sql_cmd)
    Session.commit()
    
    # SQL set type content.__type__ = "article"
    #conn.execute(users.delete().where(users.c.name > 'm'))
    update_content(id)
    return get_content(id)


def morph_to_assignment(content):
    """
    Publish and Assignment
    """
    pass