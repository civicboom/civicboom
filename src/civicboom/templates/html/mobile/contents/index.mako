<%inherit file="/html/mobile/common/lists.mako"/>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />

<%def name="page_title()">
    ${_("Explore _content")}
</%def>

<%def name="body()">
    <%
        self.list = d['list']
    %>

    <div data-role="page" data-theme="b" id="explore_content" class="">
        ${components.header(title="Explore contents")}
        
        <div data-role="content">
            ${content_main(self.list)}
        </div>
        
        ${parent.pagination()}
    </div>
</%def>

<%def name="content_main(list)">
    ${components.search_form()}
    ${parent.list_contents(list, "woo")}
</%def>