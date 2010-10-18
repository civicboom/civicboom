from civicboom.lib.base import *

from civicboom.model.member import Group, GroupMembership, group_member_roles, group_join_mode, group_member_visability, group_content_visability
from civicboom.lib.form_validators.base import DefaultSchema
from civicboom.lib.form_validators.registration import UniqueUsernameValidator
from civicboom.lib.misc import update_dict
from civicboom.lib.form_validators.dict_overlay import overlay_errors

import formencode


log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------


error_not_found    = action_error(_("group not found"), code=404)
error_unauthorised = action_error(_("you do not have permission access this group"), code=403)

#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

class GroupSchema(DefaultSchema):
    name                = formencode.validators.String(max=255, min=2               , not_empty=False)
    description         = formencode.validators.String(max=255, min=2               , not_empty=False)
    default_role        = formencode.validators.OneOf(group_member_roles.enums      , not_empty=False)
    join_mode           = formencode.validators.OneOf(group_join_mode.enums         , not_empty=False)
    member_visability   = formencode.validators.OneOf(group_member_visability.enums , not_empty=False)
    content_visability  = formencode.validators.OneOf(group_content_visability.enums, not_empty=False)

class CreateGroupSchema(GroupSchema):
    username            = UniqueUsernameValidator()


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_group(id, is_admin=False):
    """
    Shortcut to return a group and raise not found or permission exceptions automatically (as these are common opertations every time a group is fetched)
    """
    group = get_group(id)
    if not group:
        raise error_not_found
    if is_admin and not group.is_admin(c.logged_in_user):
        raise error_unauthorised
    return group

def validate_group_dict(group_dict, schema, action='create'):
    """
    When groups are created or edited the form contents need to be validated
    """
    # Convert kwargs and form post to dict for overlaying
    group = {}
    for key in group_dict.keys():
        group[key] = {
            'name' : key,
            'value': group_dict[key]
        }
    
    try:                                                # Try validation
        #schema = CreateGroupSchema()                    #   Build schema
        return schema.to_python(dict(group_dict))         #   Validate
    except formencode.Invalid, error:                   # Form has failed validation
        group['missing'] = []
        overlay_errors(error, group.values(), group['missing'])
        return {'status':'error', 'message':'failed validation', 'data': {'group':group, 'action':action}, 'template':'groups/edit'}
        #raise action_error(message="unable to create group", data=kwargs)


#-------------------------------------------------------------------------------
# Group Controler
#-------------------------------------------------------------------------------

class GroupsController(BaseController):
    
    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    def index(self, **kwargs):
        """
        GET /groups: All groups the current user belongs to
        
        @param exclude_fields - 
        
        @return 200 - data.list = array of group objects that logged in user is a member including the members role in the group
        """
        # url('groups')
        groups = [update_dict(group_role.group.to_dict(**kwargs), {'role':group_role.role}) for group_role in c.logged_in_user.groups_roles]
        return action_ok(data={'list': groups})


    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    @authenticate_form
    def create(self, **kwargs):
        """
        POST /groups: Create a new group
        
        @param form_title
        @param form_contents
        @param form_type
        @param ...
        
        @return 400 - missing data (ie, a type=comment with no parent_id)
        @return 201 - content created, data.id = new content id
        """
        # url('contents') + POST
        form = validate_group_dict(kwargs, CreateGroupSchema(), action='create')
        
        group              = Group()
        group.username     = form['username']
        group.status       = 'active'
        group_admin        = GroupMembership()
        group_admin.member = c.logged_in_user
        group_admin.role   = "admin"
        group.members_roles.append(group_admin)
        Session.add(group)
        Session.commit()
        
        self.update(group.id) # Overlay any additional form fields over the new group object using the update method
        
        return action_ok(message=_('group created ok'), data={'id':group.id}, code=201)


    @auto_format_output()
    @authorize(is_valid_user)
    def new(self):
        """
        GET /groups/new - Form to create a new item
        
        @return 200 - ???
        """
        #url_for('new_group')
        return action_ok(template='groups/edit')


    @auto_format_output()
    @web_params_to_kwargs()
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
        
        group_dict = group.to_dict('single')
        group_dict.update(kwargs)
        form = validate_group_dict(group_dict, GroupSchema(), action='edit')
        
        group.name                = form['name']
        group.description         = form['description']
        group.default_role        = form['default_role']
        group.join_mode           = form['join_mode']
        group.member_visability   = form['member_visability']
        group.content_visability  = form['content_visability']
        
        Session.commit()
        
        return action_ok(message=_('group updated ok'), data={'group':group.to_dict(), 'action':'edit'})


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id):
        """
        DELETE /groups/{id}: Delete an existing group
        (aka POST /groups/{id} with POST[_method] = "DELETE")
        
        @return 403 - lacking permission
        @return 200 - content deleted successfully
        """
        group = _get_group(id, is_admin=True)
        group.delete()
        return action_ok(_("group deleted"), code=200)


    @auto_format_output()
    def show(self, id):
        """
        GET /group/{id}: Show a specific item
        
        @return 200 - data.content = group object (with list of members [if public])
        """
        group = _get_group(id)
        return action_ok(data={'group':group.to_dict('actions')})


    @auto_format_output()
    @authorize(is_valid_user)
    def edit(self, id):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        """
        # url('edit_content', id=ID)
        group = _get_group(id, is_admin=True)
        return action_ok(data={'group':group.to_dict(), 'action':'edit'})
