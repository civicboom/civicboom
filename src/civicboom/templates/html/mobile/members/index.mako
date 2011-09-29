<%inherit file="/html/mobile/common/lists.mako"/>

<%def name="init_vars()">
<%
    self.title      = _("Explore _users and _groups")
    self.page_id    = "explore_member"
%>
</%def>


<%def name="body()">
    ${parent.generate_list(d['list'], member_li, title=_('Members'), more=None)}
</%def>


##------------------------------------------------------------------------------
## Generate a single li element for the given member
##------------------------------------------------------------------------------
<%def name="member_li(item)">
    <li>
        <a href="${h.url('member', id=item['username'])}" title="${item['name']}" rel="external">
            <img src="${item['avatar_url']}" class="thumbnail" />
            <h3>
                ${item['name']}
                % if item.get('type') == "group":
                    <small><b> [${_("_Group")}]</b></small>
                % endif
            </h3>
            % if item.get('username'):
                <p>${item['username']}</p>
            % endif
            % if item.get('num_followers') != None:
                <p><b>${item['num_followers']}</b> followers</p>
            % endif
        </a>
    </li>
</%def>
