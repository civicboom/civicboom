"""
Consistants

(cant put these in app_globals because we can use '_')
"""
from civicboom.lib.base import url, current_url, _
import re


def get_list_titles(list_name):
    contents_list_titles = [
        # list name,             icon,          description
        ('all'                 , 'article'    , _('all').capitalize()   ),
        ('drafts'              , 'draft'      , _("Drafts")   ),
        ('assignments_active'  , 'assignment' , _("Requests I want you to respond to")  ),
        ('assignments_previous', 'assignment' , _('previous _assignments').capitalize() ),
        ('responses'           , 'response'   , _("Responses I've written") ),
        ('articles'            , 'article'    , _("My news")    ),
    ]

    for (list, icon, description) in contents_list_titles:
        if list == list_name:
            return (icon, description)

    return (list_name, list_name)


def setting_titles():
    return {
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


#-------------------------------------------------------------------------------
# Signin Actions
#-------------------------------------------------------------------------------

def get_action_objects_for_url(action_url=None):
    """
    If signing in and performing an action
    Will return ()
    """
    from civicboom.lib.helpers import get_object_from_action_url
    from civicboom.controllers.members  import MembersController
    from civicboom.controllers.contents import ContentsController
    content_show = ContentsController().show
    member_show  = MembersController().show

    actions_list = [
        #            url identifyer                                ,  action      ,    description
        (re.compile('/signout'                                   ) , 'signout'    , _('sign out')            ),
        (re.compile('/accept'                                    ) , 'accept'     , _('accept a _assignment')),
        (re.compile('/follow'                                    ) , 'follow'     , _('follow a _member')    ),
        (re.compile('/boom'                                      ) , 'boom'       , _('boom _content')       ),
        (re.compile('/contents/new\?parent_id='                  ) , 'new_respose', _('create a response')   ),
        (re.compile('/contents/new\?target_type=article'         ) , 'new_article', _('post a _article')     ),
        (re.compile('/contents\?(.*?)type=comment(.*?)parent_id=') , 'comment'    , _('make a comment')      ), #AllanC - I weep at the inefficency and code duplication
        (re.compile('/contents\?(.*?)parent_id=(.*?)type=comment') , 'comment'    , _('make a comment')      ),
        (re.compile('/contents/new'                              ) , 'new_article', _('create new content')  ), # Failsafe for new aticle is all 
    ]

    # If performing an action we may want to display a custom message with the login
    if not action_url:
        action_url = current_url()
    for action_identifyer, action_action, action_description in actions_list:
        if action_identifyer.search(action_url):
            args, kwargs = get_object_from_action_url( action_url )
            action_object          = {} # Set this in case we cant recover an action object
            action_object_frag_url = ''
            if args and kwargs:
                # Generate action object frag URL
                kwargs['format'] = 'frag'
                action_object_frag_url = url(*args, **kwargs)
                # Find action object
                if 'content' in args and 'id' in kwargs:
                    action_object = content_show(id=kwargs['id']).get('data')
                if 'member' in args and 'id' in kwargs:
                    action_object = member_show(id=kwargs['id']).get('data')
            return dict(
                action        = action_action          ,
                description   = action_description     ,
                action_object = action_object          ,
                frag_url      = action_object_frag_url ,
            )
    return {}
