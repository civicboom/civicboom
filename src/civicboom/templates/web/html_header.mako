<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

##------------------------------------------------------------------------------
## HTML Header
##------------------------------------------------------------------------------
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
  ##
  ## Inheriting templates can add there own CSS and Javascript additions
  ## if subtemplates implement head_links they should always call the parent template as follows
  ## <%def name="head_links()">
  ##   ${parent.head_links()}
  ##   <link "your custom bits here">
  ## </%def>  
  <%def name="head_links()">
    ##-------------------
    ## CSS Style Sheets
    ##-------------------
    % if config['development_mode']:
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/reset-fonts-grids/reset-fonts-grids.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/autocomplete/assets/skins/sam/autocomplete.css">
    <link rel="stylesheet" type="text/css" href="/styles/design09/design09.css" />
    % else:
    <link rel="stylesheet" type="text/css" href="/styles/design09/_combined.css" />
    % endif

    ##-------------------
    ## Javascripts
    ##-------------------
    % if config['development_mode']:
    <!-- YUI 2.x global imports -->
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/yahoo-dom-event/yahoo-dom-event.js"></script><!-- Utility Dependencies -->
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/element/element-min.js"            ></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/animation/animation-min.js"        ></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/connection/connection-min.js"      ></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/datasource/datasource-min.js"      ></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/autocomplete/autocomplete-min.js"  ></script>
    <!-- Civicboom global imports -->
    <script type="text/javascript" src="/javascript/misc.js"          ></script>
    <script type="text/javascript" src="/javascript/url_encode.js"    ></script>
    <script type="text/javascript" src="/javascript/toggle_div.js"    ></script>
    <script type="text/javascript" src="/javascript/location.js"      ></script>
    <script type="text/javascript" src="/javascript/member.js"      ></script>
    % else:
    <script type="text/javascript" src="/javascript/_combined.js"></script>
    % endif
  </%def>
  ${self.head_links()}


  ##----------------------------------------------------------------------------
  ## Development Javascript Debug Console Output
  ##----------------------------------------------------------------------------
  % if config['development_mode']:
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
<body class="yui-skin-sam">

  ## AllanC - IE6 Warning messge
  ##<!--[if lte IE 6]>
  ##<script type="text/javascript">
  ##  alert("${_("site name")} does not currently support Microsoft Internet Explorer 6 or below. Please use an alternative browser.");
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
