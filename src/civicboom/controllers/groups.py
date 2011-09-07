from civicboom.lib.base import *
from cbutils.misc import make_username

from civicboom.controllers.account import AccountController
set_persona = AccountController().set_persona

from civicboom.model.member import Group, GroupMembership, group_member_roles, group_join_mode, group_member_visibility, group_content_visibility, Member

#from civicboom.controllers.contents import _normalize_member # now part of base

from civicboom.controllers.contents import ContentsController

create_content = ContentsController().create

from civicboom.lib.form_validators.dict_overlay import validate_dict

import formencode

from civicboom.lib.form_validators.base         import DefaultSchema
from civicboom.lib.form_validators.registration import UniqueUsernameValidator

from civicboom.controllers.settings import SettingsController

import re

from civicboom.lib.communication.email_lib import send_email

settings_update = SettingsController().update

log      = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

# This also appears in Setting Controller
class PrivateGroupValidator(formencode.validators.FancyValidator):
    messages = {
        'invalid'           : x_('Value must be one of: public; private'),
        'require_upgrade'   : x_('You require a paid account to use this feature, please contact us!'),
        }

    def _to_python(self, value, state):
        if value not in ['public', 'private']:
            raise formencode.Invalid(self.message('invalid', state), value, state)
        if value == "private" and not c.logged_in_persona.has_account_required('plus'):
            raise formencode.Invalid(self.message('require_upgrade', state), value, state)
        return value
        

class GroupSchema(DefaultSchema):
    name                       = formencode.validators.String(max=255, min=4               , not_empty=False)
    description                = formencode.validators.String(max=4096, min=0              , not_empty=False)
    default_role               = formencode.validators.OneOf(group_member_roles.enums      , not_empty=False)
    join_mode                  = formencode.validators.OneOf(group_join_mode.enums         , not_empty=False)
    member_visibility          = PrivateGroupValidator()
    default_content_visibility = PrivateGroupValidator()


class CreateGroupSchema(GroupSchema):
    username                   = UniqueUsernameValidator()


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------


