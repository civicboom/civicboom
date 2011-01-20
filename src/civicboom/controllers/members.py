from civicboom.lib.base import *

from civicboom.controllers.contents import _normalize_member


# AllanC - for members autocomplete index
from civicboom.model    import Member, Follow
from sqlalchemy         import or_, and_
#from sqlalchemy.orm     import join


log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_member(member):
    """
    Shortcut to return a member and raise not found automatically (as these are common opertations every time a member is fetched)
    """
    member = get_member(member)
    if not member:
        raise action_error(_("member not found"), code=404)
    return member

#-------------------------------------------------------------------------------
# Search Filters
#-------------------------------------------------------------------------------

def _init_search_filters():
    
    def append_search_member(query, member):
        if isinstance(member, Member):
            member = member.id
        try:
            return query.filter(Member.id       == int(member))
        except:
            return query.filter(Member.username == member     )

    def append_search_name(query, name):
        return query.filter(or_(Member.name.ilike("%"+name+"%"), Member.username.ilike("%"+name+"%")))
    
    def append_search_type(query, type_text):
        return query.filter(Member.__type__==type_text)

    def append_search_location(query, location_text):
        log.warning('member location search not implemented')
        return query

    def append_search_followed_by(query, member):
        member_id = _normalize_member(member, always_return_id=True)
        return query.filter(Member.id.in_( Session.query(Follow.member_id  ).filter(Follow.follower_id==member_id) ))

    def append_search_follower_of(query, member):
        member_id = _normalize_member(member, always_return_id=True)
        return query.filter(Member.id.in_( Session.query(Follow.follower_id).filter(Follow.member_id  ==member_id) ))

    search_filters = {
        'member'       : append_search_member      ,
        'name'         : append_search_name        ,
        'type'         : append_search_type        ,
        'location'     : append_search_location    ,
        'followed_by'  : append_search_followed_by ,
        'follower_of'  : append_search_follower_of ,
    }
    
    return search_filters

search_filters = _init_search_filters()

#-------------------------------------------------------------------------------
# Members Controler
#-------------------------------------------------------------------------------

class MembersController(BaseController):
    """
    @title Members
    @doc members
    @desc REST Controller styled on the Atom Publishing Protocol
    """


    @web
    def index(self, **kwargs):
        """
        GET /members: Show a list of members
        
        @api members 1.0 (WIP)
    
        @param list    type of list to get
               all     all members (useful with "term")
        @param term    filter results
        @param * (see common list return controls)
    
        @return 200      list ok
                members  array of member objects
        """
        #def (, list='all', term=None,
        #result = []
        #if list == "all":
        #    result = Session.query(Member)
        #if term:
        #    result = result.filter(or_(Member.name.ilike("%"+term+"%"), Member.username.ilike("%"+term+"%")))
        #return action_ok(data={"list": [m.to_dict(**kwargs) for m in result]})
        
        # Autocomplete uses term not name - for ease of migration term is copyed to name if name not present
        if 'term' in kwargs and 'name' not in kwargs:
            kwargs['name'] =  kwargs['term']
        
        # Setup search criteria
        if 'limit' not in kwargs: #Set default limit and offset (can be overfidden by user)
            kwargs['limit'] = config['search.default.limit']
        if 'offset' not in kwargs:
            kwargs['offset'] = 0
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ""
        
        results = Session.query(Member)
        results = results.filter(Member.status=='active')
        if False: # if fields in include_fields are in User or Group only
            results = results.with_polymorphic('*')
        
        for key in [key for key in search_filters.keys() if key in kwargs]: # Append filters to results query based on kwarg params
            results = search_filters[key](results, kwargs[key])
        
        results = results.order_by(Member.name.asc())
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        # Return search results
        return action_ok(
            data = {'list': [member.to_dict(**kwargs) for member in results.all()]} ,
        )


    @web
    def show(self, id, **kwargs):
        """
        GET /members/{id}: Show a specific item
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                member   member object
        @return 404      member not found
        """
        member = _get_member(id)
        
        if 'lists' not in kwargs:
            kwargs['lists'] = 'followers, following, assignments_accepted, content, groups, members, actions, boomed_content'
        
        data = {'member': member.to_dict(list_type='full', **kwargs)}

        # AllanC - cannot be imported at begining of module because of mutual coupling error
        from civicboom.controllers.member_actions import MemberActionsController
        member_actions_controller = MemberActionsController()
        
        for list in [list.strip() for list in kwargs['lists'].split(',')]:
            if hasattr(member_actions_controller, list):
                data[list] = getattr(member_actions_controller, list)(member, **kwargs)['data']['list']
        
        return action_ok(data=data)





# AllanC - Depricated old stuff?

#index_lists = {
#    'following'             : lambda member: member.following ,
#    'followers'             : lambda member: member.followers ,
#     'assignments_accepted': lambda member: member.assignments_accepted , 
#}


    #@auto_format_output
    #@authorize
    #def index(self, list=None):
    #    member_list_name = request.params.get('list', list)
    #    if member_list_name not in index_lists: raise action_error(_('list type %s not supported') % member_list_name)
    #    members = index_lists[member_list_name](c.logged_in_persona)
    #    members = [member.to_dict('default_list') for member in members]
    #    
    #    return {'data': {'list': members}}
