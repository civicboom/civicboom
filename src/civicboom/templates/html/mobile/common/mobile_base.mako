<html>
    <head>
        <title>${_('_site_name Mobile')}</title>
        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.2.0/build/cssreset/reset-min.css">
        <link rel="shortcut icon" href="/images/favicon.ico" />
        
##----------------------------------------------------------------------------
## Base CSS and Javascript imports
##----------------------------------------------------------------------------
% if config['development_mode']:
    <%
    from glob import glob
    css_common = glob("civicboom/public/styles/common/*.css")
    css_web    = glob("civicboom/public/styles/mobile/*.css")
    css_all    = css_common + css_mobile
    css_all    = [n[len("civicboom/public/"):] for n in css_all]
    css_all.sort()
    %>
    % for css in css_all:
            <link rel="stylesheet" type="text/css" href="${h.wh_url("public", css)}" />
    % endfor
% else:
	<link rel="stylesheet" type="text/css" href="${h.wh_url("public", "styles/mobile.css")}" />
% endif

    </head>
  
    <body>
        <div id="CivicboomMobile">
            ${next.body()}
        </div>
    </body>
</html>
