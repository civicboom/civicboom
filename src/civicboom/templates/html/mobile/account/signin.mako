<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="components"      file="/html/mobile/common/components.mako" />

<%def name="page_title()">
	${_("Sign in")}
</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
            ${components.title_logo()}
        	<div class="signin_title">
        	   <h1>${_("Sign in to _site_name!")}</h1>
        	   ${parent.error_message()}
        	</div>
	       ${signin()}
	   </div>
	</div>
</%def>

<%def name="signin()">
	<form action="${h.url('current', format='redirect')}" method="POST" data-ajax="false" data-theme="b">
	    <div data-role="fieldcontain" data-theme="b">
			<label for="username">${_("Username")}</label>
			<input data-theme="b" type="text" id="username" name="username" placeholder="e.g. dave43"/>
			<label for="password">${_("Password")}</label>
			<input data-theme="b" type="password" id="password" name="password" />
		</div>
        <div data-role="fieldcontain" data-theme="b">
		    <input data-theme="b" class="button" type="submit" name="submit" value="${_("Sign in")}"/>
		</div>
	</form>
</%def>