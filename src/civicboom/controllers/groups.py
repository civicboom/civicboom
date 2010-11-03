from civicboom.lib.base import *

from civicboom.model.member import Group, GroupMembership, group_member_roles, group_join_mode, group_member_visability, group_content_visability

from civicboom.lib.form_validators.dict_overlay import validate_dict

import formencode

from civicboom.lib.form_validators.base         import DefaultSchema
from civicboom.lib.form_validators.registration import UniqueUsernameValidator

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

class GroupSchema(DefaultSchema):
    name                       = formencode.validators.String(max=255, min=2               , not_empty=False)
    description                = formencode.validators.String(max=255, min=2               , not_empty=False)
    default_role               = formencode.validators.OneOf(group_member_roles.enums      , not_empty=False)
    join_mode                  = formencode.validators.OneOf(group_join_mode.enums         , not_empty=False)
    member_visability          = formencode.validators.OneOf(group_member_visability.enums , not_empty=False)
    default_content_visability = formencode.validators.OneOf(group_content_visability.enums, not_empty=False)

class CreateGroupSchema(GroupSchema):
    username                   = UniqueUsernameValidator()


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_group(id, is_admin=False):
    """
    Shortcut to return a group and raise not found or permission exceptions automatically (as these are common opertations every time a group is fetched)
    """
    group = get_group(id)
    if not group:
        raise action_error(_("group not found"), code=404)
    if is_admin and not group.is_admin(c.logged_in_persona):
        raise action_error(_("you do not have permission for this group"), code=403)
    return group


#-------------------------------------------------------------------------------
# Group Controler
#-------------------------------------------------------------------------------

class GroupsController(BaseController):
    """
    @doc groups
    @title Groups
    @desc REST Controller styled on the Atom Publishing Protocol
    """
    
    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    def index(self, **kwargs):
        """
        GET /groups: All groups the current user is a member of
        
        @param * (see common list return controls)
        
        @return 200 - data.list = array of group objects that logged in user is a member including the additional field 'members "role" in the group'
        """
        # url('groups')
        
        # member searching?
        
        pass



    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def create(self, **kwargs):
        """
        POST /groups: Create a new group
        
        Creates a new group with the specifyed username with the currently logged in user as as administrator of the new group
        
        @param username - a unique username, cannot clash with existing usernames
        @param *        - see "POST /groups"
        
        @return 400 - data invalid (ie, username that already exisits)
        @return 201 - group created, data.id = new group id
        @return 301 - if format redirect specifyed will redirect to show group
        """
        # url('groups') + POST
        
        data       = {'group':kwargs, 'action':'create'}
        data       = validate_dict(data, CreateGroupSchema(), dict_to_validate_key='group', template_error='groups/edit')
        group_dict = data['group']
        
        group              = Group()
        group.username     = group_dict['username']
        group.status       = 'active'
        group_admin        = GroupMembership()
        group_admin.member = c.logged_in_persona
        group_admin.role   = "admin"
        group.members_roles.append(group_admin)
        Session.add(group)
        Session.commit()
        
        self.update(group.id) # Overlay any additional form fields over the new group object using the update method - also intercepts if format is redirect
        
        return action_ok(message=_('group created ok'), data={'id':group.id}, code=201)


    @auto_format_output
    @authorize(is_valid_user)
    def new(self):
        """
        GET /groups/new - Form to create a new item
        
        @return 200 - ???
        """
        #url_for('new_group')
        return action_ok(template='groups/edit')


    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def update(self, id, **kwargs):
        """
        PUT /groups/{id} - Update a groups settings
        (aka POST /groups/{id} with POST[_method] = "PUT")
        
        @param * - see "POST contents"
        
        @return 403 - lacking permission to edit
        @return 200 - success
        """
        group = _get_group(id, is_admin=True)
        
        group_dict = group.to_dict()
        group_dict.update(kwargs)
        data = {'group':group_dict, 'action':'edit'}
        data = validate_dict(data, GroupSchema(), dict_to_validate_key='group', template_error='groups/edit')
        group_dict = data['group']
        
        group.name                       = group_dict['name']
        group.description                = group_dict['description']
        group.default_role               = group_dict['default_role']
        group.join_mode                  = group_dict['join_mode']
        group.member_visability          = group_dict['member_visability']
        group.default_content_visability = group_dict['default_content_visability']
        
        Session.commit()
        
        if c.format == 'html':
            return redirect(url('group', id=group.id))
        
        return action_ok(message=_('group updated ok'), data=data)


    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id):
        """
        DELETE /group/{id}: Delete an existing group
        (aka POST /group/{id} with POST[_method] = "DELETE")
        
        Current user must be identifyed as an administrator of this group.
        
        @api groups 1.0 (WIP)
        
        @return 403 - lacking permission
        @return 404   group not found to delete
        @return 200 - group deleted successfully
        """
        group = _get_group(id, is_admin=True)
        group.delete()
        return action_ok(_("group deleted"), code=200)


    @auto_format_output
    @web_params_to_kwargs
    def show(self, id, **kwargs):
        """
        GET /group/{id}: Show a specific item
        
        @api groups 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                group    group object (with list of members [if group members public])
        @return 404      group not found
        """
        if 'list_type' not in kwargs:
            kwargs['list_type'] = 'full+actions'
        group = _get_group(id)
        return action_ok(data={'group':group.to_dict(**kwargs)})


    @auto_format_output
    @authorize(is_valid_user)
    def edit(self, id):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        
        Current user must be identifyed as an administrator of this group.
        """
        # url('edit_group', id=ID)
        group = _get_group(id, is_admin=True)
        return action_ok(data={'group':group.to_dict(), 'action':'edit'}) #Auto Format with activate HTML edit template automatically if template placed/named correctly
