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
    ##% if config['development_mode']:
    <link rel="stylesheet" type="text/css" href="/styles/common/yui-3.2.0-reset-fonts.css" />
    <link rel="stylesheet" type="text/css" href="/styles/common/icons.css" />
    <link rel="stylesheet" type="text/css" href="/styles/widget/layout_${c.widget['theme']}.css" />
    ## AllanC - A temp rem until we can concatinate compiled .css files for each theme
    ##% else:
    ##<link rel="stylesheet" type="text/css" href="${h.wh_url("public", "styles/widget.css")}" />
    ##% endif

    ##----------------------------------------------------------------------
    ## Scripts
    ##----------------------------------------------------------------------
    <script type='text/javascript' src='/javascript/jquery-1.5.1.js'        ></script>
    <script type='text/javascript' src='/javascript/jquery.jcarousel.min.js'></script>

    ##----------------------------------------------------------------------
    ## Google Analitics (async setup, see scripts_end for more)
    ##----------------------------------------------------------------------
    ${scripts_end.google_analytics_head()}
    
    <style type="text/css">
        ## AllanC - IE7 does not support CSS inheritence so they have to be specified manually
        .ie7 a         {color:#${c.widget.get('color_font')};}
        .ie7 a:active  {color:#${c.widget.get('color_font')};}
        .ie7 a:visited {color:#${c.widget.get('color_font')};}
    </style>
</head>

<%
additonal_layout_class = ""
#if isinstance(c.widget_width, basestring) and int(c.widget_width) >= 280:
#    additonal_layout_class = "wide"
%>
<body id="CivicboomWidget" class="${additonal_layout_class}" style="width:${c.widget['width']}px; height:${c.widget['height']}px;">
    ${next.body()}
    ${scripts_end.google_analytics_end()}
</body>
</html>