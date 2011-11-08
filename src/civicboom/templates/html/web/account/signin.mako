<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("Sign in")}</%def>

<%def name="body()">
    ${signin_page()}
    ${type_page()}
    ${ind_page()}
    ${org_page()}
</%def>

<%def name="signin_page()">
    <div class="layout body page_border" id="signin-page">
        ${signin_actions()}
            <table class="signin">
                <tr>
                    <td width="400" colspan="2">
                        ${signin()}
                        ${forgot()}
                    </td>
                    <td rowspan="2" style="text-align: center;">
                        <b style="font-size: 3em;">&nbsp;&nbsp;&nbsp;&larr;&nbsp;or&nbsp;&rarr;</b>
                    </td>
                    <td rowspan="2">
                        ${janrain()}
                    </td>
                </tr>
                <tr>
                    <td class="block" width="200" style="text-align: center;">
                        <a class="button" style="width: 75%;" href="#" onclick="
                            $('#signin-page').fadeOut(250, function() {$('#type-page').fadeIn(250);});
                        ">${_("Create an account")}</a>
                    </td>
                    <td class="block" width="200" style="text-align: center;">
                        <a class="button hide_if_nojs" style="width: 75%;" href="#" id="iforgot-button" onclick="
                            $('#username_forgotten').val($('#username').val());
                            $('#iforgot-button').fadeOut(250, function() {$('#signin-button').fadeIn(250);});
                            $('#signin-box').fadeOut(250, function() {$('#iforgot-box').fadeIn(250);});
                        ">${_("Reset password")}</a>
                        <a class="button hide_if_nojs" style="width: 75%;" href="#" id="signin-button"  onclick="
                            $('#signin-button').fadeOut(250, function() {$('#iforgot-button').fadeIn(250);});
                            $('#iforgot-box').fadeOut(250, function() {$('#signin-box').fadeIn(250);});
                        ">${_("Sign in")}</a>
                    </td>
                    <script>
                    $(function() {
                        $('#signin-button').hide();
                    });
                    </script>
                </tr>
                <tr>
                    <td class="block" colspan="2">
                    </td>
                </tr>
            </table>
    </div>
    ${components.misc_footer()}
</%def>

<%def name="type_page()">
    <div class="layout hide_if_js body page_border" id="type-page">
            <table class="signin">
                <tr>
                    <td colspan="2">
                        <h1>Individual or Organisation?</h1>
                    </td>
                </tr>
                <tr>
                    <td width="50%">
                        <div style="width: 100%; text-align: center;">
                            <img src="/images/misc/titlepage/organisation.png">
                            <a class="button" style="width: 315px;" href="#"  onclick="
                                $('#type-page').fadeOut(250, function() {$('#ind-page').fadeIn(250);});
                            ">${_("I am signing up for myself")}</a>
                        </div>
                    </td>
                    <td>
                        <div style="width: 100%; text-align: center;">
                            <img src="/images/misc/titlepage/audience.png">
                            <a class="button" style="width: 315px;" href="#"  onclick="
                                $('#type-page').fadeOut(250, function() {$('#org-page').fadeIn(250);});
                            ">${_("I am signing up for my organisation")}</a>
                        </div>
                    </td>
                </tr>
            </table>
    </div>
</%def>

<%def name="ind_page()">
    <div class="layout hide_if_js body page_border" id="ind-page">
        <div style="width: 400px; margin: auto;">${signup()}</div>
    </div>
</%def>

<%def name="org_page()">
    <div class="layout hide_if_js body page_border" id="org-page">
        <div style="width: 400px; margin: auto; text-align: left;">
        <h1>Create a personal account first</h1>
        <p>First you will need to create an account for yourself. Once you have
        an account, you can create a Hub for your organisation that other
        people can be added to.
        <p>&nbsp;
        <p>If you already have a personal account, <a href="/account/signin">sign in</a>
        and use the Hub selector (top right of the page) to create a new Hub.
        <p>&nbsp;
        ${signup()}
        </div>
    </div>
</%def>

<%def name="janrain()">
% if 'api_key.janrain' in config:
<section>
	% if config['online']:
		${h.get_janrain(lang=c.lang)}
	% else:
		<img src="/images/test/janrain.png">
	% endif
</section>
% endif
</%def>

<%def name="signin()">
<section id="signin-box">
	<h1>${_("Sign in")}</h1>
	<form action="${h.url('current', format='redirect')}" method="POST">
		<table class="form">
			<tr>
				<td width="50"><label for="username">${_("Username")}</label></td>
				<td><input type="text"     id="username" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="password">${_("Password")}</label></td>
				<td><input type="password" id="password" name="password" /></td>
			</tr>
			<tr>
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Sign in")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>

