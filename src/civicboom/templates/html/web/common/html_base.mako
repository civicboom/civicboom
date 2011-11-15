<!DOCTYPE html>
<%def name="html_class_additions()"></%def>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ --> 
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie ie6 ${self.html_class_additions()}"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie ie7 ${self.html_class_additions()}"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie ie8 ${self.html_class_additions()}"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie ie9 ${self.html_class_additions()}"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js ${self.html_class_additions()}"> <!--<![endif]-->
<head>
##----------------------------------------------------------------------------
## Meta Text
##----------------------------------------------------------------------------
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=8,chrome=1">

<%def name="description()">${_("_site_description")}</%def>
	<meta name="description" content="${self.description()}"/>
	<meta name="keywords"    content="civicboom, social media, community, information, news" />
	<meta name="authors"     content="${config['email.contact']}, Elizabeth Hodgson, Allan Callaghan, Chris Girling, Greg Miell, Greg Mackelden" />
	<meta name="robots"      content="all" />
	<meta name="viewport"    content="width=480, initial-scale=1">
	<meta name="google-site-verification" content="IeUt8MCUCpzq14C8DaxD5w8c-5iiRB1V5E4uh7nq3NY" />

	<link rel="shortcut icon" href="/images/boom16.ico" />
	<link rel="apple-touch-icon" href="/images/boom128.png" />
	<link rel="fluid-icon" href="/images/boom128.png" />
	<link rel="search" type="application/opensearchdescription+xml" href="/misc/opensearch.xml" title="${_("_site_name")}" />
	<link rel="profile" href="http://microformats.org/profile/hcard">
<%def name="canonical_url()">${h.url('current', sub_domain='www', protocol='https', qualified=True, format=None)}</%def>
	<link rel="canonical" href="${self.canonical_url()}"/>

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
	<link rel="stylesheet" type="text/css" media="screen" href="${h.wh_url("public", "styles/web.css")}" />
<!--[if !(IE)]>
	<link rel="stylesheet" type="text/css" href="/fonts/fam-pro.css" />
<![endif]-->
##-------------------
## Javascripts
##-------------------
% if config['development_mode']:
    <script>
        boom_development = true;
        if (!window.console || ! window.console.log)
            console = {log: function (){}}
    </script>
    ## AllanC - Please note the order of these JS files should match the order in /public/javascript/Makefile to reduce potential errors with loading dependencys between the live and development sites
	<!-- Browser bug fixes -->
	<script src="/javascript/modernizr-1.7.js"></script>
	<script src="/javascript/swfobject.js"></script>
	<!-- jQuery -->
	<script src="/javascript/jquery-1.7.js"></script>
	<!-- Civicboom -->
	<script src="/javascript/prototypes.js"></script>
	<script src="/javascript/misc.head.js"></script>
	<script src="/javascript/url_encode.js"></script>
	<script src="/javascript/cb_frag.js"></script>
% else:
	<script src="${h.wh_url("public", "javascript/_combined.head.js")}"></script>
% endif

<%namespace name="share" file="/frag/common/share.mako" />

## addthis isn't used by the title page, but it slows down our first impression D:
% if config['online'] and not (c.controller=="misc" and c.action=="titlepage"):
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
    <% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
	<div id="flash_message" class="hidden_by_default status_${c.result['status']}${' event_load' if c.result['message'] != '' else ''}" data-message-json="${json_message}">${c.result['message']}</div>
	% if c.result['message'] != "":
	<!-- if we have a flash message in the session, activate it -->
	<script type="text/javascript">
		
		//$(function() {flash_message(${json_message|n});});
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
<body class="c-${c.controller} a-${c.action} u-${u}" data-base_url="${h.url('/', qualified=True)}">
    ${flash_message()}
    <header>
        % if hasattr(next, 'header'):
            ${next.header()}
        % else:
            <%include file="header.mako"/>
        % endif
    </header>
    <div id="app">${next.body()}</div>
    <footer><%include file="footer.mako"/></footer>

    <%def name="breadcrumbs()"></%def>
    <div class="hide_if_js">${self.breadcrumbs()}</div>

    ${popup_frame()}
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
