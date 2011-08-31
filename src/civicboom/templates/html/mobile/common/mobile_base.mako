<html>
    <head>
        ${title()}
        <link rel="shortcut icon" href="/images/favicon.ico" />
        
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
                $.mobile.page.prototype.options.degradeInputs.date = 'text';
            });
        </script>
        <script type="text/javascript" src="/javascript/jquery.mobile-1.0b2.js"></script>
        <script src="/javascript/jquery.ui.datepicker.js"></script>
        <script src="/javascript/jquery.ui.datepicker.mobile.js"></script>
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

<%def name="error_message()">
    <h3 id="error_message" class="status_${c.result['status']}">${c.result['message']}</h3>
    % if c.result['message'] != "":
    <script type="text/javascript">
        <% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
    </script>
    % endif
</%def>