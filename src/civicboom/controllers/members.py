from civicboom.lib.base import *

from civicboom.lib.misc import str_to_int

#from civicboom.controllers.contents import _normalize_member


# AllanC - for members autocomplete index
from civicboom.model    import Member, Follow
from sqlalchemy         import or_, and_
#from sqlalchemy.orm     import join


log      = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Search Filters
#-------------------------------------------------------------------------------

def _init_search_filters():
    
    def append_search_member(query, member):
        #if isinstance(member, Member):
        #    member = member.id
        #try:
        #    return query.filter(Member.id       == int(member))
        #except:
        
        if isinstance(member, basestring):
            return query.filter(Member.username == member                  )
        else:
            return query.filter(Member.id       == normalize_member(member))

    def append_search_name(query, name):
        return query.filter(or_(Member.name.ilike("%"+name+"%"), Member.username.ilike("%"+name+"%")))
    
    def append_search_type(query, type_text):
        return query.filter(Member.__type__==type_text)

    def append_search_location(query, location_text):
        log.warning('member location search not implemented')
        return query

    def append_search_followed_by(query, member):
        member_id = normalize_member(member)
        return query.filter(Member.id.in_( Session.query(Follow.member_id  ).filter(Follow.follower_id==member_id) ))

    def append_search_follower_of(query, member):
        member_id = normalize_member(member)
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
    
        @param member       find this specific member by name
        @param name         find members with names like this (aka 'term' for the autocompleter)
        @param type         'user' or 'group'
        @param location     find members with a public location near to this point
        @param followed_by  find members followed by the specified member
        @param follower_of  find members who are a follower of the specified member
        @param *            (see common list return controls)
    
        @return 200      list ok
                list     array of member objects
        
        @example http://new.civicboom.com/members.json?name=unit
        @example http://new.civicboom.com/members.json?follower_of=1&limit=5
        """
        
        # Autocomplete uses term not name - for ease of migration term is copyed to name if name not present
        if 'term' in kwargs and 'name' not in kwargs:
            kwargs['name'] = kwargs['term']
        
        # Setup search criteria
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
        
        # Sort
        if 'sort' not in kwargs:
            sort = 'name'
        # TODO: use kwargs['sort']
        results = results.order_by(Member.name.asc())
        
        # Count
        count = results.count()
        
        # Limit & Offset
        kwargs['limit']  = str_to_int(kwargs.get('limit'), config['search.default.limit.members'])
        kwargs['offset'] = str_to_int(kwargs.get('offset')                                       )
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        # Return search results
        # Return search results
        return action_ok(
            data = {'list': {
                'items' : [content.to_dict(**kwargs) for content in results.all()] ,
                'count' : count ,
                'limit' : kwargs['limit'] ,
                'offset': kwargs['offset'] ,
                'type'  : 'member' ,
                }
            }
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
        
        @example http://new.civicboom.com/members/1.json
        """
        
        member = get_member(id)
        
        if 'lists' in kwargs:
            lists = [list.strip() for list in kwargs['lists'].split(',')]
        else:
            lists = [
                # Comunity
                'followers',
                'following',
                'groups',
                'members', # if a group and public
                
                # Content
                'drafts',
                'assignments_active',
                'assignments_previous',
                'articles',
                'responses',
                
                # Other
                'assignments_accepted',
                'actions',
                'boomed' ,
            ]
        
        data = {'member': member.to_dict(list_type='full', **kwargs)}
        
        # Imports
        # AllanC - cannot be imported at begining of module because of mutual coupling error
        from civicboom.controllers.contents       import ContentsController, list_filters
        from civicboom.controllers.member_actions import MemberActionsController
        contents_controller       = ContentsController()
        member_actions_controller = MemberActionsController()
        
        # Content Lists
        for list in [list for list in lists if list in list_filters.keys()]:
            data[list] = contents_controller.index(creator=member.username, list=list, limit=config['search.default.limit.sub_list'], **kwargs)['data']['list']
        
        # Member Lists
        for list in [list for list in lists if hasattr(member_actions_controller, list)]:
            data[list] = getattr(member_actions_controller, list)(member, **kwargs)['data']['list']
        
        return action_ok(data=data)
