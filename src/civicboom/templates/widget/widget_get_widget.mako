<%inherit file="./widget_content.mako"/>
<%namespace name="widget_includes"  file="get_widget_code.mako"/>

<p class="content_title">${_("Embed this widget on your website")}</p>
<p>${_("Simply copy and paste this code into your site's HTML to embed this organisation's _site_name request feed.")}</p>
${widget_includes.get_widget_code(member=c.widget_owner,preview=False,instructions=False, customisation_controls=False)}
<p>${_("Want to get a widget for your community?")}</p>
<a href="/" target="_black">${_("Click here and get started")}</a>