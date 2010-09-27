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
	<% title_dev_prefix = "" %>
	<% if config['development_mode']: title_dev_prefix = "Dev-" %>
	<title>${title_dev_prefix}${_("_site_name")}: ${self.title()}</title>

##----------------------------------------------------------------------------
## Base CSS and Javascript imports
##----------------------------------------------------------------------------

##-------------------
## CSS Style Sheets
##-------------------
% if config['development_mode']:
	<link rel="stylesheet" type="text/css" href="/styles/jquery.ui-1.8.4.css" />
	<link rel="stylesheet" type="text/css" href="/styles/jquery.ui.stars.css" />
	<link rel="stylesheet" type="text/css" href="/styles/civicboom.css" />
% else:
	<link rel="stylesheet" type="text/css" href="/styles/_combined.css" />
% endif

##-------------------
## Javascripts
##-------------------
% if config['development_mode']:
	<!-- HTML5 -->
	<script type="text/javascript" src="/javascript/Modernizr.js"></script>
	<script type="text/javascript" src="/javascript/html5.js"></script>
	<!-- jQuery -->
	<script type="text/javascript" src="/javascript/jquery-1.4.2.js"></script>
	<script type="text/javascript" src="/javascript/jquery.ui-1.8.4.js"></script>
	<script type="text/javascript" src="/javascript/jquery.ui.stars-3.0.1.js"></script>
	<!-- Civicboom -->
	<script type="text/javascript" src="/javascript/misc.js"></script>
	<script type="text/javascript" src="/javascript/url_encode.js"></script>
	<script type="text/javascript" src="/javascript/toggle_div.js"></script>
% else:
	<script type="text/javascript" src="/javascript/_combined.js"></script>
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
    <div id="flash_message" style="position: absolute; top: 0px; left: 0px; right: 0px;" class="hidden_by_default status_${c.result['status']}">${c.result['message']}</div>
        
	<!-- animation for flash message -->
	<script type="text/javascript">
		function flash_message(json_message) {
			if (typeof(json_message) == "string") {json_message = {status:'ok', message:json_message};}
			if (json_message.message != "") {
				$("#flash_message").removeClass("status_error").removeClass("status_ok").addClass("status_"+json_message.status);
				$("#flash_message").text(json_message.message).slideDown("slow").delay(5000).slideUp("slow");
			}
		}
	% if c.result['message'] != "":
		<% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
		$(function() {flash_message(${json_message|n});});
	% endif
    </script>
</%def>

##------------------------------------------------------------------------------
## HTML Body
##------------------------------------------------------------------------------
<body class="c-${c.controller} a-${c.action}">
	${flash_message()}
	<header><%include file="includes/header.mako"/></header>
	${next.body()}
	<footer><%include file="includes/footer.mako"/></footer>
	<%include file="includes/scripts_end.mako"/>
</body>
</html>
