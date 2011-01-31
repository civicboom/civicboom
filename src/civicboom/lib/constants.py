"""
Consistants

(cant put these in app_globals because we can use '_')
"""
from pylons.i18n.translation  import _


# in the form list_name, icon, display_text
contents_list_titles = [
    #list name , icon, description
    ('drafts'              , 'draft'      , _('Drafts')                ),
    ('assignments_active'  , 'assignment' , _('Active _assignments')   ),
    ('assignments_previous', 'assignment' , _('Previous _assignments') ),
    ('responses'           , 'response'   , _('Responses')             ),
    ('articles'            , 'article'    , _('_articles')             ),
]

def get_list_titles(list_name):
    for (list, icon, description) in contents_list_titles:
        if list == list_name:
            return (icon, description)
    return (list_name,list_name)

actions_list = [
    # url identifyer , description
    ('/accept', _('Accept an _assignment')),
]