"""
Consistants

(cant put these in app_globals because we can use '_')
"""
from pylons.i18n.translation  import _

import re


def get_list_titles(list_name):
    # in the form list_name, icon, display_text
    contents_list_titles = [
        #list name , icon, description
        ('all'                 , 'article'    , _('all').capitalize()                   ),
        ('drafts'              , 'draft'      , _('drafts').capitalize()                ),
        ('assignments_active'  , 'assignment' , _('active _assignments').capitalize()   ),
        ('assignments_previous', 'assignment' , _('previous _assignments').capitalize() ),
        ('responses'           , 'response'   , _('responses').capitalize()             ),
        ('articles'            , 'article'    , _('_articles').capitalize()             ),
    ]

    for (list, icon, description) in contents_list_titles:
        if list == list_name:
            return (icon, description)
    return (list_name,list_name)

