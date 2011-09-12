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
    ${_("Messages")}
</%def>

<%def name="body()">
    <%   
        self.list =     d['list']
        self.messages = self.list['items']
        self.count =    self.list['count']
        self.type =     self.list['type']
        if self.list['kwargs'].get('list'):
            self.list['kwargs']['list']
    %>
    
    ## Main member detail page (username/description/etc)
    <div data-role="page" data-theme="b" id="messages" class="messages">
        ${components.header()}
        
        <div data-role="content">
            ${parent.flash_message()}
            % if self.count:
                ${parent.list_messages(self.list, self.type)}
            % else:
                <p>You have no ${title or list['type']}</p>
                <p><a href="${h.url(controller='profile', action='index')}" rel="external">Return to profile</a></p>
            % endif
        </div>
        
        ${parent.pagination()}
    </div>
</%def>