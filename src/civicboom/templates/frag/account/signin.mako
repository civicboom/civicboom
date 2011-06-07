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
                member_name = member['name']
            %>
            ## AllanC: TODO - internationalise this string!
            <p>By signing in/up you will follow <b>${member_name}</b> </p>
            
        % elif c.action_objects['action'] == 'boom':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            ## AllanC: TODO - internationalise this string!
            <p>By signing in/up you will Boom the _content <b>${content['title']}</b> by <b>${creator_name}</b></p>
        %elif  c.action_objects['action'] == 'new_respose':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
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
        <style>
            .content_why {
                font-size: 150%;
                margin: 5em auto 0 0.5em;
            }
            .content_mobile {
                font-size: 150%;
                margin: 2em auto 0 0.5em;
            }
            .content_mobile img {
                display: inline-block;
            }
        </style>
        <div class="content_why">
            <h1>Why get involved?</h1>
            <p>You can help <b>${creator_name}</b> in:</p>
            <ol>
                <li>Stuff!</li>
                <li>More stuff!</li>
                <li>Even more stuff!</li>
            </ol>
        </div>
        <div class="content_mobile">
            Did you know you can also respond with your Android phone?
            <a href="http://market.android.com/details?id=com.civicboom.mobile2"><img src="/images/about/qr_mobile2.png" style="float: right;"></a>
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Signin Fragment
##------------------------------------------------------------------------------
<%def name="content_why()">
    <div class="content_why">
        <h1>Why get involved?</h1>
        <p>You can help <b>${creator_name}</b> in:</p>
        <ol>
            <li>Stuff!</li>
            <li>More stuff!</li>
            <li>Even more stuff!</li>
        </ol>
    </div>
    <div class="content_mobile">
        Did you know you can also respond with your Android phone?
    </div>
</%def>