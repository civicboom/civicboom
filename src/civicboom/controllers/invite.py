from civicboom.lib.base import *

from civicboom.controllers.contents        import ContentsController
from civicboom.controllers.members         import MembersController, has_role_required
from civicboom.controllers.payments        import PaymentsController
from civicboom.controllers.member_actions  import MemberActionsController
from civicboom.controllers.group_actions   import GroupActionsController
from civicboom.controllers.payment_actions  import PaymentActionsController

import copy

from civicboom.model.member import group_member_roles, PaymentAccount


contents_controller        = ContentsController()
members_controller         = MembersController()
payments_controller        = PaymentsController()
member_actions_controller  = MemberActionsController()
group_actions_controller   = GroupActionsController()
payment_actions_controller = PaymentActionsController()


def get_payment_account(id):
    return Session.query(PaymentAccount).get(id)

def check_member(member):
    return has_role_required('editor', c.logged_in_persona_role) and member == c.logged_in_persona

def check_payment_account(payment_account):
    return has_role_required('admin', c.logged_in_persona_role) and c.logged_in_persona in payment_account.members

def check_assignment(content):
    return content.editable_by(c.logged_in_persona)


def roles_group(group):
    roles = group_member_roles.enums
    roles = [role for role in roles if has_role_required(role, c.logged_in_persona_role)]
    return roles
search_limit = 6

invite_types = {
    'group' : {
        'key'           : 'member',
        'type'          : 'group',
        'get'           : get_member,
        'show'          : members_controller.show,
        'check'         : check_member,
        'method'        : 'invite',
        'roles'         : roles_group,
    },
    'assignment'        : {
        'key'           : 'content',
        'type'          : 'assignment',
        'get'           : get_content,
        'show'          : contents_controller.show,
        'check'         : check_assignment,
        'method'        : 'invite',
    },
    'trusted_follower' : {
        'key'           : 'member',
        
        'get'           : get_member,
        'show'          : members_controller.show,
        'check'         : check_member,
        'method'        : 'follower_invite_trusted',
    },
    'payment_add_user' : {
        'key'           : 'payment_account',
        
        'get'           : get_payment_account,
        'show'          : payments_controller.show,
        'check'         : check_payment_account,
        'method'        : 'member_add',
        'exclude'       : 'members',
        'frag_refresh'  : '/payments' #url('payments'), # AllanC - url may not have been defined at this point, it was failing tests on my machine only as it was the first test run.
    }
}


def re_key(dictionary):
   # Re-create key numbering
    keys = sorted(dictionary.keys())
    key_map = {}
    i = 0
    for key in keys:
        key_map[key] = i
        i = i + 1
            
    return dict([ (key_map[key], dictionary[key]) for key in dictionary.keys()] )


