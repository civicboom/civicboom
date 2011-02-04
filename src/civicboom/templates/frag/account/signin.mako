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
    <div class="frag_col">
    % if hasattr(c, 'action_objects'):
        % if c.action_objects['action'] == 'accept':
            <%
                assignment   = c.action_objects['action_object']['content']
                creator_name = assignment['creator']['name'] or assignment['creator']['username']
            %>
            ## AllanC: TODO - internationalise this string!
            <p>By signing in you will accept the <b>${assignment['title']}</b> request that has been set by <b>${creator_name}</b></p>
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