<%inherit file="/html/web/common/html_base.mako"/>
<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("Please check your email")}</%def>
<%def name="footer()">${components.misc_footer()}</%def>

<%def name="show_error(name)">
    ##% if 'group' in d and name in d['group'] and 'error' in d['group'][name]:
    % if d and 'invalid' in d and name in d['invalid']:
        <span class="error-message">${d['invalid'][name]}</span>
    % endif
</%def>

	<style>
		table.email {
			width: 51em; margin: auto; margin-top: 3em; font-size: 120%;
		}
		table.email td {
			vertical-align: top;
		}
		.email h2, .email p {
			padding-top: 1em;
		}
		.nopad {
			padding:0 !important;
		}
	</style>
<div class="layout">
	<table><tr><td class="body page_border">
	<table class="email">
		<tr>
			<td style="width: 33em; padding-right: 2em;">
			    <h1>Great! You're nearly done!</h1>
			    <h2>An email has been sent to the email address you provided, it should arrive in the next few minutes.</h2>
			    <p>Just click on the link <b>in the email</b>, follow the instructions to complete the
				sign up and enjoy full access to Civicboom!</p>
				<p>Please note that all future notifications will be sent to your registered
				email. If you wish to update it, click on the Settings link in your profile
				once you've completed the sign up.</p>
				<p style="font-weight: bold;">Happy booming!</p>
			</td>
			<td>
				<h2 class="nopad">Want to explore?</h2>
				<ul>
					<li>
						<h2><a href="${h.url('contents', list='assignments_active')}">${_("_Assignments HERE")}</a></h2>
						See what's being asked...
					</li>
					<li>
						<h2><a href="${h.url('contents', list='articles')}">${_('_Assignments and _articles HERE')}</a></h2>
						View the latest crowd-sourced news...
					</li>
					<%doc><li>
						<h2><a href="${h.url('members', type='user')}">Users HERE</a></h2>
						Check out the Civicboom community...
					</li>
					<li>
						<h2><a href="${h.url('members', type='group')}">Hubs HERE</a></h2>
						From news organisations to local fesitvals... they're all here
					</li></%doc>
				</ul>
			</td>
		</tr>
	</table>
	</td></tr></table>
</div>