class InviteController(BaseController):
    """
    a controller which produces a nice graphical invite fragment
    """

    @web
    @authorize
    def index(self, **kwargs):
        """
        GET /index: Get an invite fragment

        @a-pi invite 1.0 (WIP)

        @return 200      page ok
        @return 500      invalid parameters
        @return 404      item does not exist
        @return 403      invite not possible for this item
        """
        
        # Get item type and id
        type = invite_types.get(kwargs.get('invite'))
        id   = kwargs.get('id')
        search_offset  = int(kwargs.get('search-offset' , 0))
        invitee_offset = int(kwargs.get('invitee-offset', 0))
        if not type or not id:
            raise action_error('need type and id', code=500)
        
        # Get item
        item = type['get'](id)
        
        # Exclude object results
        object_exclude_members = []
        if type.get('exclude'):
            object_exclude_members = [member.username for member in getattr(item, type.get('exclude'))]
        form_exclude_members = kwargs.get('exclude-members', '').split(',')
        form_exclude_members.extend(object_exclude_members)
        kwargs['exclude-members'] = ','.join(form_exclude_members)
        
        if not item:
            raise action_error('could not find item', code=404)
        
        # Check item type
        if type.get('type'):
            if item.__type__ != type['type']:
                raise action_error('invite not possible for this object type', code=403)
        
        # Check item permission
        if not type['check'](item):
            raise action_error('no permission', code=403)
        
        # Get roles and check current role if applicable
        roles = type['roles'](item) if type.get('roles') else None
        role = kwargs.get('invite-role')
        if role:
            if not type.get('roles'):
                role = None
        if roles and role not in roles:
            role = item.default_role
        
        # Get form items
        invitee_list   = {}
        invitee_add    = {}
        invitee_remove = []
        if request.environ['REQUEST_METHOD'] == 'POST':
            for key in request.POST:
                order = None
                if key.count('-') > 0:
                    list, order = key.split('-',1)
                    value       = request.POST[key]
                    if   list == 'inv' and order:
                        user = get_member(value)
                        invitee_list[int(order)] = user.to_dict()
                    elif list == 'add' and order:
                        user = get_member(order)
                        invitee_add[order] = user.to_dict()
                    elif list == 'rem' and order != None:
                        invitee_remove.append(int(order))
                    elif list == 'invitee':
                        if   order == 'button':
                            pass
                        elif order == 'prev':
                            invitee_offset -= search_limit
                            if invitee_offset < 0:
                                invitee_offset = 0
                            pass
                        elif order == 'next':
                            invitee_offset += search_limit
                            pass
        
        # Remove removed items from invitee list
        invitee_usernames = [invitee_list[key]['username'] for key in invitee_list.keys() if key not in invitee_remove]
        invitee_list = dict([(key, invitee_list[key]) for key in invitee_list.keys() if invitee_list[key]['username'] in invitee_usernames])
                
        invitee_list = re_key(invitee_list)
        
        if 'submit-everyone' in request.POST:
            if kwargs.get('search-type', '') != '':
                everyone_search = dict([(user['username'], get_member(user['username']).to_dict()) for user in self.search(limit_override=1000, **kwargs)['data']['invite_list']['items'] if user['username'] not in invitee_usernames])
                invitee_add.update(everyone_search)
            else:
                set_flash_message({'status': 'error', 'message':_('You cannot add everyone!')})
        
        # Add new additions to invitee_list
        for username in invitee_add.keys():
            if username not in [user['username'] for user in invitee_list.values()]:
                invitee_list[len(invitee_list)] = invitee_add[username]
        
        invitee_usernames = [invitee_list[key]['username'] for key in invitee_list.keys()]
        
        message = None
        error_list = None
        
        if 'submit-invite' in request.POST and 'submit-everyone' not in request.POST:
            error_list = {}
            if len(invitee_list) > 0:
                for key in invitee_list.keys():
                    invitee = copy.deepcopy(invitee_list[key])
                    method = getattr(item, type['method'], None)
                    if method:
                        try:
                            method(invitee['username'], role=role)
                        except action_error as error:
                            error.original_dict['data'] = invitee
                            error_list[invitee['username']] = error.original_dict
                if len(error_list) > 0:
                    message = _('Invited everyone except:') + ' ' + ','.join(error_list.keys())
                    invitee_list = dict([(key, invitee_list[key]) for key in invitee_list.keys() if invitee_list[key]['username'] in error_list.keys()])
                    invitee_list = re_key(invitee_list)
                else:
                    message = _('Invited everyone')
                    invitee_list = {}
            else:
                message = _('Nobody to invite')
            invitee_offset = 0
            invite_offset = 0
            
        # Process invitee list into near-proper list format
        invitee_list = {'count' : len(invitee_list),
                        'items'  : invitee_list,
        }
        
        # search data
        data = self.search(**kwargs)['data']
        
        object_exclude_members.extend(invitee_usernames)
        
        # If we are rendering a static page we need the object's data GregM: OH NO WE DON'T
#        if c.format == 'html':
#            data.update(type['show'](id = id)['data'])
        
        # Overlay any of the invite list's data over any object's data
        data.update( {
            'invitee_list'    : invitee_list,
            'invitee-offset'  : invitee_offset,
            'invite'          : kwargs.get('invite'),
            'id'              : kwargs.get('id'),
            'exclude-members' : ','.join(object_exclude_members),
            'actions'         : [],
            'invite-role'     : role,
            'frag_refresh'    : type.get('frag_refresh', '')
        } )
        
        if error_list:
            data.update( {'error-list': error_list})
            
        if roles:
            data.update( {'roles': roles})
        
        return action_ok(data=data, message=message)
    
    @web
    @authorize
    def show (self, id, **kwargs):
        kwargs['id'] = id
        return self.index(**kwargs)
    
    @web
    @authorize
    def search(self, **kwargs):
        search_offset = int(kwargs.get('search-offset', 0))
        
        if 'search-prev' in request.POST:
            search_offset -= search_limit
            if search_offset < 0:
                search_offset = 0
            pass
        elif 'search-next' in request.POST:
            search_offset += search_limit
            pass
        else:
            search_offset = 0
        
        search_type = {}
        if not kwargs.get('search-type', '') == '':
            search_type[kwargs['search-type']] = c.logged_in_persona.username
        
        invite_list = members_controller.index(
            type   = None,                                      # could search for users and hubs separately kwargs.get('type')
            limit  = kwargs.get('limit_override') or search_limit,
            offset = search_offset,
            term   = kwargs.get('search-name'),
            exclude_members = kwargs.get('exclude-members'),
            sort   = 'name',
            **search_type
        )['data']['list']
        
        data = {
            'invite_list'     : invite_list,
            'search-name'     : kwargs.get('search-name'),
            'search-type'     : kwargs.get('search-type'),
            'search-offset'   : search_offset,
            'search-limit'    : search_limit,
            'exclude-members' : kwargs.get('exclude-members'),
        }
        
        return action_ok(data=data)
