"""
Consistants

(cant put these in app_globals because we can use '_')
"""
from pylons.i18n.translation import _

import re


# in the form list_name, icon, display_text
contents_list_titles = [
    #list name , icon, description
    ('all'                 , 'article'    , _('all').capitalize()   ),
    ('drafts'              , 'draft'      , _("What I am working on now")   ),
    ('assignments_active'  , 'assignment' , _("Requests I want you to respond to")  ),
    ('assignments_previous', 'assignment' , _('previous _assignments').capitalize() ),
    ('responses'           , 'response'   , _("Responses I've written") ),
    ('articles'            , 'article'    , _("My news")    ),
]


def get_list_titles(list_name):
    for (list, icon, description) in contents_list_titles:
        if list == list_name:
            return (icon, description)
    return (list_name, list_name)


# AllanC - !!!???!! I just found this duplicated in get_action_objects_for_url in civicboomb.lib.civicboom_lib -
#          this took me ages to debug .. why wasnt this commented? why is this still here?
#actions_list = [
#    #            url identifyer                                ,  action      ,    description
#    (re.compile('/accept'                                    ) , 'accept'     , _('Accept a _assignment')),
#    (re.compile('/follow'                                    ) , 'follow'     , _('Follow a _member')    ),
#    (re.compile('/boom'                                      ) , 'boom'       , _('Boom _content')       ),
#    (re.compile('/contents/new\?parent_id='                  ) , 'new_respose', _('Create a response')   ),
#    (re.compile('/contents/new\?target_type=article'         ) , 'new_article', _('Post a _article')     ),
#    (re.compile('/contents\?(.*?)type=comment(.*?)parent_id=') , 'comment'    , _('make a comment')      ), #AllanC - I weep at the inefficency and code duplication
#    (re.compile('/contents\?(.*?)parent_id=(.*?)type=comment') , 'comment'    , _('make a comment')      ),
#]

setting_titles = {
    'password'      :   _('Password and mobile access'),
    'help_adverts'  :   _('Help and guides')
}

setting_icons = {
    'general'       :   'general',
    'password'      :   'password',
    'notifications' :   'messages',
    'location'      :   'location',
    'advanced'      :   'advanced',
    'help_adverts'  :   'help',
    'link_janrain'  :   'link_accounts',
}
