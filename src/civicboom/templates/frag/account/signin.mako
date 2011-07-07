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
    <style>
        .content_why {
            font-size: 150%;
            margin: 1em auto 1em 0.5em;
        }
        .content_mobile {
            font-size: 150%;
            margin: 1em auto 0 0.5em;
            padding-top: 1em;
        }
        .content_mobile .left-col {
            float: left;
            width: 17.5em;
            padding-top: 2em;
        }
        .content_mobile .right-col {
            float: right;
        }
        .content_mobile a img {
            width: 8em;
        }
        .frag_col .frag_signin p {
            font-size: 150%;
        }
    </style>
    <div class="frag_top_row">
    <div class="frag_col frag_signin">
        <div class="frag_list">
    % if hasattr(c, 'action_objects'):
        ## Approved actions
        
        ## Accept
        % if   c.action_objects['action'] == 'accept':
            <%
                assignment   = c.action_objects['action_object']['content']
                creator_name = assignment['creator']['name'] or assignment['creator']['username']
                content_title = assignment['title'] or None
            %>
            ## AllanC: TODO - internationalise this string!
            ${content_why(creator_name, content_title, assignment)}
            ## <p>By signing  in/up you will accept the <b>${assignment['title']}</b> request that has been set by <b>${creator_name}</b></p>
            
        ## Follow
        % elif c.action_objects['action'] == 'follow':
            <%
                member      = c.action_objects['action_object'].get('member')
                member_name = member['name']
            %>
            ##<p>By signing in/up you will follow <b>${member_name}</b> </p>
            ${content_why(member_name)}
            
        % elif c.action_objects['action'] == 'boom':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            ## AllanC: TODO - internationalise this string!
            ${content_why(creator_name)}
            ## <p>By signing in/up you will Boom the _content <b>${content['title']}</b> by <b>${creator_name}</b></p>
        %elif  c.action_objects['action'] == 'new_respose':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            ${content_why(creator_name)}
            ## <p>By signing in/up you will respond to the _assignment <b>${content['title']}</b> by <b>${creator_name}</b></p>
        %elif  c.action_objects['action'] == 'comment':
            <%
                content       = c.action_objects['action_object'].get('content')
            %>
            ## <p>By signing in/up you make a comment on <b>${content.get('title')}</b> </p>
        %elif  c.action_objects['action'] == 'new_article':
            <%
            %>
            <p>By signing in/up you will ${c.action_objects['description']}</p>
        % endif

        ##${c.action_objects['description']}
        ##${c.action_objects['action_object']}
        <br/>
    % endif
    
        <table>
            <tr>
                <td style="padding-right: 1em;">${signin.signin()}</td>
                <td>${signin.signup()}</td>
                <div style="padding: 0.5em;"></div>
            </tr>
            
            <tr>
                <td colspan="2">
                    ${signin.janrain()}
                </td>
            </tr>
        </table>
        ${signin.forgot()}
        ## ${content_mobile()}
        <div class="separator"></div>
    </div>
    </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Signin Fragment
##------------------------------------------------------------------------------
<%def name="content_why(creator_name=None, content_title=None, content=None)">
    <div class="content_why">
        <h1>Get involved!</h1>
        <p>Sign in/up and respond NOW to <b>${creator_name}
        % if content_title:
            's ${content_title}
        % endif
        </b> and:</p><br />
        <ol>
            <li>Get published!</li>
            <li>Get recognition!</li>
            <li>Help ${creator_name} build a news community!</li>
        </ol>
    </div>
</%def>

<%def name="content_mobile()">
    <div class="content_mobile">
        <div class="left-col">Did you know you can also respond with your Android phone?</div>
        <div class="right-col"><a href="${url(controller='misc', action='about', id='mobile')}"><img src="/images/about/qr_mobile2.png" style="float: right;"></a></div>
    </div>
    
</%def>