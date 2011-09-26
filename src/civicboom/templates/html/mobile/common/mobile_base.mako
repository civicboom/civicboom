<!DOCTYPE html>
% if hasattr(next, 'init_vars'):
    ${next.init_vars()}
    ## AllanC - is init vars actually needed here? init_vars was a horrible hack to enable the frag rendered to prepare variables to style the frag holders (icons for actions, titles), is this needed in the mobile variant?
% endif
<html>
    <head>
        ${title()}
        
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <link rel="shortcut icon" href="/images/boom16.ico" />
        
        ## --- CSS imports ---
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
        ## ------
        
        <script type="text/javascript" src="/javascript/jquery-1.6.2.js"></script>
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
        <script type="text/javascript" src="/javascript/jquery.mobile-1.0b3.js"></script>
        ## Not currently used
        ## <script src="/javascript/jquery.ui.datepicker.mobile.js"></script>
    </head>
    
  
    <body class="c-${c.controller} a-${c.action}">
        ${next.body()}
    </body>
</html>

<%def name="title()">
    <title>
        ${_('_site_name Mobile')}
        % if hasattr(next, 'page_title'):
        : ${next.page_title()}
        % endif
    </title>
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