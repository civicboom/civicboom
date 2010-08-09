"""
A colleciton of utils to convert content between various types.

Beacause there is no standard way to change object types,
we need to do some raw SQL processing to change the database level data and then re-query the object form the database
"""

from civicboom.lib.database.get_cached import get_content

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
    if not content or content.__type__ != "draft": return  # Abort if content retrived is not a draft
    # SQL to remove draft record
    # SQL to insert blank article record
    update_content(content)
    return get_content(content)


def morph_to_assignment(content):
    """
    Publish and Assignment
    """
    pass