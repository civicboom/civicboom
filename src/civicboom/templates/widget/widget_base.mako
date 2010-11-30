##<%inherit file="/design09/gadget/gadget_base.mako"/>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${_("_site_name Widget")}</title>

% if config['development_mode']:
	<link rel="stylesheet" type="text/css" href="/styles/common/yui-3.2.0-grids-min.css" />
	<link rel="stylesheet" type="text/css" href="/styles/widget/layout.css" />
	<link rel="stylesheet" type="text/css" href="/styles/widget/widget_size_wide.css" />
% else:
	<link rel="stylesheet" type="text/css" href="/styles/widget.css" />
% endif


% if config['development_mode']:
	<script src="/javascript/yui-min.js"></script>
	<script>
		Y = new YUI({ debug : true }); //var 
		Y.log("YUI Debugger Enabled", "info",  "civicboom");
	</script>
% endif
    </head>
    
    <%
	theme = "theme_" + c.widget_theme
	additonal_layout = ""
	if c.widget_width >= 280:
	    additonal_layout = "wide"
    %>
    <body id="CivicboomWidget">
        <div class="${theme} ${additonal_layout}">
            ${next.body()}
        </div>
    </body>
    <%include file="/web/common/scripts_end.mako"/>
</html>
