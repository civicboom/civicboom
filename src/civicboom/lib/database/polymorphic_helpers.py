"""
A colleciton of utils to convert content between various types.

Beacause there is no standard way to change object types,
we need to do some raw SQL processing to change the database level data and then re-query the object form the database
"""

from civicboom.lib.database.get_cached import get_content, update_content
from civicboom.model.content import Content, DraftContent, ArticleContent, AssignmentContent, UserVisibleContent

from civicboom.model.meta import Session


#inspired by http://old.nabble.com/How-to-get-current-module-object-td15532853.html
def get_this_module_object():
  import sys
  modname = globals()['__name__']
  module = sys.modules[modname]
  return module
this_module = get_this_module_object()


#-------------------------------------------------------------------------------
# Morph to - Morph content between content types
#-------------------------------------------------------------------------------

def morph_content_to(content, after_type, before_type_enforce=None):
    """
    params:
        content can be a Content object or a string id
        after_type is a string of the type the object is being transformed too
        
    return:
        the new mophed object from the database
    """
    
    content = get_content(content)
    if not content: raise Exception('no content to morph')
    
    id = content.id
    
    # If no before type specifyed, lookup the default before_type
    type_conversion_lookup = {"article":"draft"} # "type_to":"enforce_type_from" e.g. "article":"draft" will check that an object IS a draft before it converts it to an article
    if not before_type_enforce:
        if after_type in type_conversion_lookup:
            before_type_enforce = type_conversion_lookup[after_type]
    
    if content.__type__ != before_type_enforce:
        raise Exception('unable to morph content to %s because it is not %s' % (after_type ,before_type_enforce) )
    
    sql_generator = getattr(this_module,'_generate_morph_to_%s_sql' % after_type)
    
    if not sql_generator:
        raise Exception('Unable to find SQL generator to morph from %s to %s' % (after_type ,before_type_enforce) )
    
    for sql_cmd in sql_generator(id):
        Session.execute(sql_cmd)
    Session.commit()
    
    update_content(id) # Invalidate cache for this content and update etag
    return get_content(id)

    
#-------------------------------------------------------------------------------
# SQL Commands to manually perform the morphing between content types
#-------------------------------------------------------------------------------

def _generate_morph_to_article_sql(id):
    return [
        # SQL to remove draft record but leave the main Content object still in tact
        DraftContent.__table__.delete().where(DraftContent.__table__.c.id == id),
        
        # SQL to insert blank article record
        UserVisibleContent.__table__.insert().values(id=id),
        ArticleContent.__table__.insert().values(id=id),
        
        # SQL set object content type content.__type__ = "article"
        Content.__table__.update().where(Content.__table__.c.id==id).values(__type__="article"),
    ]
