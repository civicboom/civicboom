from civicboom.lib.base import *

from civicboom.controllers.contents       import ContentsController
from civicboom.controllers.members        import MembersController
from civicboom.controllers.member_actions import MemberActionsController
from civicboom.controllers.group_actions  import GroupActionsController

from civicboom.model.member import Member, Group
from civicboom.model.content import AssignmentContent


contents_controller       = ContentsController()
members_controller        = MembersController()
member_actions_controller = MemberActionsController()
group_actions_controller  = GroupActionsController()

def check_member(member):
    if isinstance(member, Group):
        membership = member.get_membership(c.logged_in_user)
        return (has_role_required('editor', membership.role) and membership.status == 'active')
    else:
        return member.id == c.logged_in_user.id

def check_assignment(content):
    return content.editable_by(c.logged_in_persona)

search_limit = 6

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
        @return 500      invalid parameters
        @return 404      item does not exist
        @return 403      invite not possible for this item
        """
        
        # Get item type and id
        type = invite_types.get(kwargs.get('invite'))
        id   = kwargs.get('id')
        search_offset = int(kwargs.get('search-offset', 0))
        if not type or not id:
            raise action_error('need type and id', code=500)
        
        # Get item
        item = type['get'](id)
        
        if not item:
            raise action_error('could not find item', code=404)
        
        # Check item type
        if type.get('type'):
            if not isinstance(item, type['type']):
                raise action_error('invite not possible for this object type', code=403)
        
        # Check item permission
        if not type['check'](item):
            raise action_error('no permission', code=403)
        
        # Get form items
        invitee_list   = {}
        invitee_add    = {}
        invitee_remove = []
        if request.environ['REQUEST_METHOD'] == 'POST':
            for key in request.POST:
                username = None
                order = None
                if key[0:4] == 'add-':
                    username = key[4:]
                    list = 'add'
                if key[0:4] == 'rem-':
                    order = int(key[4:])
                    list = 'rem'
                if key[0:4] == 'inv-':
                    username = request.POST[key]
                    order = int(key[4:])
                    list = 'inv'
                    
                if username and list == 'inv':
                    user = get_member(username)
                    invitee_list[order] = user.to_dict()
                elif username and list == 'add':
                    user = get_member(username)
                    invitee_add[username] = user.to_dict()
                elif order != None and list == 'rem':
                    invitee_remove.append(order)
                
            if 'search' in request.POST and request.POST['search'] == 'Search':
                # We don't need to do anything for searching as the parameters are submitted
                #  and passed to the members index
                pass
            if 'search-prev' in request.POST:
                search_offset -= search_limit
                if search_offset < 0:
                    search_offset = 0
                pass
            if 'search-next' in request.POST:
                search_offset += search_limit
                pass
        
        
        # Add new additions to invitee_list
        for username in invitee_add.keys():
            if username not in [user['username'] for user in invitee_list.values()]:
                invitee_list[len(invitee_list)] = invitee_add[username]
        
        # Remove removed items from invitee list
        invitee_usernames = [invitee_list[key]['username'] for key in invitee_list.keys() if key not in invitee_remove]
        invitee_list = dict([(key, invitee_list[key]) for key in invitee_list.keys() if invitee_list[key]['username'] in invitee_usernames])
        
        # Re-create key numbering
        invitee_keys = sorted(invitee_list.keys())
        invitee_key_map = {}
        i = 0
        for key in invitee_keys:
            invitee_key_map[key] = i
            i = i + 1
                
        invitee_list = dict([ (invitee_key_map[key], invitee_list[key]) for key in invitee_list.keys()] )
        
        
        # Process invitee list into near-proper list format
        invitee_list = {'count' : len(invitee_list),
                        'items'  : invitee_list,
        }
        
        # Turn search type into a parameter for index method
        search_type = {}
        if not kwargs.get('search-type', '') == '':
            search_type[kwargs['search-type']] = 'me'
        
        invite_list = members_controller.index(
            type   = None,                                      # could search for users and hubs separately kwargs.get('type')
            limit  = search_limit,
            offset = search_offset,
            name   = kwargs.get('search-name'),
            exclude_members = ','.join(invitee_usernames),
            **search_type
        )['data']['list']
        
        # If we are rendering a static page we need the object's data
        if c.format == 'html':
            data = type['show'](id = id)['data']
        else:
            data = {}
        
        # Overlay any of the invite list's data over any object's data
        data.update( {
            'invite_list'     : invite_list,
            'invitee_list'    : invitee_list,
            'search-name'     : kwargs.get('search-name'),
            'search-type'     : kwargs.get('search-type'),
            'search-offset'   : search_offset,
            'search-limit'    : search_limit,
            'invite'          : kwargs.get('invite'),
            'id'              : kwargs.get('id'),
            'exclude-members' : ','.join(invitee_usernames),
            'actions'         : [],
        } )
        
        
        return action_ok(data=data)
    
    @web
    @authorize
    def search(self, **kwargs):
        search_offset = int(kwargs.get('search-offset', 0))
        
        if 'search-prev' in request.POST and request.POST['search-prev'] == '<<':
            search_offset -= search_limit
            if search_offset < 0:
                search_offset = 0
            pass
        if 'search-next' in request.POST and request.POST['search-next'] == '>>':
            search_offset += search_limit
            pass
        
        search_type = {}
        if not kwargs.get('search-type', '') == '':
            search_type[kwargs['search-type']] = 'me'
        
        invite_list = members_controller.index(
            type   = None,                                      # could search for users and hubs separately kwargs.get('type')
            limit  = search_limit,
            offset = search_offset,
            name   = kwargs.get('search-name'),
            exclude_members = kwargs.get('exclude-members'),
            **search_type
        )['data']['list']
        
        # Overlay any of the invite list's data over any object's data
        data = {
            'invite_list'     : invite_list,
            'search-name'     : kwargs.get('search-name'),
            'search-type'     : kwargs.get('search-type'),
            'search-offset'   : search_offset,
            'search-limit'    : search_limit,
            'exclude-members' : kwargs.get('exclude-members'),
        }
        
        return action_ok(data=data)