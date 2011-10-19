<!DOCTYPE html>
<html>
    <head>
        <%def name="title()"></%def>
        <title>${_('_site_name Mobile')}: ${self.title()}</title>
        
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <link rel="shortcut icon" href="/images/boom16.ico" />
        
        ##----------------------------------------------------------------------
        ## CSS
        ##----------------------------------------------------------------------
        % if config['development_mode']:
            <style type="text/css">
                <%
                    css_all = h.css_files('mobile', include_common=False)
                %>
                % for css in css_all:
                @import url("${h.wh_url("public", css)}");
                % endfor
            </style>
        % else:
            <link rel="stylesheet" type="text/css" href="${h.wh_url("public", "styles/mobile.css")}" />
        % endif

        ##----------------------------------------------------------------------
        ## Javascript
        ##----------------------------------------------------------------------
        % if config['development_mode']:
            <%
                # AllanC - Please note the order of these JS files should match the order in /public/javascript/Makefile to reduce potential errors with loading dependencys between the live and development sites
                js_all =[
                    'javascript/jquery-1.6.2.js',
                    'javascript/jquery.mobile.cb_settings.js',
                    'javascript/jquery.mobile-1.0rc1.js',
                    'javascript/geo.js',
                ]
            %>
            % for js in js_all:
            <script type="text/javascript" src="${h.wh_url("public", js)}"></script>
            % endfor
        % else:
            <script type="text/javascript" src="${h.wh_url("public", "javascript/_combined.mobile.js")}"></script>
        % endif
        <script type="text/javascript">
            $.fixedToolbars.setTouchToggleEnabled(false);
        </script>
    </head>
  
    <body class="c-${c.controller} a-${c.action}">
        ##${self.flash_message()}
        ${next.body()}
    </body>
</html>





##------------------------------------------------------------------------------
## Templates
##------------------------------------------------------------------------------
<%doc>
<%def name="page()">
    <div data-role="page" data-theme="b" ${caller.page_attr()}>
        ${caller.body()}
        % if hasattr(caller, 'page_header'):
        <div data-role="header" data-position="inline" data-id="page_header" data-theme="b">
            ${caller.page_header()}
        </div>
        % endif
        <div data-role="content">
            ${caller.page_content()}
        </div>
        % if hasattr(caller, 'page_footer'):
        <div data-role="footer" \
            % if hasattr(caller, 'footer_attr'):
                ${caller.header_attr()}
            % else:
                data-position="fixed" data-fullscreen="true" \
            % endif
        >
            ${caller.page_footer()}
        </div>
        % endif
    </div>
</%def>
</%doc>



<%def name="header(title=None, link_back=None, link_next=None, nav_bar=None)">
    <div data-role="header" data-position="inline" data-id="page_header" data-theme="b">
        <div class="header">
            % if link_back:
                <a href="${link_back}" class="back_link" data-direction="reverse">
                    <span><</span>
                </a>
            % endif
            <a href="/" rel="external">
                <img class='logo_img' src='${h.wh_url("public", "images/logo-v3-128x28.png")}' alt='${_("_site_name")}' />
            </a>
            % if link_next:
                <a href="${link_next}" class="next_link">
                    <span>></span>
                </a>
            % endif
            <div class="separator"></div>
        </div>
        
        % if callable(nav_bar):
            <div data-role="navbar" class="ui-navbar">
                <ul>
                    ${nav_bar()}
                </ul>
            </div>
        % endif
        
    </div>
</%def>

<%def name="footer()">
    <div data-role="footer" data-id="nav" data-position="fixed">
		<div data-role="navbar">
			<ul>
                <li><a data-icon="search" href="${h.url('contents')                                   }" rel="external">Explore</a></li>
                % if c.logged_in_persona:
                <li><a data-icon="info"   href="${h.url('contents')                                   }" rel="external">Feeds</a></li>
                <%
                    num_messages = c.logged_in_persona.num_unread_messages + c.logged_in_persona.num_unread_notifications
                    if not num_messages:
                        num_messages = ''
                %>
				<li><a data-icon="alert"  href="${h.url(controller='profile', action="index")}#messages" rel="external">${num_messages} Messages</a></li>
                <li><a data-icon="home"   href="${h.url(controller='profile', action="index")         }" rel="external">Profile</a></li>
                % else:
                <li><a data-icon="search" href="${h.url(controller='account', action='signin')        }" rel="external">Signin</a></li>
                % endif
                ##class="ui-btn-active ui-state-persist"
			</ul>
		</div><!-- /navbar -->
	</div><!-- /footer -->
</%def>

<%def name="flash_message()">
    <h3 id="flash_message" class="status_${c.result['status']}">${c.result['message']}</h3>
    % if c.result['message'] != "":
    <script type="text/javascript">    
        <% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
        ## AllanC is json_message actually used here? is this needed?
    </script>
    % endif
</%def>



##-----------------------------------------------------------------------------
## Create a swipe event catcher to change to the given page
##-----------------------------------------------------------------------------
<%def name="swipe_event(anchor, to, direction='')">
    <script type="text/javascript">
        $('${anchor}').live('swipe${direction}', function(event) {
            $.mobile.changePage($('${to}'), {
                changeHash: false,
                transition: "slide",
                % if direction == "right":
                    reverse: true,
                % endif
            });
        });
    </script>
</%def>


<%def name="title_logo()">
    <div class="title_logo">
        <a href="${h.url(controller='misc', action='titlepage')}" rel='external'>
            <img class='logo_img' src='${h.wh_url("public", "images/logo-v3-684x150.png")}' alt='${_("_site_name")}' />
        </a>
    </div>
</%def>

<%def name="form_button(action_url, title, method='post')">
    ${h.secure_form(action_url, method=method, data_ajax=False)}
    <input type="submit" value="${title}">
    ${h.end_form()}
</%def>