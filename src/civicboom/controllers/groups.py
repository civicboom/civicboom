from civicboom.lib.base import *

from civicboom.model.member import Group, GroupMembership
from civicboom.lib.form_validators.base import DefaultSchema
from civicboom.lib.form_validators.registration import UniqueUsernameValidator
from civicboom.lib.misc import update_dict

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

class CreateGroupSchema(DefaultSchema):
    name = UniqueUsernameValidator()

def _get_group(id, admin_only=False):
    group = get_group(id)
    if not group:
        raise error_not_found
    if check_admin and not group.is_admin(c.logged_in_user):
        raise error_unauthorised
    return group


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
        
        try:                                                # Try validation
            schema = CreateGroupSchema()                    #   Build schema
            form   = schema.to_python(dict(kwargs))         #   Validate
        except formencode.Invalid, error:                   # Form has failed validation
            form        = error.value                       #   Setup error vars
            form_errors = error.error_dict or {}            #   
            raise action_error(message="unable to create group")
        
        group              = Group()
        group.name         = form['name']
        group.status       = 'show'
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
        
        group = _get_group(id, check_admin=True)
        

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id):
        """
        DELETE /contents/{id}: Delete an existing group
        (aka POST /contents/{id} with POST[_method] = "DELETE")
        
        @return 403 - lacking permission
        @return 200 - content deleted successfully
        """
        group = _get_group(id, check_admin=True)
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
        group = _get_group(id, check_admin=True)
        return action_ok(data={'group':group.to_dict()})
