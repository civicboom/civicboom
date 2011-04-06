<%inherit file="/frag/common/frag.mako"/>

<%namespace name="signin" file="/html/web/account/signin.mako"/>

##------------------------------------------------------------------------------
##
##------------------------------------------------------------------------------
<%def name="init_vars()">
    <%
        self.attr.title     = _('Sign in or Sign up ')
        self.attr.icon_type = 'boom'
    %>
</%def>

##------------------------------------------------------------------------------
## Signin Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_col frag_signin">
    % if hasattr(c, 'action_objects'):
        ## Approved actions
        
        ## Accept
        % if   c.action_objects['action'] == 'accept':
            <%
                assignment   = c.action_objects['action_object']['content']
                creator_name = assignment['creator']['name'] or assignment['creator']['username']
            %>
            ## AllanC: TODO - internationalise this string!
            <p>By signing  in/up you will accept the <b>${assignment['title']}</b> request that has been set by <b>${creator_name}</b></p>
            
        ## Follow
        % elif c.action_objects['action'] == 'follow':
            <%
                member      = c.action_objects['action_object'].get('member')
                member_name = member['name'] or member['username']
            %>
            ## AllanC: TODO - internationalise this string!
            <p>By signing in/up you will follow <b>${member_name}</b> </p>
            
        % elif c.action_objects['action'] == 'boom':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name'] or content['creator']['username']
            %>
            ## AllanC: TODO - internationalise this string!
            <p>By signing in/up you will Boom the _content <b>${content['title']}</b> by <b>${creator_name}</b></p>
        %elif  c.action_objects['action'] == 'new_respose':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name'] or content['creator']['username']
            %>
            <p>By signing in/up you will respond to the _assignment <b>${content['title']}</b> by <b>${creator_name}</b></p>
        %elif  c.action_objects['action'] == 'comment':
            <%
                content       = c.action_objects['action_object'].get('content')
            %>
            <p>By signing in/up you make a comment on <b>${content.get('title')}</b> </p>
        % endif

        ##${c.action_objects['description']}
        ##${c.action_objects['action_object']}
        <br/>
    % endif
    <table>
        <tr>
            <td style="padding-right: 1em;">${signin.signin()}</td>
            <td>${signin.signup()}</td>
        </tr>
        <tr>
            <td colspan="2">
                ${signin.janrain()}
            </td>
        </tr>
    </table>
    ${signin.forgot()}
    </div>
</%def>