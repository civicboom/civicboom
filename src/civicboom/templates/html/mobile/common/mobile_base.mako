<html>
    <head>
        <title>${next.page_title()}</title>
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
        <script type="text/javascript" src="/javascript/jquery.mobile-1.0b1.js"></script>
        <script type="text/javascript">
            // $.mobile.page.prototype.options.addBackBtn = "true";
        </script>
    </head>
  
    <body class="c-${c.controller} a-${c.action}">
        ${next.body()}
    </body>
</html>
