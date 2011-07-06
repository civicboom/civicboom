<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="page_title()">
	${_("_site_name Mobile")}
</%def>

<%def name="header()">
	<h1>${_("_site_name - Mobile Edition")}</h1>
</%def>

<%def name="body()">
	<%inherit file="/html/mobile/account/signin.mako"/>
</%def>