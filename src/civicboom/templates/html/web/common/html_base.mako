<%namespace name="scripts_end" file="/html/web/common/scripts_end.mako"/>
<!DOCTYPE html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ --> 
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link rel="shortcut icon" href="/images/civicboom.ico" />
	<link rel="apple-touch-icon" href="/images/civicboom.png" />

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
<%
from glob import glob
css_common = glob("civicboom/public/styles/common/*.css")
css_web    = glob("civicboom/public/styles/web/*.css")
css_all    = css_common + css_web
css_all    = [n[len("civicboom/public"):] for n in css_all]
%>
% for css in css_all:
	<link rel="stylesheet" type="text/css" href="${css}" />
% endfor
% else:
	<link rel="stylesheet" type="text/css" href="/styles/web.css" />
% endif

##-------------------
## Javascripts
##-------------------
% if config['development_mode']:
	<!-- Browser bug fixes -->
	<script src="/javascript/Modernizr.js"></script>
	<script src="/javascript/swfobject.js"></script>
	<!-- jQuery -->
	<script src="/javascript/jquery-1.4.2.js"></script>
	<!-- Civicboom -->
	<script src="/javascript/misc.js"></script>
	<script src="/javascript/url_encode.js"></script>
	<script src="/javascript/cb_frag.js"></script>
% else:
	<script src="/javascript/_combined.head.js"></script>
% endif
<!-- IE9.js breaks other browsers, so keep it out of the minimised packs -->
<!--[if lt IE 7]>
	<script src="/javascript/IE8.js"></script>
<![endif]-->


##----------------------------------------------------------------------------
## Google Analitics (async setup, see scripts_end for more)
##----------------------------------------------------------------------------
	${scripts_end.google_analytics_head()}

##----------------------------------------------------------------------------
## JQuery SimpleModel Setup
##----------------------------------------------------------------------------
## http://www.ericmmartin.com/projects/simplemodal/
	<script type="text/javascript">
		$.extend($.modal.defaults, {
			closeClass: "simplemodalClose" ,
			##closeHTML : "<a href='#' class='icon icon_close' style='float: right;' title='Close'></a>" ,
			##opacity   : 60 ,
			onOpen: function (dialog) {
				dialog.overlay.fadeIn('slow');
				dialog.container.fadeIn('slow');
				dialog.data.fadeIn('slow');
			} ,
			onClose: function (dialog) {
				dialog.overlay.fadeOut('slow');
				dialog.container.fadeOut('slow');
				dialog.data.fadeOut('slow', function () {$.modal.close();});
			},
		});
	</script>

##----------------------------------------------------------------------------
## Development Javascript Debug Console Output
##----------------------------------------------------------------------------
% if config['development_mode']:
	<!-- Development Mode - Enabale Console Logging in client browser (recomend firebug) but could instate YUI log console here -->
	<script src="/javascript/yui-min.js"></script>
	<script>
		Y = new YUI({ debug : true }); //var 
		Y.log("YUI Debugger Enabled", "info",  "civicboom");
	</script>
% endif


##------------------------------------------------------------------------------
## Additional Head Links - child templates can add scripts & styles
##------------------------------------------------------------------------------
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


</head>

##------------------------------------------------------------------------------
## Flash Message Area
##------------------------------------------------------------------------------
## Some form functions will need to return a status to inform users the operation completed

<%def name="flash_message()">
	<div id="flash_message" class="hidden_by_default status_${c.result['status']}">${c.result['message']}</div>
	% if c.result['message'] != "":
	<!-- if we have a flash message in the session, activate it -->
	<script type="text/javascript">
		<% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
		$(function() {flash_message(${json_message|n});});
	</script>
	% endif
	<!-- redirect all AJAX errors to use the flash message system -->
	<script type="text/javascript">
		$('body').ajaxError(function(event, request, settings, exception) {
			flash_message(jQuery.parseJSON(request.responseText));
		});
	</script>
</%def>

##------------------------------------------------------------------------------
## Popup - Dynamic AJAX populated framework
##------------------------------------------------------------------------------
<%def name="popup_frame()">
	<%include file="popup_base.mako"/>
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
	##<nav><%include file="navigation.mako"/></nav>
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
	${popup_frame()}
	##<%include file="scripts_end.mako"/>
	${scripts_end.body()}
</body>
</html>
