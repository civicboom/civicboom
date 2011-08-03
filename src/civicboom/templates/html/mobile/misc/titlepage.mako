<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="page_title()">
	${_("_site_name Mobile")}
</%def>

<%def name="header()">
	<h1>${_("_site_name - Mobile Edition")}</h1>
</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
	        <a href="${url(controller='account', action='signin')}" rel="external">sign in</a>
	    </div>
	</div>
</%def>