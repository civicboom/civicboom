<%namespace name="member_includes"  file="/web/common/member.mako"  />
##<%namespace name="content_includes" file="/web/common/content_list.mako"/>

<%namespace name="frag_list" file="/frag/common/frag_lists.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
${frag_member(d)}
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="frag_member(d)">
    <% member = d['member'] %>
    
    <div class="action_bar">
        ${action_bar(d['actions'])}
    </div>
    
    <div class="frag_data frag_member">
        <div class="frag_left_col">
            ## Member Details
            ${member_avatar(member)}
            ${member_map(  member)}
        </div>
        <div class="frag_right_col">
            ## Member Content
            ${frag_list.member_list( d['following']           , _('Following')             )}
            ${frag_list.member_list( d['followers']           , _('Followers')             )}
            ${frag_list.content_list(d['assignments_accepted'], _('Accepted _assignments') )}
            ${frag_list.content_list(d['content']             , _('Content')               )}
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar(member)">
    <div class="avatar">
        ${member_includes.avatar(member , show_name=True, show_follow_button=True, class_='large')}
    </div>
</%def>



##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="member_map(member)">

</%def>



##------------------------------------------------------------------------------
## Action Bar
##------------------------------------------------------------------------------
<%def name="action_bar(actions)">
    <p><a href='${url(controller='misc', action='widget_preview')}'>widget preview</a></p>
</%def>



##------------------------------------------------------------------------------
## 
##------------------------------------------------------------------------------
<%def name="member_(member)">

</%def>

