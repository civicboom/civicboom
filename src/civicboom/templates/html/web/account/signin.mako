<%inherit file="/html/web/common/html_base.mako"/>

<%def name="title()">${_("Sign in")}</%def>


<%def name="body()">
    
    
    <div class="layout">
        
        ${signin_actions()}
        
        <table><tr><td class="body page_border">
            <table class="signin">
                <tr>
                    <td width="45%">
                        ${signin()}
                    </td>
                    <td width="10%" rowspan="3">
                        <b style="font-size: 3em;">&nbsp;or&nbsp;&rarr;</b>
                    </td>
                    <td width="45%" rowspan="3">
                        ${janrain()}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        ${forgot()}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        ${signup()}
                    </td>
                </tr>
            </table>
        </td></tr></table>
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
<section>
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
	<h1>${_("Sign up (It's free!)")}</h1>
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
<section>
	<a class="button" style="float: right; margin: 16px;" href="#" id="iforgot" onclick="$('#iforgot').hide(); $('#reminder').show();">${_("Forgotten your password?")}</a>
	
	<div id="reminder" class="hideable">
	<p>&nbsp;
	<form action="${h.url(controller='account', action='forgot_password', format='redirect')}" method="post" style="clear:both">
		<table class="form">
			<tr>
				<td width="50"><label for="username_forgotten">${_("Username")}</label></td>
				<td><input type="text"  id="username_forgotten" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td colspan="2"><label>or</label></td>
			</tr>
			<tr>
				<td><label for="email_forgotten">${_("Email")}</label></td>
				<td><input type="email" id="email_forgotten" name="email" placeholder="e.g. dave@coolnews.net"/></td>
			</tr>
			<tr>
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Send password reminder")}"/></td>
			</tr>
		</table>
	</form>
	<p>&nbsp;
	</div>
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
            <p>By signing  in/up you will accept the <b>${assignment['title']}</b> request that has been set by <b>${creator_name}</b></p>
            
        ## Follow
        % elif c.action_objects['action'] == 'follow':
            <%
                member      = c.action_objects['action_object'].get('member')
                member_name = member['name']
            %>
            <p>By signing in/up you will follow <b>${member_name}</b> </p>
        
        % elif c.action_objects['action'] == 'boom':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            <p>By signing in/up you will Boom the _content <b>${content['title']}</b> by <b>${creator_name}</b></p>
            
        %elif  c.action_objects['action'] == 'new_respose':
            <%
                content      = c.action_objects['action_object'].get('content')
                creator_name = content['creator']['name']
            %>
            <p>By signing in/up you will respond to the _assignment <b>${content['title']}</b> by <b>${creator_name}</b></p>
        
        %elif  c.action_objects['action'] == 'comment':
            <%
                content       = c.action_objects['action_object'].get('content')
            %>
            <p>By signing in/up you make a comment on <b>${content.get('title')}</b> </p>
        
        %else:
            ##c.action_objects['action'] == 'new_article':
            <%
            %>
            <p>By signing in/up you will ${c.action_objects['description']}</p>
        % endif
        
        ##${c.action_objects['description']}
        ##${c.action_objects['action_object']}
        </div>
    % endif
    
</%def>
