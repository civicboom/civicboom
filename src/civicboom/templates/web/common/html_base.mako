<!DOCTYPE html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ --> 
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link rel="shortcut icon" href="${h.wh_public("images/civicboom.ico")}" />
	<link rel="apple-touch-icon" href="${h.wh_public("images/civicboom.png")}">

##----------------------------------------------------------------------------
## Meta Text
##----------------------------------------------------------------------------
	<meta name="description" content="${_("_site_description")}"/>
	<meta name="keywords"    content="" />
	<meta name="authors"     content="${config['email.contact']}, Elizabeth Hodgson, Allan Callaghan, Chris Girling" />
	<meta name="robots"      content="all" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta charset="utf-8">

##----------------------------------------------------------------------------
## Title
##----------------------------------------------------------------------------  
<%def name="title()">${_("_tagline")}</%def>
<% title_dev_prefix = "Dev-" if config['development_mode'] else "" %>
	<title>${title_dev_prefix}${_("_site_name")}: ${self.title()}</title>

##----------------------------------------------------------------------------
## Base CSS and Javascript imports
##----------------------------------------------------------------------------
##-------------------
## CSS Style Sheets
##-------------------
% if config['development_mode']:
	<link rel="stylesheet" type="text/css" href="/styles/common/yui-3.2.0-grids-min.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/jquery.ui-1.8.4.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/jquery.ui.stars.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/layout.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/icons_avatar_thumbnails.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/misc.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/account.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/content_editor.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/messages.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/menuh.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/layout.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/misc.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/member_includes.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/content.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/settings.css" />
% else:
	<link rel="stylesheet" type="text/css" href="/styles/web.css" />
% endif

##-------------------
## Javascripts
##-------------------
% if config['development_mode']:
	<!-- Browser bug fixes -->
	<script src="/javascript/Modernizr.js"></script>
	<!-- jQuery -->
	<script src="/javascript/jquery-1.4.2.js"></script>
	<script src="/javascript/jquery.ui.js"></script>
	<script src="/javascript/jquery.ui.stars-3.0.1.js"></script>
	<script src="/javascript/jquery.html5-0.0.1.js"></script>
	<!-- Civicboom -->
	<script src="/javascript/misc.js"></script>
	<script src="/javascript/url_encode.js"></script>
	<script src="/javascript/toggle_div.js"></script>
	<script src="/javascript/cb_frag.js"></script>
% else:
	<script src="/javascript/_combined.common.js"></script>
% endif
<!-- IE9.js breaks other browsers, so keep it out of the minimised packs -->
<!--[if lt IE 9]>
	<script src="/javascript/IE9.js"></script>
<![endif]-->


##--------------------------------------------------------
## Head Links - child templates can add scripts & styles
##--------------------------------------------------------
<%def name="head_links()"></%def>
${self.head_links()}


##-------------------
## Style Overrides
##-------------------
% if hasattr(next, 'styleOverides'):
    <style type="text/css" >
    ${next.styleOverides()}
    </style>
% endif

##----------------------------------------------------------------------------
## Google Analitics - ASync array setup
##----------------------------------------------------------------------------
## http://code.google.com/apis/analytics/docs/tracking/asyncUsageGuide.html#SplitSnippet
## As this is just an array there is no harm in declaring it here
	<!-- Google Analytics -->
	<script type="text/javascript">
		var _gaq = _gaq || [];
		_gaq.push(['_setAccount', '${config['api_key.google.analytics']}']);
		_gaq.push(['_trackPageview']);
	</script>


##----------------------------------------------------------------------------
## Development Javascript Debug Console Output
##----------------------------------------------------------------------------
% if config['development_mode']:
	<!-- Development Mode - Enabale Console Logging in client browser (recomend firebug) but could instate YUI log console here -->
    
	## YUI 3
    <script src="/javascript/yui-min.js"></script>
    <script>
        Y = new YUI({ debug : true }); //var 
        Y.log("YUI Debugger Enabled", "info",  "civicboom");
    </script>
% endif
</head>

##------------------------------------------------------------------------------
## Flash Message Area
##------------------------------------------------------------------------------
## Some form functions will need to return a status to inform users the operation completed
## This displays the message and then removes it from the session once it is displayed the first time
## See "Definitive Guide to Pylons" pg 191 for details
<%def name="flash_message()">
    <div id="flash_message" class="hidden_by_default status_${c.result['status']}">${c.result['message']}</div>
% if c.result['message'] != "":
	<!-- if we have a flash message in the session, activate it -->
	<script type="text/javascript">
		<% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
		$(function() {flash_message(${json_message|n});});
    </script>
% endif
</%def>

##------------------------------------------------------------------------------
## HTML Body
##------------------------------------------------------------------------------
<%
if c.logged_in_persona:
	u = "user"
else:
	u = "anon"
%>
<body class="c-${c.controller} a-${c.action} u-${u}">
	${flash_message()}
	<nav><%include file="navigation.mako"/></nav>
	<header><%include file="header.mako"/></header>
	<div id="app">
% if hasattr(next, 'col_left'):
		<div id="col_left">${next.col_left()}</div>
% endif
% if hasattr(next, 'col_right'):
		<div id="col_right">${next.col_right()}</div>
% endif
		<div id="col_main">${next.body()}</div>
	</div>
	<footer><%include file="footer.mako"/></footer>
	<%include file="scripts_end.mako"/>
</body>
</html>
