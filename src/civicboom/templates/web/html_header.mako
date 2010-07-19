<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  
  <title>Test</title>

  % if hasattr(self,'styleOverides'):
  <style type="text/css">
    ${self.styleOverides()}
  </style>
  % endif
  
</head>

<body>

  ##<!--[if lte IE 6]>
  ##<script type="text/javascript">
  ##  alert("${c.site_name} does not currently support Microsoft Internet Explorer 6 or below. Please use an alternative browser.");
  ##</script>
  ##<![endif]-->

  ## AllanC
  ## Some divs are tagged with the class "hideable"
  ## if these were set in the CSS to be display:none they would never be revealable if the client has javascript disabled
  ## solution, set the css propert for the hideable elements from javascript,
  ## see toggle_div.js for more details on revealing these divs
  ## see indiconews_base.js for createCSS
  ##<script type="text/javascript">
    ##AllanC: investigate this being done with YUI Stylesheet utils lib, I dont like relying on the current 3rd party CSS javascript
  ##  createCSS(".hideable", "display: none;");
  ##  createCSS(".popup"   , "display: none; position: fixed; left: 200px; top: 50px;");
  ##</script>

  ##<!-- YUI #doc3 = 100%  width -->
  ##<!-- YUI #doc4 = 974px width, centered -->
  <%def name="yuiTemplateType()"></%def>
  <div id="doc4" class="${self.yuiTemplateType()}">
    ${next.body()}
  </div>
  <!-- end of overall doc div -->
 
  ##<%include file="includes/scripts_end.mako"/>
</body>
</html>
