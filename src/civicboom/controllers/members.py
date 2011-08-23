from civicboom.lib.base import *

#from civicboom.controllers.contents import _normalize_member

from cbutils.misc import update_dict
import re

# AllanC - for members autocomplete index
from civicboom.model      import Member, Follow, GroupMembership, Group
from sqlalchemy           import or_, and_, null, not_
from sqlalchemy.orm       import join, joinedload, defer


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

    def append_search_name(query, text):
        if not text:  # o_O
            return query

        parts = []
        for word in text.split():
            word = re.sub("[^a-zA-Z0-9_-]", "", word)
            if word:
                parts.append(word)

        if parts:
            text = " | ".join(parts)
            return query.filter("""
                to_tsvector('english', username || ' ' || name || ' ' || description) @@
                to_tsquery(:text)
            """).params(text=text)
        else:
            return query

    def append_search_username(query, username_text):
        if username_text:
            return query.filter(Member.username==username_text)
        return query

    def append_search_type(query, type_text):
        if type_text:
            return query.filter(Member.__type__==type_text)
        return query

    def append_search_location(query, location_text):
        log.warning('member location search not implemented')
        return query

    def append_exclude_members(query, members):
        if not members:
            return query
        if isinstance(members, basestring):
            members = [member.strip() for member in members.split(',')]
        return query.filter(not_(Member.username.in_(members)))

    def append_search_group_join_mode(query, join_mode):
        return query.filter(Member.__type__=='group').filter(Group.join_mode==join_mode)

    def append_search_group_default_content_visibility(query, default_content_visibility):
        return query.filter(Member.__type__=='group').filter(Group.default_content_visibility==default_content_visibility)

    def append_search_followed_by(query, member):
        member_id = normalize_member(member)
        return query.filter(Member.id.in_( Session.query(Follow.member_id  ).filter(Follow.follower_id==member_id).filter(Follow.type!='trusted_invite') ))

    def append_search_follower_of(query, member):
        member_id = normalize_member(member)
        return query.filter(Member.id.in_( Session.query(Follow.follower_id).filter(Follow.member_id  ==member_id).filter(Follow.type!='trusted_invite') ))


    search_filters = {
        'member'         : append_search_member      ,
        'name'           : append_search_name        ,
        'username'       : append_search_username    ,
        'type'           : append_search_type        ,
        'location'       : append_search_location    ,
        'exclude_members': append_exclude_members    ,
        'group_join_mode': append_search_group_join_mode ,
        'default_content_visibility': append_search_group_default_content_visibility,
        #'followed_by'  : append_search_followed_by ,
        #'follower_of'  : append_search_follower_of ,
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
        @param exculde_members comma separated list of usernames to exclude from the return
        @param sort         comma separated list of fields, prefixed by '-' for decending order (default) '-id' 
        @param *            (see common list return controls)
    
        @return 200      list ok
                list     array of member objects
        @return 404      members_of=user is not a group
        
        @example https://test.civicboom.com/members.json?name=unit
        @example https://test.civicboom.com/members.json?follower_of=1&limit=5
        """
        # Autocomplete uses term not name - for ease of migration term is copyed to name if name not present
        if 'term' in kwargs and 'name' not in kwargs:
            kwargs['name'] = kwargs['term']
        
        # Setup search criteria
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
        
        list_to_dict_transform = None

        if 'members_of' in kwargs or 'groups_for' in kwargs:
            results = Session.query(GroupMembership)
            
            if 'members_of' in kwargs:
                results = results.options(joinedload(GroupMembership.member))
                
                # Get Group
                group   = get_group(kwargs['members_of'])
                # Permissions - only show member roles if part of this group
                if group.member_visibility=="public" or group == c.logged_in_persona or group.get_membership(c.logged_in_persona):
                    results = results.filter(GroupMembership.group_id==normalize_member(group))
                else:
                    results = None

                # to_dict transform
                def member_roles_to_dict_transform(results, **kwargs):
                    return [update_dict(member_role.member.to_dict(**kwargs),{'role':member_role.role, 'status':member_role.status}) for member_role in results]
                list_to_dict_transform = member_roles_to_dict_transform
                
            elif 'groups_for' in kwargs:
                results = results.select_from(join(Group, GroupMembership, GroupMembership.group))
                results = results.options(joinedload(GroupMembership.group))
                
                # Get Member
                member = get_member(kwargs['groups_for'])
                results = results.filter(GroupMembership.member_id==normalize_member(member))
                # Permissions - only show membership of public groups
                if member == c.logged_in_persona and kwargs.get('private', False):
                    pass
                else:
                    results = results.filter(GroupMembership.status  == 'active')
                    results = results.filter(Group.member_visibility == 'public')

                # to_dict transform
                def group_roles_to_dict_transform(results, **kwargs):
                    return [update_dict(group_role.group.to_dict(**kwargs), {'role':group_role.role, 'status':group_role.status}) for group_role in results]
                list_to_dict_transform = group_roles_to_dict_transform
                
            
        elif 'follower_of' in kwargs or 'followed_by' in kwargs:
            member  = get_member(kwargs.get('follower_of') or kwargs.get('followed_by'))
            results = Session.query(Follow)
            
            if 'followed_by' in kwargs:
                results.options(joinedload(Follow.member))
                results = results.filter(Follow.follower==member)

                def me_followed_by_to_dict_transform(results, **kwargs):
                    return [update_dict(follow.member.to_dict(**kwargs), {'follow_type':follow.type}) for follow in results]

                def followed_by_to_dict_transform(results, **kwargs):
                    return [follow.member.to_dict(**kwargs) for follow in results]

                if member == c.logged_in_persona:
                    list_to_dict_transform = me_followed_by_to_dict_transform
                else:
                    list_to_dict_transform = followed_by_to_dict_transform
                
            if 'follower_of' in kwargs:
                results.options(joinedload(Follow.follower))
                results = results.filter(Follow.member==member)

                def me_follower_of_to_dict_transform(results, **kwargs):
                    return [update_dict(follow.follower.to_dict(**kwargs), {'follow_type':follow.type}) for follow in results]

                def follower_of_to_dict_transform(results, **kwargs):
                    return [follow.follower.to_dict(**kwargs) for follow in results]

                if member == c.logged_in_persona:
                    list_to_dict_transform = me_follower_of_to_dict_transform
                else:
                    list_to_dict_transform = follower_of_to_dict_transform
            
            if member != c.logged_in_persona:
                results = results.filter(Follow.type!='trusted_invite')
            
            #select_from(join(User, Address, User.addresses))

        else:
            results = Session.query(Member)
            # TODO
            if 'group_join_mode' in kwargs: #AllanC - was if False: so I bolted my group_join_mode hack on :( ... HACK ... # Could - if fields in include_fields are in User or Group only
                results = results.with_polymorphic('*')
            results = results.filter(Member.status=='active')
            for key in [key for key in search_filters if key in kwargs]: # Append filters to results query based on kwarg params
                results = search_filters[key](results, kwargs[key])
        
            # Sort
            for sort_field in kwargs.get('sort', '-id').split(','):
                if sort_field[0] == "-":
                    results = results.order_by(getattr(Member, sort_field[1:]).desc())
                else:
                    results = results.order_by(getattr(Member, sort_field    ).asc() )
            
        # NOOO!! ... this should be at the end ... and sort all fields ... but this is cant be done with Follow objects ... rarara ... bollox

        
        # Could be a much better way of doing the above
        # http://lowmanio.co.uk/blog/entries/postgresql-full-text-search-and-sqlalchemy/
        # The link has some tips as how to use add_colums - it is very lightly documented in SQLA docs        
        
        
        return to_apilist(results, obj_type='members', list_to_dict_transform=list_to_dict_transform, **kwargs)



    @web
    def show(self, id, **kwargs):
        """
        GET /members/{name}: Show a specific item
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                member   member object
        @return 404      member not found
        
        @example https://test.civicboom.com/members/1.json
        """
        
        member = get_member(id)

        if member and id.isdigit() and int(member.id) == int(id):
            return redirect(url('member', id=member.username))
        
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
                'assignments_accepted', # AllanC - see limit imposed below
                'actions',
                'boomed' ,              # AllanC - see limit imposed below
            ]
        
        data = {'member': member.to_dict(list_type='full', **kwargs)}
        
        # Imports
        # AllanC - cannot be imported at begining of module because of mutual coupling error
        from civicboom.controllers.contents       import ContentsController, list_filters
        from civicboom.controllers.member_actions import MemberActionsController
        contents_controller       = ContentsController()
        member_actions_controller = MemberActionsController()
        
        # Content Lists
        for list in [list for list in lists if list in list_filters]:
            data[list] = contents_controller.index(creator=member.username, list=list, limit=config['search.default.limit.sub_list'], **kwargs)['data']['list']
            lists.remove(list) # AllanC - fix; don't allow the same lists to be got from both content and member controller
        
        # Member Lists
        for list in [list for list in lists if hasattr(member_actions_controller, list)]:
            limit = None
            if list in ['boomed', 'assignments_accepted']: # AllanC - we dont want to limit member lists, but we do want to limit content lists to 3
                limit = config['search.default.limit.sub_list']
            data[list] = getattr(member_actions_controller, list)(member, limit=limit, **kwargs)['data']['list']
        
        return action_ok(data=data)
