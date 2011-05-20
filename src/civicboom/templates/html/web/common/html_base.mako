<!DOCTYPE html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ --> 
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
##----------------------------------------------------------------------------
## Meta Text
##----------------------------------------------------------------------------
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=8,chrome=1">
	<meta name="description" content="${_("_site_description")}"/>
	<meta name="keywords"    content="civicboom, social media, community, information, news" />
	<meta name="authors"     content="${config['email.contact']}, Elizabeth Hodgson, Allan Callaghan, Chris Girling, Greg Miell" />
	<meta name="robots"      content="all" />
	<meta name="viewport"    content="width=480, initial-scale=1">
	<meta name="google-site-verification" content="IeUt8MCUCpzq14C8DaxD5w8c-5iiRB1V5E4uh7nq3NY" />

	<link rel="shortcut icon" href="/images/boom16.ico" />
	<link rel="apple-touch-icon" href="/images/boom128.png" />
	<link rel="fluid-icon" href="/images/boom128.png" />
	<link rel="search" type="application/opensearchdescription+xml" href="/misc/opensearch.xml" title="${_("_site_name")}" />
	<link rel="profile" href="http://microformats.org/profile/hcard">

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
css_all    = [n[len("civicboom/public/"):] for n in css_all]
css_all.sort()
%>
% for css in css_all:
	<link rel="stylesheet" type="text/css" href="${h.wh_url("public", css)}" />
% endfor
% else:
	<link rel="stylesheet" type="text/css" href="${h.wh_url("public", "styles/web.css")}" />
% endif

##-------------------
## Javascripts
##-------------------
% if config['development_mode']:
    ## AllanC - Please note the order of these JS files should match the order in /public/javascript/Makefile to reduce potential errors with loading dependencys between the live and development sites
	<!-- Browser bug fixes -->
	<script src="/javascript/modernizr-1.7.js"></script>
	<script src="/javascript/swfobject.js"></script>
	<!-- jQuery -->
	<script src="/javascript/jquery-1.5.1.js"></script>
	<!-- Civicboom -->
	<script src="/javascript/prototypes.js"></script>
	<script src="/javascript/misc.js"></script>
	<script src="/javascript/url_encode.js"></script>
	<script src="/javascript/cb_frag.js"></script>
	<script src="/javascript/ajaxError.js"></script>
% else:
	<script src="${h.wh_url("public", "javascript/_combined.head.js")}"></script>
% endif

<%namespace name="share" file="/frag/common/share.mako" />

% if config['online']:
	${share.AddThisScript()}
% endif

##----------------------------------------------------------------------------
## Google Analitics (async setup, see scripts_end for more)
##----------------------------------------------------------------------------
	<%namespace name="scripts_end" file="/html/web/common/scripts_end.mako"/>
	${scripts_end.google_analytics_head()}


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
	<div id="app">${next.body()}</div>
	<footer><%include file="footer.mako"/></footer>
    ${popup_frame()}
	##<%include file="scripts_end.mako"/>
	${scripts_end.body()}

    <!--[if lt IE 8 ]>
    <script type="text/javascript">
            if ($.cookie('allow_lt_ie8')!='True') {
                window.location="${url(controller='misc', action='browser_unsupported')}";
            }
    </script>
    <![endif]-->

	<% from pylons import request %>
	<!--
	Version: ${request.environ['app_version'] or 'develop'}
	Node:    ${request.environ['node_name']}
	-->
</body>
</html>
