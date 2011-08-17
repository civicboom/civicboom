<%inherit file="/html/mobile/common/lists.mako"/>

<%!
    import copy
%>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

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
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="messages" class="messages">
        ${components.header()}
        
        <div data-role="content">
            ${list_includes.list_messages(self.list, self.type)}
        </div>
        
        ${parent.pagination()}        
    </div>
</%def>

<%def name="page_title()">
    something
</%def>