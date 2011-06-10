"""
Consistants

(cant put these in app_globals because we can use '_')
"""
from pylons.i18n.translation  import _

import re

# in the form list_name, icon, display_text
contents_list_titles = [
    #list name , icon, description
    ('all'                 , 'article'    , _('all').capitalize()                   ),
    ('drafts'              , 'draft'      , _("What I'm working on")                ),
    ('assignments_active'  , 'assignment' , _("What I've asked")                    ),
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
    (re.compile('/accept'                                   ) , 'accept'     , _('Accept a _assignment')),
    (re.compile('/follow'                                   ) , 'follow'     , _('Follow a _member')     ),
    (re.compile('/boom'                                     ) , 'boom'       , _('Boom _content')        ),
    (re.compile('/contents/new\?parent_id='                 ) , 'new_respose', _('Create a response')    ),
    (re.compile('/contents?(.*?)type=comment(.*?)parent_id=') , 'comment'    , _('make a comment')       ), #AllanC - I weep at the inefficency and code duplication
    (re.compile('/contents?(.*?)parent_id=(.*?)type=comment') , 'comment'    , _('make a comment')       ),

#/contents/new?parent_id=26&type=comment

]
