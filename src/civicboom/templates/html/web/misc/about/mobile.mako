<%inherit file="base.mako"/>
<%def name="title()">${_("_site_name Mobile")}</%def>

<a href="http://market.android.com/details?id=com.civicboom.mobile2"><img src="/images/about/qr_mobile2.png" style="float: right;"></a>

<h1>${_('_site_name Mobile')}</h1>

<ul class="bulleted">
<li>${_("Get requests directly via your Android mobile")}
<li>${_("Respond in an instant")}
<li>${_("Upload images, video, text and audio")}
</ul>

<p>&nbsp;

<h1>${_("How to get the app")}</h1>
${_("Scan the barcode (opposite) into your phone by using the barcode reader on your handset")}
(If you don't have the barcode reader, you can download the app directly from the
<a href="http://market.android.com/details?id=com.civicboom.mobile2">Android marketplace</a> on your handset)

<p>&nbsp;

<h1>${_("Signed up to _site_name via Facebook, Twitter, LinkedIn, etc? Then once you've downloaded the app:")}</h1>

<ol class="bulleted">
<li>${_("Go to your website settings page")}
<li>${_("Make a note of your username")}
<li>${_("Create a password")}
<li>${_("Log into the mobile app with your username and password")}
</ol>

<p>&nbsp;

<% 
    images = [
      ['login', 15, 20, True],
      ['live_feed', 110, 145, True],
      ['work_drafts', 110, 305, True],
      ['read_alerts', 110, 475, True],
      ['respond_messages', 100, 610, True],
      ['read_feed', 299, 10, True],
      ['view_requests', 299, 145, True],
      ['respond_request', 292, 275, True],
      ['add_media', 303, 405, True],
      ['geotag', 281, 542, True],
      ['publish', 503, 370, False]
    ]
%>
<h1>${_("Android app features and functions")}</h1>
<style tyle="text/css">
  #mobileflow {
    position: relative; width:735px; height:567px; background: url(/images/about/mobile/background.png);
  }
  .abs {
    position: absolute;
  }
  .hov div {
    border: solid white 3px;
    top: -70px;
    left: -40px;
    width: 237px;
    height: 345px;
    position: absolute;
    display: none;
    background-repeat: no-repeat;
    background-color: #FFF;
    z-index: 10;
  }
  .hov:hover div {
    display: block;
  }
  % for image in images:
    #h-${image[0]} { top: ${image[1]}px; left: ${image[2]}px; }
    #m-${image[0]} { background-image: url(/images/about/mobile/${image[0]}-l.png); }
  % endfor
</style>
<div style="position: relative; width:735px; height:567px; background: url(/images/about/mobile/background.png);" id="mobileflow">
  % for image in images:
    <div class="abs ${'hov' if image[3] else ''}" id="h-${image[0]}"><div id="m-${image[0]}"></div><img src="/images/about/mobile/${image[0]}.png" /></div>
  % endfor
</div>
