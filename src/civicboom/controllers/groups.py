from civicboom.lib.base import *
from civicboom.lib.misc import make_username

from civicboom.controllers.account import AccountController
set_persona = AccountController().set_persona

from civicboom.model.member import Group, GroupMembership, group_member_roles, group_join_mode, group_member_visibility, group_content_visibility

from civicboom.controllers.contents import _normalize_member

from civicboom.lib.form_validators.dict_overlay import validate_dict

import formencode

from civicboom.lib.form_validators.base         import DefaultSchema
from civicboom.lib.form_validators.registration import UniqueUsernameValidator

from civicboom.controllers.settings import SettingsController

settings_update = SettingsController().update

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
    member_visibility          = formencode.validators.OneOf(group_member_visibility.enums , not_empty=False)
    default_content_visibility = formencode.validators.OneOf(group_content_visibility.enums, not_empty=False)

class CreateGroupSchema(GroupSchema):
    username                   = UniqueUsernameValidator()


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_group(id, is_admin=False, is_member=False):
    """
    Shortcut to return a group and raise not found or permission exceptions automatically (as these are common opertations every time a group is fetched)
    """
    group = get_group(id)
    if not group:
        raise action_error(_("group not found"), code=404)
    if is_admin and not group.is_admin(c.logged_in_persona):
        raise action_error(_("you do not have permission for this group"), code=403)
    if is_member and not group.get_membership(c.logged_in_persona):
        raise action_error(_("you are not a member of this group"), code=403)
    return group


#-------------------------------------------------------------------------------
# Member Search
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Group Controler
#-------------------------------------------------------------------------------

class GroupsController(BaseController):
    """
    @doc groups
    @title Groups
    @desc REST Controller styled on the Atom Publishing Protocol
    """
    
    @web
    def index(self, **kwargs):
        """
        GET /groups: All groups the current user is a member of

        @api groups 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200 - data.list = array of group objects that logged in user is a member including the additional field 'members "role" in the group'
        """
        # url('groups')
        
        # member searching?
        
        pass

    def members(self, **kwargs):
        # AllanC: this was created for two calls
        #         member -> whats groups they were members of and there roles
        #         group  -> list members and there roles
        #
        # this had complications because of:
        #   permissions of the viewing user
        #   permissions of the group
        #   the roles need returning (so cant be part of members/index neatly)
        #
        # UNFINISHED!!!!!!!!!!!! AND BROKEN!
        
        
        # Setup search criteria
        if 'limit' not in kwargs: #Set default limit and offset (can be overfidden by user)
            kwargs['limit'] = config['search.default.limit']
        if 'offset' not in kwargs:
            kwargs['offset'] = 0
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ""
        
        #if 'status' not in kwargs:
        #    kwargs['status']
            
        
        results = Session.query(Member).join(Group, Member, Group.members_roles)
        
        if 'group' in kwargs:
            group   = _normalize_member(kwargs['group'], always_return_id=True)    
            results = results.filter(Group.id==group)
        
        if 'member' in kwargs:
            member   = _normalize_member(kwargs['member'], always_return_id=True)    
            results = results.filter(Member.id==member)
        
        #results = results.filter(Member.status=='active')

        results = results.order_by(Member.name.asc())
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        # Return search results
        return action_ok(
            data = {'list': [member.to_dict(**kwargs) for member in results.all()]} ,
        )

    @web
    @auth
    def create(self, **kwargs):
        """
        POST /groups: Create a new group

        @api groups 1.0 (WIP)
        
        Creates a new group with the specifyed username with the currently logged in user as as administrator of the new group
        
        @param username - a unique username, cannot clash with existing usernames
        @param *        - see "POST /groups"
        
        @return 400 - data invalid (ie, username that already exisits)
        @return 201 - group created, data.id = new group id
        @return 301 - if format redirect specifyed will redirect to show group
        """
        # url('groups') + POST
        # if only display name is specified, generate a user name
        if not kwargs.get('username') and kwargs.get("name"):
            kwargs["username"] = make_username(kwargs.get("name"))
        
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
        
        self.update(group.id, **kwargs) # Overlay any additional form fields over the new group object using the update method - also intercepts if format is redirect

        user_log.info("Created Group #%d (%s)" % (group.id, group.username))
        
        return action_ok(message=_('group created ok'), data={'id':group.id}, code=201)


    @web
    #@auth ? need token?
    @authorize
    def new(self, **kwargs):
        """
        GET /groups/new: Form to create a new item
        
        @return 200 - ???
        """
        #url_for('new_group')
        return action_ok(template='groups/edit')


    @web
    @auth
    def update(self, id, **kwargs):
        """
        PUT /groups/{id}: Update a groups settings

        @api groups 1.0 (WIP)
        
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
        #group.description                = group_dict['description'] GregM: Broke description saving, ARRGHHHHHH!!!!!!!!!
        group.default_role               = group_dict['default_role']
        group.join_mode                  = group_dict['join_mode']
        group.member_visibility          = group_dict['member_visibility']
        group.default_content_visibility = group_dict['default_content_visibility']
        
        # GregM: call settings_update with logo_file as avatar
        # ARRRGHHH: Hacked c.format as settings_update redirects on html
        cformat = c.format
        c.format = 'python'
        if 'description' in kwargs:
            settings_update(id=id, description=kwargs['description'])
        if 'avatar' in kwargs:
            settings_update(id=id, avatar=kwargs['avatar'])
        if 'website' in kwargs:
            settings_update(id=id, website=kwargs['website'])
        c.format = cformat
        
        Session.commit()

        user_log.info("Updated Group #%d (%s)" % (group.id, group.username))
        
        if c.format == 'html':
            ##return redirect(url('members', id=group.username))
            set_persona(group)
            
        return action_ok(message=_('group updated ok'), data=data)


    @web
    @auth
    def delete(self, id, **kwargs):
        """
        DELETE /group/{id}: Delete an existing group
        
        Current user must be identifyed as an administrator of this group.
        
        @api groups 1.0 (WIP)
        
        @return 403 lacking permission
        @return 404 group not found to delete
        @return 200 group deleted successfully
        """
        group = _get_group(id, is_admin=True)
        user_log.info("Deleted Group #%d (%s)" % (group.id, group.username))
        group.delete()
        return action_ok(_("group deleted"), code=200)


    @web
    def show(self, id, **kwargs):
        """
        GET /group/{id}: Show a specific item
        
        @api groups 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                group    group object (with list of members [if group members public])
        @return 404      group not found
        """
        from civicboom.controllers.members import MembersController
        return MembersController().show(id, **kwargs)


    @web
    #@auth ? need token
    @authorize
    def edit(self, id, **kwargs):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        
        Current user must be identified as an administrator of this group.
        """
        # url('edit_group', id=ID)
        # GregM: BIG DIRTY HACK to show website and description in the group config editor.
        group = _get_group(id, is_admin=True)
        config = group.config
        groupdict = group.to_dict()
        groupdict['website'] = config.get('website')
        groupdict['description'] = config.get('description')
        
        return action_ok(data={'group':groupdict, 'action':'edit'}) #Auto Format with activate HTML edit template automatically if template placed/named correctly
