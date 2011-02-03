<%inherit file="/html/widget/common/widget_content.mako"/>

<%namespace name="get_widget" file="/frag/misc/get_widget.mako"/>

##<p class="content_title">${_("Embed this widget on your website")}</p>
<p>${_("Simply copy and paste this code into your site's HTML")}</p>
## to embed this organisation's _site_name request feed.

<form action="">
  <textarea rows="4" name="widget_link" style="width:95%;">${get_widget.widget_iframe(c.widget['owner'])}</textarea>
</form>

<p>${_("Want to get a widget for your community?")}</p>
<a href="${h.url('/',subdomain='')}" target="_black">${_("Get started with ")}<img src="/images/logo.png" alt="${_('_site_name')}" style="max-height: 1.5em; vertical-align: middle;"/></a>