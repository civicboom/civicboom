<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
            ${self.title_logo()}
            <h1>${_('The new way to source and share news!')}</h1>
            <div class="title_content">
    	        <a href="${h.url(controller='account', action='signin')}" rel="external"><button data-theme="b">${_('Sign in!')}</button></a>
    	        <p>
    	           <a href="${h.url(controller="contents", action="index")}">${_("or start exploring _site_name!")}</a>
                </p>
                <p><a href="${h.url(controller='misc', action='force_web')}" rel="external">${_('Click here to view the desktop website')}</a></p>
            </div>
	    </div>
	</div>
</%def>