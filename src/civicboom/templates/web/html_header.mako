<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

##------------------------------------------------------------------------------
## HTML Header
##------------------------------------------------------------------------------
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link rel="shortcut icon" href="/images/civicboom.ico" />
  
  ##----------------------------------------------------------------------------
  ## Meta Text
  ##----------------------------------------------------------------------------
  <meta name="description" content="${_("site description")}"/>
  <meta name="keywords"    content="" />
  <meta name="authors"     content="${app_globals.email_contact}, Elizabeth Hodgson, Allan Callaghan, Chris Girling" />
  <meta name="robots"      content="all" />

  ##----------------------------------------------------------------------------
  ## Title
  ##----------------------------------------------------------------------------  
  <%def name="title()">${_("tagline")}</%def>
  <% title_dev_prefix = "" %>
  <% if app_globals.development_mode: title_dev_prefix = "Dev-" %>
  <title>${title_dev_prefix}${_("site name")}: ${self.title()}</title>

  ##----------------------------------------------------------------------------
  ## CSS Style Sheets
  ##----------------------------------------------------------------------------
  <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/reset-fonts-grids/reset-fonts-grids.css" />
  <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/assets/skins/sam/skin.css" />
  <link rel="stylesheet" type="text/css" href="/styles/design09/design09.css" />

  ##----------------------------------------------------------------------------
  ## Javascripts
  ##----------------------------------------------------------------------------
  
  ##<!-- YUI 2.x imports -->
  <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/yahoo-dom-event/yahoo-dom-event.js"></script><!-- Utility Dependencies -->
  <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/element/element-min.js"            ></script> 
  <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/container/container_core-min.js"   ></script><!-- Needed for Menus, Buttons and Overlays used in the Toolbar -->
  <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/editor/simpleeditor-min.js"        ></script><!-- Source file for Rich Text Editor-->
  
  ##<!-- Civicboom imports -->
  <script type="text/javascript" src="/javascript/url_encode.js"      ></script>
  <script type="text/javascript" src="/javascript/toggle_div.js"      ></script>

  ##----------------------------------------------------------------------------
  ## Development Javascript Debug Console Output
  ##----------------------------------------------------------------------------
  % if app_globals.development_mode:
    <!-- Development Mode - Enabale Console Logging in client browser (recomend firebug) but could instate YUI log console here -->
    <!-- Use console output with: YAHOO.log("Loggy log log"); -->
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/logger/logger-min.js"></script>
    <script type="text/javascript">YAHOO.widget.Logger.enableBrowserConsole();</script>
  % endif
  
  ##----------------------------------------------------------------------------
  ## RSS
  ##----------------------------------------------------------------------------
  ##  Overriding class's should override rss() to print rss_header_link()
  ##  this is so that pages without an RSS feed dont print a link in the header
  <%def name="rss()"></%def>
  <%def name="rss_url()"  ></%def>
  <%def name="rss_title()"></%def>
  <%def name="rss_header_link()" >
    <link href="${self.rss_url()}" title="${self.rss_title()}" type="application/rss+xml" rel="alternate"/>
  </%def>
  ${self.rss()}

  ##----------------------------------------------------------------------------
  ## Style Overrides
  ##----------------------------------------------------------------------------
  ##  Inheriting mako files can put in there own custom CSS rules
  % if hasattr(self,'styleOverides'):
  <style type="text/css">
    ${self.styleOverides()}
  </style>
  % endif
  
</head>



##------------------------------------------------------------------------------
## HTML Body
##------------------------------------------------------------------------------
<body>

  ## AllanC - IE6 Warning messge
  ##<!--[if lte IE 6]>
  ##<script type="text/javascript">
  ##  alert("${app_globals.site_name} does not currently support Microsoft Internet Explorer 6 or below. Please use an alternative browser.");
  ##</script>
  ##<![endif]-->

  ## AllanC
  ## Some divs are tagged with the class "hideable"
  ## if these were set in the CSS to be display:none they would never be revealable if the client has javascript disabled
  ## solution, set the css propert for the hideable elements from javascript,
  ## see toggle_div.js for more details on revealing these divs
  ## see indiconews_base.js for createCSS
  <script type="text/javascript">
    ##AllanC: investigate this being done with YUI Stylesheet utils lib, I dont like relying on the current 3rd party CSS javascript
    createCSS(".hideable", "display: none;");
    createCSS(".popup"   , "display: none; position: fixed; left: 200px; top: 50px;");
  </script>

  ##<!-- YUI #doc3 = 100%  width -->
  ##<!-- YUI #doc4 = 974px width, centered -->
  <%def name="yuiTemplateType()"></%def>
  <div id="doc4" class="${self.yuiTemplateType()}">
    ${next.body()}
  </div>
 
  <%include file="scripts_end.mako"/>
</body>
</html>
