from civicboom.lib.base import *
from civicboom.lib.form_validators.registration import CreateGroupSchema

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

error_not_found = action_error(_("group not found"), code=404)

class GroupsController(BaseController):
    
    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    def index(self, list='content'):
        """
        GET /groups: All groups the current user belongs to
        
        @param list - what type of contents to return, possible values:
          content
          assignments_active
          assignments_previous
          assignments
          articles
          drafts
        
        @return 200 - data.list = array of group objects
        """
        # url('groups')
        pass

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def create(self):
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
            form   = schema.to_python(dict(request.params)) #   Validate
        except formencode.Invalid, error:                   # Form has failed validation
            form        = error.value                       #   Setup error vars
            form_errors = error.error_dict or {}            #   
            return action_error(message="unable to create group")
        
        group              = Group()
        group.name         = form['name']
        group.status       = 'show'
        group_admin        = GroupMembership()
        group_admin.group  = group
        group_admin.member = c.logged_in_user
        group_admin.role   = "admin"
        group.members.append(group_admin)
        
        Session.add(group)
        Session.commit()
        return action_ok(message=_('group created ok'), data={'id':group.id}, code=201)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def new(self, format='html'):
        """
        GET /contents/new - Form to create a new item
        
        @return 301 - redirect to /contents/{id}/edit
        """
        #url_for('new_group')
        group_id = self.create(format='python')['data']['id']
        return redirect(url('edit_group', id=group_id))

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def update(self, id):
        """
        PUT /groups/{id} - Update a groups settings
        (aka POST /groups/{id} with POST[_method] = "PUT")
        
        @param * - see "POST contents"
        
        @return 403 - lacking permission to edit
        @return 200 - success
        """
        pass

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id, format="html"):
        """
        DELETE /contents/{id}: Delete an existing group
        (aka POST /contents/{id} with POST[_method] = "DELETE")
        
        @return 403 - lacking permission
        @return 200 - content deleted successfully
        """
        pass

    @auto_format_output()
    def show(self, id):
        """
        GET /group/{id}: Show a specific item
        
        @return 200 - data.content = group object (with list of members [if public])
        """
        group = get_member(id)
        
        if not group or group.__type__!="group":
            raise error_not_found
        
        return action_ok(
            data     = {'group':group.to_dict('actions')}
        )



    @auto_format_output()
    @authorize(is_valid_user)
    def edit(self, id, format='html'):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        """
        # url('edit_content', id=ID)
        pass
