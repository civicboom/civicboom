from civicboom.lib.base import *

from civicboom.controllers.contents       import ContentsController, list_filters as content_list_filters
from civicboom.controllers.members        import MembersController
from civicboom.controllers.member_actions import MemberActionsController
from civicboom.controllers.group_actions  import GroupActionsController
#from civicboom.controllers.messages       import MessagesController
#from civicboom.controllers.search   import SearchController
#from civicboom.controllers.groups   import GroupsController
#from civicboom.controllers.contents import ContentsController

from civicboom.model.member import Member, Group
from civicboom.model.content import AssignmentContent


contents_controller       = ContentsController()
members_controller        = MembersController()
member_actions_controller = MemberActionsController()
group_actions_controller  = GroupActionsController()
#messages_controller       = MessagesController()
#content_list_names        = content_list_filters.keys()

def check_member(member):
    if isinstance(member, Group):
        membership = member.get_membership(c.logged_in_user)
        return (has_role_required('editor', membership.role) and membership.status == 'active')
    else:
        return member.id == c.logged_in_user.id

def check_assignment(content):
    return content.editable_by(c.logged_in_persona)

invite_types = {
    'group' : {
        'key'    : 'member',
        'type'   : Group,
        'get'    : get_member,
        'show'   : members_controller.show,
        'check'  : check_member,
        'method' : 'invite'
    },
    'assignment' : {
        'key'    : 'content',
        'type'   : AssignmentContent,
        'get'    : get_content,
        'show'   : contents_controller.show,
        'check'  : check_assignment,
        'method' : 'invite'
    },
    'trusted_follower' : {
        'key'    : 'member',
        
        'get'    : get_member,
        'show'   : members_controller.show,
        'check'  : check_member,
        'method' : 'follower_invite_trusted'
    },
}


class InviteController(BaseController):
    """
    @title Invite
    @doc invite
    @desc a controller which produces a nice graphical invite fragment
    """

    @web
    @authorize
    def index(self, **kwargs):
        """
        GET /index: Get an invite fragment

        @api invite 1.0 (WIP)

        @return 200      page ok
        """
        
        # Get item type and id
        invite_type = invite_types.get(kwargs.get('invite_type'))
        invite_id   = kwargs.get('invite_id')
        if not invite_type or not invite_id:
            raise action_error('need type and id', code=500)
        
        # Get item
        item = invite_type['get'](invite_id)
        
        if not item:
            raise action_error('could not find item', code=404)
        
        # Check item type
        if invite_type.get('type'):
            if not isinstance(item, invite_type['type']):
                raise action_error('invite not possible for this object type', code=403)
        
        # Check item permission
        if not invite_type['check'](item):
            raise action_error('no permission', code=403)
        
        # Get form items
        invitee_list = {}
        invitee_remove = []
        if request.environ['REQUEST_METHOD'] == 'POST':
            for key in request.POST:
                username = None
                if key[0:4] == 'add-' and request.POST[key] == 'Add':
                    username = key[4:]
                    list = 'add'
                if key[0:4] == 'rem-' and request.POST[key] == 'Remove':
                    username = key[4:]
                    list = 'rem'
                if key[0:4] == 'inv-' and request.POST[key] == key[4:]:
                    username = key[4:]
                    list = 'add'
                if username and list == 'add':
                    user = get_member(username)
                    invitee_list[username] = user.to_dict()
                elif username and list == 'rem':
                    invitee_remove.append(username)
            if 'search' in request.POST and request.POST['search'] == 'Search':
                pass
        
        # Remove removed items from invitee list
        invitee_list = dict([(key, invitee_list[key]) for key in invitee_list if key not in invitee_remove])
        # Process invitee list into near-proper list format
        invitee_list = {'count' : len(invitee_list),
                        'items'  : invitee_list.values(),
        }
        
        # Turn search type into a parameter for index method
        search_type = {}
        if not kwargs.get('search-type', '') == '':
            search_type[kwargs['search-type']] = 'me'
        
        invite_list = members_controller.index(
            type   = kwargs.get('type'),
            limit  = 6,
            offset = kwargs.get('offset'),
            name   = kwargs.get('search-name'),
            **search_type
        )['data']['list']
        
        # If we are rendering a static page we need the object's data
        if c.format == 'html':
            data = invite_type['show'](id = invite_id)['data']
        else:
            data = {}
        
        # Overlay any of the invite list's data over any object's data
        data.update( {
            'invite_list'  : invite_list,
            'invitee_list' : invitee_list,
            'search-name'  : kwargs.get('search-name'),
            'search-type'  : kwargs.get('search-type'),
            'invite-type'  : kwargs.get('invite_type'),
            'invite-id'    : kwargs.get('invite_id'),
            'actions'      : [],
        } )
        
        return action_ok(data=data)