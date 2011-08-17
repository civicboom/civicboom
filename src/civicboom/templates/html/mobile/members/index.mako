<%inherit file="/html/mobile/common/lists.mako"/>

<%!
    import copy
%>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />

<%def name="page_title()">
    ${_("Explore _members")}
</%def>

<%def name="body()">
    <%
        self.list = d['list']
    %>

    <div data-role="page" data-theme="b" id="explore_member" class="">
        ${components.header(title="Explore members")}
        
        <div data-role="content">
            ${content_main(self.list)}
        </div>
        
        <div data-role="footer" data-position="fixed" data-fullscreen="true">
            ${parent.pagination()}
        </div>
    </div>
</%def>

<%def name="content_main(list)">
    ${components.search_form()}
    ${parent.list_members(list)}
</%def>