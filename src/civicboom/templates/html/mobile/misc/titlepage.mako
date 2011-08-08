<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="page_title()">
	${_("_site_name Mobile")}
</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="header" data-position="inline" data-theme="b">
            <h1>${_("Welcome to _site_name Mobile!")}</h1>
        </div>
        
        <div data-role="content">
            <div class="title_logo">
                <img class='logo_img' src='${h.wh_url("public", "images/logo-v3-684x150.png")}' alt='${_("_site_name")}' />
            </div>
            <div class="title_content">
    	        <a href="${url(controller='account', action='signin')}" rel="external"><button>Sign in!</button></a>
    	        <p>
    	           <a href="${h.url(controller="contents", action="index")}">${_("or start exploring _site_name!")}</a>
                </p>
            </div>
	    </div>
	</div>
</%def>