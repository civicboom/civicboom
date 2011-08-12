<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%!
    import copy
%>

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
        ${components.header(title="Explore members")}
        
        <div data-role="content">
            ${content_main(self.list)}
        </div>
        
        <div data-role="footer" data-position="fixed" data-fullscreen="true">
            ${pagination()}
        </div>
    </div>
</%def>

<%def name="content_main(list)">
    ${components.search_form()}
    ${list_includes.list_members(list)}
</%def>

##-----------------------------------------------------------------------------
## Render a navbar containing next/previous links for index lists
##-----------------------------------------------------------------------------
<%def name="pagination()">
    <%
        args, kwargs = c.web_params_to_kwargs
        kwargs = copy.copy(kwargs)
        if 'format' in kwargs:
            del kwargs['format']
        offset = self.list['offset']
        limit  = self.list['limit']
        count  = self.list['count']
        items  = len(self.list['items'])
    %>
    
    <div data-role="navbar" class="ui-navbar">
        <ul>
        % if offset > 0:
            <li>
                <% kwargs['offset'] = offset - limit %>
                <a href="${h.url('current', format='html', **kwargs)}" class="prev" data-direction="reverse">${_("Previous")}</a>
            </li>
        % endif
        % if offset + items < count:
            <li>
                <% kwargs['offset'] = offset + limit %>
                <a href="${h.url('current', format='html', **kwargs)}" class="next">${_("Next")}</a>
            </li>
        % endif
        </ul>
    </div>
</%def>