def _gen_username(base):
    if Session.query(Member).filter(Member.id==base).count() == 0:
        return base

    if not re.search(base, "[0-9]$"):
        base = base + "2"
    while Session.query(Member).filter(Member.id==base).count() > 0:
        name, num = re.match("(.*?)([0-9]+)", base).groups()
        base = name + str(int(num)+1)
    return base


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
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
        
        #if 'status' not in kwargs:
        #    kwargs['status']
            
        
        results = Session.query(Member).join(Group, Member, Group.members_roles)
        
        if 'group' in kwargs:
            group   = normalize_member(kwargs['group'])
            results = results.filter(Group.id==group)
        
        if 'member' in kwargs:
            member   = normalize_member(kwargs['member'])
            results = results.filter(Member.id==member)
        
        #results = results.filter(Member.status=='active')

        if 'limit' not in kwargs: #Set default limit and offset (can be overfidden by user)
            kwargs['limit'] = config['search.default.limit']
        if 'offset' not in kwargs:
            kwargs['offset'] = 0

        results = results.order_by(Member.name.asc())
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        # Return search results
        return action_ok(
            data = {'list': [member.to_dict(**kwargs) for member in results.all()]} ,
        )

    @web
    @auth
    @role_required('admin')
    def create(self, **kwargs):
        """
        POST /groups: Create a new group

        Creates a new group with the specified username with the currently
        logged in user as as administrator of the new group

        @api groups 1.0 (WIP)
        
        @param username                   a unique username, cannot clash with existing usernames
        @param name                       display name
        @param description                description of groups purpose
        @param default_role
            admin
            editor
            contributor
            observer
        @param join_mode
            public
            invite
            invite_and_request
        @param member_visibility
            public
            private 
        @param default_content_visibility (plus account required)
            public
            private 
        
        @return 400  data invalid (ie, username that already exisits)
        @return 201  group created, data.id = new group id
        @return 301  if format redirect specifyed will redirect to show group
        """
        
        create_push_assignment = kwargs.get('create_push_assignment')
        if create_push_assignment:
            del kwargs['create_push_assignment']
            
            
        # url('groups') + POST
        # if only display name is specified, generate a user name
        if not kwargs.get('username') and kwargs.get("name"):
            kwargs["username"] = _gen_username(make_username(kwargs.get("name")))

        # if only user name is specified, generate a display name
        if not kwargs.get('name') and kwargs.get("username"):
            kwargs["name"] = kwargs.get("username")
        
        if not c.logged_in_persona.has_account_required('plus'):
            if not kwargs.get('member_visibility'):
                kwargs['member_visibility'] = 'public'
            if not kwargs.get('default_content_visibility'):
                kwargs['default_content_visibility'] = 'public'
        
        # Need to validate before creating group, not sure how we could do this via settings controller :S GregM
        data       = {'settings':kwargs, 'action':'create'}
        data       = validate_dict(data, CreateGroupSchema(), dict_to_validate_key='settings', template_error='groups/edit')
        group_dict = data['settings']
        
        
        # Create and set group admin here!
        group              = Group()
        group.id           = group_dict['username']
        group.name         = group_dict['name']
        group.status       = 'active'
        group_admin        = GroupMembership()
        group_admin.member = c.logged_in_persona
        group_admin.role   = "admin"
        group.members_roles.append(group_admin)
        group.payment_account = c.logged_in_persona.payment_account # The group is allocated the same payment account as the creator. All groups are free but if they want the plus features like approval and private content then this is needed
        
        #AllanC - TODO - limit number of groups a payment account can support - the could be the differnece between plus and corporate
        
        # GregM: Create current user as admin of group too to allow them to admin group (until permission tree is sorted!)
        #if isinstance(c.logged_in_persona, Group):
        #    group_admin_user        = GroupMembership()
        #    group_admin_user.member = c.logged_in_user
        #    group_admin_user.role   = "admin"
        #    group.members_roles.append(group_admin_user)
        
        Session.add(group)
        Session.commit()
        
        # AllanC - Hack
        # The group has been created, but the additional feilds handled by the settings controller need to be updated (e.g. description and logo image)
        # However, we have not set c.logged_in_persona so the call to the settings controller will not have the permissions for the newly created group
        # We fake the login here
        # We cant use set_persona as this called the set_persona controller action and calls a redirect
        logged_in_persona = c.logged_in_persona # have to remeber previous persona to return to or set_persona below thinks were already swiched and will perform no action
        logged_in_persona_role = c.logged_in_persona_role
        c.logged_in_persona      = group
        c.logged_in_persona_role = 'admin'
        
        # AllanC - old call? to be removed?
        # self.update(group.username, **kwargs) # Overlay any additional form fields over the new group object using the update method - also intercepts if format is redirect
        
        # Call settings controller to update group settings!
        kwargs['panel'] = 'general'
        
        settings_update(group, private=True, **kwargs)
        
        # GregM: Create new request for group (Arrgh, have to fudge the format otherwise we cause a redirect):
        format = c.format
        if create_push_assignment:
            c.format = 'python'
            assignment = create_content(type='assignment', private=False, title=_("Send us your stories"), content=_("Join us in making the news by telling us your stories, sending in videos, pictures or audio: Get recognition and get published - share your news with us now!"), format="python")
            group.config['push_assignment'] = assignment.get('data', {}).get('id')
            
        c.format = format
        
        
        c.logged_in_persona = logged_in_persona
        c.logged_in_persona_role = logged_in_persona_role
        
        user_log.info("Created Group #%s (%s)" % (group.id, group.name))
        
        # AllanC - Temp email alert for new group
        send_email(config['email.event_alert'], subject='new group', content_text='%s - %s by %s' % (c.logged_in_persona.username, c.logged_in_persona.name, c.logged_in_user.username))
        
        # GregM: prompt_aggregate for new group :)
        set_persona(group, prompt_aggregate=True) # Will redirect if in html or redirect mode
        
        return action_ok(message=_('group created'), data={'id':group.id}, code=201)


    @web
    #@auth ? need token?
    @authorize
    @role_required('admin')
    def new(self, **kwargs):
        """
        GET /groups/new: Form to create a new item
        
        @return 200 - ???
        """
        #url_for('new_group')
        ##print settings_base
        return action_ok( action="create", template='groups/create')


    @web
    @auth
    @role_required('admin')
    def update(self, id, **kwargs):
        """
        PUT /groups/{id}: Depricated!
        """
        # h.form(h.url_for('message', id=ID), method='delete')
        # Rather than delete the setting this simple blanks the required fields - or removes the config dict entry
        raise action_error(_('operation not supported'), code=501)
        group = get_group(id, is_current_persona_admin=True)
        
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
        group.default_content_visibility = group_dict.get('default_content_visibility', "public") # Shish: hack
        
        # GregM: call settings_update with logo_file as avatar
        # ARRRGHHH: Hacked c.format as settings_update redirects on html
        # old_persona = c.logged_in_persona
        
        ## GregM DIRTIEST HACK IN HISTORY! OMFG! Works... do not try this at home!
        
        Session.commit()
        
        cformat = c.format
        cpersona = c.logged_in_persona
        c.logged_in_persona = group
        c.format = 'python'
        if 'description' in kwargs:
            settings_update(id=id, description=kwargs['description'])
        if 'avatar' in kwargs:
            settings_update(id=id, avatar=kwargs['avatar'])
        if 'website' in kwargs:
            settings_update(id=id, website=kwargs['website'])
        c.format = cformat
        c.logged_in_persona = cpersona
        
        Session.commit()

        user_log.info("Updated Group #%d (%s)" % (group.id, group.username))
        
        if c.format == 'html':
            ##return redirect(url('members', id=group.username))
            set_persona(group)
            
        return action_ok(message=_('group updated'), data=data)


    @web
    @auth
    @role_required('admin')
    def delete(self, id, **kwargs):
        """
        DELETE /group/{id}: Delete an existing group
        
        Current user must be identifyed as an administrator of this group.
        
        @api groups 1.0 (WIP)
        
        @return 403 lacking permission
        @return 404 group not found to delete
        @return 200 group deleted successfully
        """
        group = get_group(id, is_current_persona_admin=True)
        user_log.info("Deleted Group #%s (%s)" % (group.id, group.name))
        group.delete()
        c.html_action_fallback_url = url('/')
        set_persona(c.logged_in_user)
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
    @role_required('admin')
    def edit(self, id, **kwargs):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        
        Current user must be identified as an administrator of this group.
        
        This will now redirect to the settings controller.
        """
        # url('edit_group', id=ID)
        # GregM: BIG DIRTY HACK to show website and description in the group config editor.
        group = get_group(id, is_current_persona_admin=True)
        config = group.config
        groupdict = group.to_dict()
        groupdict['website'] = config.get('website')
        groupdict['description'] = config.get('description')

        redirect_url = ('/settings/'+id).encode('ascii','ignore')
        return redirect(url(redirect_url))
#        # url('edit_group', id=ID)
#        # GregM: BIG DIRTY HACK to show website and description in the group config editor.
#        group = _get_group(id, is_admin=True)
#        config = group.config
#        groupdict = group.to_dict()
#        groupdict['website'] = config.get('website')
#        groupdict['description'] = config.get('description')
#        
#        return action_ok(data={'group':groupdict, 'action':'edit'}) #Auto Format with activate HTML edit template automatically if template placed/named correctly
