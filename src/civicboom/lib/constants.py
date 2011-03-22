"""
Consistants

(cant put these in app_globals because we can use '_')
"""
from pylons.i18n.translation  import _


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


def get_list_titles(list_name):
    for (list, icon, description) in contents_list_titles:
        if list == list_name:
            return (icon, description)
    return (list_name,list_name)


actions_list = [
    # url identifyer , action, description
    ('/accept'                 , 'accept'     , _('Accept an _assignment')),
    ('/follow'                 , 'follow'     , _('Follow a _member')     ),
    ('/boom'                   , 'boom'       , _('Boom _content')        ),
    ('/contents/new?parent_id=', 'new_respose', _('Create a response')    ),
    #('??'     , 'respond', _('')),
]
