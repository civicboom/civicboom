<%namespace name="scripts_end" file="/html/web/common/scripts_end.mako"/>\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${_("_site_name Widget")}</title>

		##----------------------------------------------------------------------
		## Styles
		##----------------------------------------------------------------------
		% if config['development_mode']:
		<link rel="stylesheet" type="text/css" href="/styles/common/yui-3.2.0-grids-min.css" />
        <link rel="stylesheet" type="text/css" href="/styles/common/icons.css" />
		##<link rel="stylesheet" type="text/css" href="/styles/common/thumbnails.css" />
		<link rel="stylesheet" type="text/css" href="/styles/widget/layout.css" />
		##<link rel="stylesheet" type="text/css" href="/styles/widget/widget_size_wide.css" />
		% else:
		<link rel="stylesheet" type="text/css" href="/styles/widget.css" />
		% endif

		##----------------------------------------------------------------------
		## Google Analitics (async setup, see scripts_end for more)
		##----------------------------------------------------------------------
		${scripts_end.google_analytics_head()}

		
		<%doc>
			## debug
		<meta http-Equiv="Cache-Control" Content="no-cache">
		<meta http-Equiv="Pragma" Content="no-cache">
		<meta http-Equiv="Expires" Content="0">
		</%doc>
    </head>
    
    <%
	additonal_layout = ""
	#if isinstance(c.widget_width, basestring) and int(c.widget_width) >= 280:
	#    additonal_layout = "wide"
    %>
    <body id="CivicboomWidget" style="width:${c.widget['width']}px; height:${c.widget['height']}px;">
        ##<div class="theme_${c.widget['theme']} ${additonal_layout}" style="width:${c.widget['width']}px;">
        ${next.body()}
        ##</div>
    </body>
    
	${scripts_end.google_analytics_end()}
</html>
