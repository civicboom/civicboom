<!DOCTYPE html>
<%
    
    self.link_back = None
    self.link_next = None
%>
% if hasattr(self, 'init_vars'):
    ${self.init_vars()}
% endif
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
            <%
                from glob import glob
                css_mobile = glob("civicboom/public/styles/mobile/*.css")
                css_all    = css_mobile
                css_all    = [n[len("civicboom/public/"):] for n in css_all]
                css_all.sort()
            %>
            % for css in css_all:
            <link rel="stylesheet" type="text/css" href="${h.wh_url("public", css)}" />
            % endfor
        % else:
            <link rel="stylesheet" type="text/css" href="${h.wh_url("public", "styles/mobile.css")}" />
        % endif

        ##----------------------------------------------------------------------
        ## Javascript
        ##----------------------------------------------------------------------
        % if config['development_mode']:
            ## AllanC - Please note the order of these JS files should match the order in /public/javascript/Makefile to reduce potential errors with loading dependencys between the live and development sites
            <%
                js_all =[
                    '/javascript/jquery-1.6.2.js',
                    '/javascript/jquery.mobile-1.0b3.js',
                ]
            %>
            % for js in js_all:
            ##<script type="text/javascript" src="${h.wh_url("public", js)}"></script>
            <script type="text/javascript" src="${js}"></script>
            % endfor
        % else:
            <script type="text/javascript" src="${h.wh_url("public", "javascript/_combined.mobile.js")}"></script>
        % endif
        
        ##----------------------------------------------------------------------
        ## Javascript - init
        ##----------------------------------------------------------------------
        <script type="text/javascript">
            $(document).bind("mobileinit", function(){
                // Sets defaults for jquery mobile
                $.mobile.page.prototype.options.degradeInputs.date = 'text';
                $.mobile.defaultDialogTransition    = 'fade';
                // $.mobile.ajaxEnabled = false;
                $.mobile.selectmenu.prototype.options.nativeMenu = false;
            });
            
            $(document).bind("pagecreate", function() {
                // Little hacky, tell any forms created not to ajax submit
                $('form').attr('data-ajax', 'false');
            });
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

<%def name="page()">
    <div data-role="page" data-theme="b" \
        % if hasattr(caller, 'page_id'):
        id="${caller.page_id()}" \
        % endif
        % if hasattr(caller, 'page_class'):
        class="${caller.page_class()}" \
        % endif
    >
        % if hasattr(caller, 'header'):
        <div data-role="header" data-position="inline" data-id="page_header" data-theme="b">
            ${caller.header()}
        </div>
        % endif
        <div data-role="content">
            ${caller.content()}
        </div>
        % if hasattr(caller, 'footer'):
        <div data-role="footer" data-position="fixed" data-fullscreen="true">
            ${caller.footer()}
        </div>
        % endif
    </div>
</%def>




<%def name="header()">
    <div class="header">
        % if self.link_back:
            <a href="${self.link_back}" class="back_link" data-direction="reverse">
                <span><</span>
            </a>
        % endif
        <a href="/" rel="external">
            <img class='logo_img' src='${h.wh_url("public", "images/logo-v3-128x28.png")}' alt='${_("_site_name")}' />
        </a>
        % if self.link_next:
            <a href="${self.link_next}" class="next_link">
                <span>></span>
            </a>
        % endif
        <div class="separator"></div>
    </div>
    
    % if hasattr(self, 'control_bar'):
    ${self.control_bar()}
    % else:
    <div data-role="navbar" class="ui-navbar">
        <ul>
            % if c.logged_in_user:
            <li>
                <a href="${h.url(controller='profile', action='index')}" rel="external">Profile</a>
            </li>
            % endif
            <li>
                <a href="${h.url(controller='contents', action='index')}" rel="external">Explore</a>
            </li>
        </ul>
    </div>
    % endif
</%def>

<%def name="footer()">
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
