"""
Set of helpers specific to the Civicboom project
  (these are not part of misc because misc continas more genereal functions that could be used in a range of projects)
"""

from civicboom.lib.base import url, _, current_url
import re

import logging
log      = logging.getLogger(__name__)


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
        (re.compile('/contents/new\?target_type=article'         ) , 'new_article', _('post a _article') ),
        (re.compile('/contents\?(.*?)type=comment(.*?)parent_id=') , 'comment'    , _('make a comment')      ), #AllanC - I weep at the inefficency and code duplication
        (re.compile('/contents\?(.*?)parent_id=(.*?)type=comment') , 'comment'    , _('make a comment')      ),
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