<%def name="signup()">
<section>
	<h1>${_("Sign up")}</h1>
	<form action="${h.url(controller='register', action='email', format='redirect')}" method="post">
		<table class="form">
			<tr>
				<td width="50"><label for="username_register">${_("Username")}</label></td>
				<td><input type="text" id="username_register" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="email_signup">${_("Email")}</label></td>
				<td><input type="email" id="email_signup" name="email" placeholder="e.g. dave@coolnews.net"/></td>
			</tr>
			<tr class="validation-result">
				<td></td>
				<td><div id="urldemo"></div></td>
			</tr>
			<tr>
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Sign up")}"/></td>
			</tr>
		</table>
	</form>
<script>
$(function() {
	init_validation(
		$("#username_register"),
		function() {
			$(".validation-result").css("display", "table-row");
			var val = $("#username_register").val();
			if(val.length < 4) {
				$("#urldemo").html("Username must be at least 4 characters");
				$("#username_register").addClass("invalid");
			}
			else {
				var username = val.toLowerCase().replace(/[^a-z0-9_-]/g, '-').replace(/^-+|-+$/g, '');
				$.ajax("/members.json?username="+username, {
					"success": function(result) {
					if(result.data.list.count == 0) {
						$("#urldemo").html("Your profile page will be https://www.civicboom.com/members/"+username);
						$("#username_register").addClass("valid");
					}
					else {
						$("#urldemo").html("The username "+val+" is already taken")
						$("#username_register").addClass("invalid");
					}
				}});
			}
		}
	);

	init_validation(
		$("#email_signup"),
		function() {
			var val = $("#email_signup").val();
			// really really really simple validation
			if(val.match(/.+@.+\..+/)) {
				$("#email_signup").addClass("valid");
			}
			else {
				$("#email_signup").addClass("invalid");
			}
		}
	);
});
</script>
</section>
</%def>

<%def name="forgot()">
<section id="iforgot-box" class="hide_if_js">
	<h1>${_("Reset password")}</h1>
	<form action="${h.url(controller='account', action='forgot_password', format='redirect')}" method="post" style="clear:both">
		<table class="form">
			<tr>
				<td width="50"><label for="username_forgotten">${_("Username")}</label></td>
				<td><input type="text"  id="username_forgotten" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="email_forgotten"><b>or</b> ${_("Email")}</label></td>
				<td><input type="email" id="email_forgotten" name="email" placeholder="e.g. dave@coolnews.net"/></td>
			</tr>
			<tr>
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Send password reminder")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>

<%def name="signin_actions()">
    ## AllanC:
    ##   TODO - internationalise these strings!

    ## Approved actions
    % if hasattr(c, 'action_objects'):
        <div class="signin_action_description page_border">
        
        ## Accept
        % if   c.action_objects['action'] == 'accept':
            <%
                assignment   = c.action_objects['action_object']['content']
                creator_name = assignment['creator']['name'] or assignment['creator']['username']
                content_title = assignment['title'] or None
            %>
            <p>${_('By signing  in/up you will accept the <b>%s</b> request that has been set by <b>%s</b>') % (assignment['title'], creator_name) |n}</p>
        ## Follow
        % elif c.action_objects['action'] == 'follow':
            <%
                member      = c.action_objects['action_object'].get('member')
                member_name = member['name']
            %>
            <p>${_('By signing in/up you will follow <b>%s</b>') % member_name |n}</p>
        
        % elif c.action_objects['action'] == 'boom':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            <p>${_('By signing in/up you will Boom the _content <b>$%s</b> by <b>%s</b>') % (content['title'],creator_name)  |n}</p>
            
        %elif  c.action_objects['action'] == 'new_respose':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            <p>${_('By signing in/up you will respond to the _assignment <b>%s</b> by <b>%s</b>') % (content['title'],creator_name)  |n}</p>
        
        %elif  c.action_objects['action'] == 'comment':
            <%
                content       = c.action_objects['action_object'].get('content')
            %>
            <p>${_('By signing in/up you make a comment on <b>%s</b>') % (content.get('title')) |n}</p>
        %else:
            ##c.action_objects['action'] == 'new_article':
            <%
            %>
            <p>${_('By signing in/up you will %s') % c.action_objects['description'] |n}</p>
        % endif
        
        ##${c.action_objects['description']}
        ##${c.action_objects['action_object']}
        </div>
    % endif
</%def>
