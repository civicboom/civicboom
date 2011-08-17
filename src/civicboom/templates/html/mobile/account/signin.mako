<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="page_title()">
	${_("_site_name Mobile - Sign In")}
</%def>

<%def name="header()">
	<h1>${_("Sign In")}</h1>
</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
	       ${signin()}
	   </div>
	</div>
</%def>

<%def name="signin()">
	<h1>${_("Sign in")}</h1>
	<form action="${h.url('current', format='redirect')}" method="POST" data-ajax="false">
	    <div data-role="fieldcontain">
			<label for="username">${_("Username")}</label>
			<input type="text" id="username" name="username" placeholder="e.g. dave43"/>
	    </div>
	    <div data-role="fieldcontain">
			<label for="password">${_("Password")}</label>
			<input type="password" id="password" name="password" />
		</div>
        <div data-role="fieldcontain" data-theme="b">
		    <input data-theme="b" class="button" type="submit" name="submit" value="${_("Sign in")}"/>
		</div>
	</form>
</%def>