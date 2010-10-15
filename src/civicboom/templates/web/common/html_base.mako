<!DOCTYPE html>
<html class='no-js'>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link rel="shortcut icon" href="${h.wh_public("images/civicboom.ico")}" />

##----------------------------------------------------------------------------
## Meta Text
##----------------------------------------------------------------------------
	<meta name="description" content="${_("_site_description")}"/>
	<meta name="keywords"    content="" />
	<meta name="authors"     content="${config['email.contact']}, Elizabeth Hodgson, Allan Callaghan, Chris Girling" />
	<meta name="robots"      content="all" />

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
	<link rel="stylesheet" type="text/css" href="/styles/common/misc.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/content_editor.css" />
	<link rel="stylesheet" type="text/css" href="/styles/common/messages.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/layout.css" />
	<link rel="stylesheet" type="text/css" href="/styles/web/misc.css" />
% else:
	<link rel="stylesheet" type="text/css" href="/styles/web.css" />
% endif

##-------------------
## Javascripts
##-------------------
% if config['development_mode']:
	<!-- Browser bug fixes -->
	<script src="/javascript/Modernizr.js"></script>
	<script src="/javascript/IE9.js"></script>
	<!-- jQuery -->
	<script src="/javascript/jquery-1.4.2.js"></script>
	<script src="/javascript/jquery.ui-1.8.4.js"></script>
	<script src="/javascript/jquery.ui.stars-3.0.1.js"></script>
	<script src="/javascript/jquery.html5-0.0.1.js"></script>
	<!-- Civicboom -->
	<script src="/javascript/misc.js"></script>
	<script src="/javascript/url_encode.js"></script>
	<script src="/javascript/toggle_div.js"></script>
% else:
	<script src="/javascript/_combined.js"></script>
% endif

##----------------------------------------------------------------------------
## Development Javascript Debug Console Output
##----------------------------------------------------------------------------
% if config['development_mode']:
	<!-- Development Mode - Enabale Console Logging in client browser (recomend firebug) but could instate YUI log console here -->
	<!-- Use console output with: YAHOO.log("Loggy log log"); -->
	<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/logger/logger-min.js"></script>
	<script type="text/javascript">YAHOO.widget.Logger.enableBrowserConsole();</script>
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
if c.logged_in_user:
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
