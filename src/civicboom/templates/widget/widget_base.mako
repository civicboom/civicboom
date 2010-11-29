##<%inherit file="/design09/gadget/gadget_base.mako"/>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${_("_site_name Widget")}</title>
	<link rel="stylesheet" type="text/css" href="/styles/common/yui-3.2.0-grids-min.css" />
        <link rel="stylesheet" type="text/css" href="/styles/widget/layout.css" />
        % if c.widget_theame:
            <link rel="stylesheet" type="text/css" href="/styles/widget/widget_theame_${c.widget_theame}.css" />
        % endif
        % if c.widget_width >= 280:
            <link rel="stylesheet" type="text/css" href="/styles/widget/widget_size_wide.css" />
        % endif
        % if config['development_mode']:
	    <script src="/javascript/yui-min.js"></script>
	    <script>
		Y = new YUI({ debug : true }); //var 
		Y.log("YUI Debugger Enabled", "info",  "civicboom");
	    </script>
        % endif
    </head>
    <body>
        <div id="CivicboomWidget">
            ${next.body()}
        </div>
    </body>    
    <%include file="/web/common/scripts_end.mako"/>
</html>
