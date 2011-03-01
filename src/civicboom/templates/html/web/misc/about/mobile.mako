<%inherit file="base.mako"/>
<%def name="title()">${_("_site_name Mobile")}</%def>

<p>&nbsp;

<img src="/images/about/qr_mobile2.png" style="float: right;">

<h1>${_('_site_name Mobile')}</h1>

<ul class="bulleted">
<li>${_("Get requests directly via your Android mobile")}
<li>${_("Respond in an instant")}
<li>${_("Upload images, video, text and audio")}
</ul>

<p>

<h1>${_("How to get the app")}</h1>
${_("Scan the barcode (opposite) into your phone by using the barcode reader on your handset")}
(If you don't have the barcode reader, you can download the app directly from the
<a href="http://market.android.com/details?id=com.civicboom.mobile2">Android marketplace</a> on your handset)

<p>
<% 
    images = [
      ['login', 15, 20],
      ['live_feed', 110, 145],
      ['work_drafts', 110, 305],
      ['read_alerts', 110, 475],
      ['respond_messages', 100, 610],
      ['read_feed', 299, 10],
      ['view_requests', 299, 145],
      ['respond_request', 292, 275],
      ['add_media', 303, 405],
      ['geotag', 281, 542]
    ]
%>
<h1>${_("Android app features and functions")}</h1>
<style tyle="text/css">
  .hov {
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
<div style="position: relative; width:735px; height:567px; background: url(/images/about/mobile/background.png)">
  % for image in images:
    <div class="hov" id="h-${image[0]}"><div id="m-${image[0]}"></div><img src="/images/about/mobile/${image[0]}.png" /></div>
  % endfor
  <div class="" style="position: absolute; top:503px; left: 370px"><div id="m-publish"></div><img src="/images/about/mobile/publish.png" /></div>
</div>
