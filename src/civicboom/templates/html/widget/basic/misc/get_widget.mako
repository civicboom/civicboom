<%inherit file="../common/widget_content.mako"/>

<%namespace name="get_widget" file="/frag/misc/get_widget.mako"/>

##<p class="content_title">${_("Embed this _widget on your website")}</p>
<p>${_("Simply copy and paste this code into your site's HTML")}</p>
## to embed this organisation's _site_name request feed.

<%
    # AllanC  - rrrrr .... 
    def normalize_member_username(member):
        if isinstance(member, dict):
            member = member.get('username')
        return member
%>

% if c.widget['owner']:
    <form action="">
        <textarea rows="4" name="widget_link" style="width:95%;">${get_widget.widget_iframe(member=c.widget['owner'])}</textarea>
    </form>
    <a href="${h.url(controller='misc', action='get_widget', id=normalize_member_username(c.widget['owner']), sub_domain='www')}" target="_black">${_('Customise this _widget')}</a>
##% else:
##  <a href="${h.url(controller='misc', action='get_widget',                                   sub_domain='www')}" target="_black">${_('Customise this _widget')}</a>
% endif

<p>${_("Want to get a _widget for your community?")}</p>
<a href="${h.url(controller='misc', action='titlepage', sub_domain='www')}" target="_black">${_("Get started with ")}<img src="/images/logo.png" alt="${_('_site_name')}" style="max-height: 1.5em; vertical-align: middle;"/></a>

