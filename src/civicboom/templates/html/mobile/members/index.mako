<%inherit file="/html/mobile/common/mobile_base.mako"/>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

<%def name="page_title()">
    ${_("Explore _members")}
</%def>

<%def name="body()">
    <%
        self.list = d['list']
    %>

    <div data-role="page" data-title="${page_title()}" data-theme="b" id="explore_member" class="">
        <div data-role="header" data-position="inline" data-theme="b">
            <h1>Explore members</h1>
        </div>
        
        <div data-role="content">
            ${content_main(self.list)}
        </div>
        
        ${components.control_bar()}
    </div>
</%def>

<%def name="content_main(list)">
    ${components.search_form()}
    ${list_includes.list_members(list, "woo")}
</%def>