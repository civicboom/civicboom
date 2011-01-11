<%inherit file="./widget_content.mako"/>
<%namespace name="get_widget_code"  file="get_widget_code.mako"/>

<p class="content_title">${_("Embed this widget on your website")}</p>
<p>${_("Simply copy and paste this code into your site's HTML to embed this organisation's _site_name request feed.")}</p>

<form action="">
  <textarea name="widget_link" class="widget_link_form_field">${get_widget_code.widget_code(c.widget_owner)}</textarea>
</form>

<p>${_("Want to get a widget for your community?")}</p>
<a href="/" target="_black">${_("Get started with ")}<img src="/images/logo.png" alt="${_('_site_name')}" style="max-height: 1.5em; vertical-align: middle;"/></a>