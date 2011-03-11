<%namespace name="scripts_end" file="/html/web/common/scripts_end.mako"/>\
<!DOCTYPE html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ --> 
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
    <title>${_("_site_name Widget")}</title>

    ##----------------------------------------------------------------------
    ## Styles
    ##----------------------------------------------------------------------
    % if config['development_mode']:
    <link rel="stylesheet" type="text/css" href="/styles/common/yui-3.2.0-reset-fonts.css" />
    <link rel="stylesheet" type="text/css" href="/styles/common/icons.css" />
    ##<link rel="stylesheet" type="text/css" href="/styles/common/thumbnails.css" />
    <link rel="stylesheet" type="text/css" href="/styles/widget/layout.css" />
    ##<link rel="stylesheet" type="text/css" href="/styles/widget/widget_size_wide.css" />
    % else:
    <link rel="stylesheet" type="text/css" href="${h.wh_url("public", "styles/widget.css")}" />
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
    
    <style type="text/css">
        ## AllanC - IE7 does not support CSS inheritence so they have to be specified manually
        .ie7 a         {color:#${c.widget['color_font']};}
        .ie7 a:active  {color:#${c.widget['color_font']};}
        .ie7 a:visited {color:#${c.widget['color_font']};}
    </style>
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
