##<%inherit file="/design09/gadget/gadget_base.mako"/>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${_("_site_name Widget")}</title>
        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.0.0/build/cssreset/reset-min.css"/>
        ##<link rel="stylesheet" type="text/css" href="${c.server_name}/design09/design09_includes.css" />
        ##    <link rel="stylesheet" type="text/css" href="${c.server_name}/design09/gadget_specific.css" />
        <link rel="stylesheet" type="text/css" href="/styles/design09/widget_specific.css" />
        % if c.widget_theame:
          <link rel="stylesheet" type="text/css" href="/styles/design09/widget_theame_${c.widget_theame}.css" />
        % endif
        % if c.widget_width >= 280:
          <link rel="stylesheet" type="text/css" href="/styles/design09/widget_size_wide.css" />
        % endif
    </head>
    <body>
        <div id="CivicboomWidget">
            ${next.body()}
        </div>
        ## For Google analytics
        <%include file="/web/scripts_end.mako"/>
    </body>
</html>