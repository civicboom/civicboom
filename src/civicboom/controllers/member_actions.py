"""
Member Actions
"""

from civicboom.lib.base import *
from civicboom.controllers.members import _get_member

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

# AllanC - TODO: these SQLAlchemy links should be depricated in preference to actual content searchs
content_lists = {
    'content'             : lambda member: member.content ,
    'content_public'      : lambda member: member.content_public ,
    'assignments_active'  : lambda member: member.content_assignments_active ,
    'assignments_previous': lambda member: member.content_assignments_previous,
    'assignments'         : lambda member: member.content_assignments ,
    'articles'            : lambda member: member.content_articles ,
    'drafts'              : lambda member: member.content_drafts ,
    #'accepted_assignments': lambda member: member.accepted_assignments ,
}


class MemberActionsController(BaseController):

    #-----------------------------------------------------------------------------
    # Actions
    #-----------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def follow(self, id, format="html"):
        """
        POST /members/{name}/follow: follow the member

        @api members 1.0 (WIP)

        @return 200   following ok
        @return 500   error following
        """
        status = c.logged_in_user.follow(id)
        if status == True:
            return action_ok(_('You are now following %s') % id)
        raise action_error(_('Unable to follow member: %s') % status)


    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def unfollow(self, id, format="html"):
        """
        POST /members/{name}/unfollow: unfollow the member

        @api members 1.0 (WIP)

        @return 200   unfollowing ok
        @return 500   error unfollowing
        """
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        raise action_error(_('Unable to stop following member: %s') % status)


    #-----------------------------------------------------------------------------
    # View
    #-----------------------------------------------------------------------------

    @auto_format_output
    @web_params_to_kwargs
    def followers(self, id, **kwargs):
        """
        GET /members/{name}/followers: get a list of followers
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.followers]})


    @auto_format_output
    @web_params_to_kwargs
    def following(self, id, **kwargs):
        """
        GET /members/{name}/following: get a list of members the user is following
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.following]})


    @auto_format_output
    @web_params_to_kwargs
    def content(self, id, **kwargs):
        """
        GET /members/{name}/content: get a list content (including private if current user)
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        @param list what type of contents to return, possible values:
          content
          assignments_active
          assignments_previous
          assignments
          articles
          drafts

        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        """
        if 'list' not in kwargs:
            kwargs['list'] = 'content'
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = 'creator'
        
        member = _get_member(id)
        
        # AllanC - I dont like this ...
        #          we want people to be able to filter the lists from the API ... but as we just call the SQLAlchemy links we cant tell what data is public or private
        #          we need a more sophisticated method of doing this, maybe leveraging a new search with public=true
        #          content_lists (above) should be refactored?
        if member != c.logged_in_user:
            kwargs['list'] = 'content_public'
        
        list = kwargs['list']
        if list not in content_lists:
            raise action_error(_('list type %s not supported') % list, code=400)
            
        contents = content_lists[list](member)
        contents = [content.to_dict(**kwargs) for content in contents]
        
        return action_ok(data={'list': contents})