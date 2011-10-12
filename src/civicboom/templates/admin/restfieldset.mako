# -*- coding: utf-8 -*-
<%inherit file="/admin/html_base.mako"/>
<%!
from formalchemy.ext.pylons.controller import model_url
from pylons import url
%>
<%def name="h1(title, href=None)">
    <h1 id="header" style="padding-bottom: 0px;">
      %if breadcrumb:
        <div class="breadcrumb">
         /${'/'.join([u and '<a href="%s">%s</a>' % (u,n.lower()) or n.lower() for u,n in breadcrumb])|n} 
        </div>
      %endif
      %if href:
        <a href="${href}">${title.title()}</a>
      %else:
        ${title.title()}
      %endif
    </h1>
</%def>
<%def name="buttons()">
    <p class="fa_field">
      <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all" href="#">
        <input type="submit" value="${F_('Save')}" />
      </a>
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url(collection_name)}">
        <span class="ui-icon ui-icon-circle-arrow-w"></span>
        ${F_('Cancel')}
      </a>
    </p>
</%def>

<%def name="title()">
    ${collection_name.title()}
</%def>
<%def name="body()">
  %if isinstance(models, dict):
    <h1 id="header" style="padding-bottom: 0px;">${_('_site_name Control Panel')}</h1>
	<table class="outer">
		<tr><td>
<table>
	<tr><th colspan="3">${_("Database Editor")}</th></tr>
	<tr>
		<td>
			<p><a class="ui-state-default ui-corner-all" href="${models['ArticleContent']}">Articles</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['AssignmentContent']}">Assignments</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['CommentContent']}">Comments</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['DraftContent']}">Drafts</a></p>
			<hr>
			<p><a class="ui-state-default ui-corner-all" href="${models['ContentEditHistory']}">Content Edit History</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['FlaggedEntity']}">Flags</a></p>
		</td>
		<td>
			<p><a class="ui-state-default ui-corner-all" href="${models['User']}">Users</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['Group']}">Groups</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['Message']}">Messages</a></p>
		</td>
		<td>
			<p><a class="ui-state-default ui-corner-all" href="${models['License']}">Licenses</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['Tag']}">Tags</a></p>
			<p><a class="ui-state-default ui-corner-all" href="${models['Media']}">Media</a></p>
		</td>
	</tr>
	<tr>
	    <th colspan="1">${_("Payment")}</th>
	    <td></td>
        <td></td>
	</tr>
	<tr>
	    <td>
	        <p><a class="ui-state-default ui-corner-all" href="${models['PaymentAccount']}">Payment Accounts</a></p>
	        <p><a class="ui-state-default ui-corner-all" href="${models['Invoice']}">Invoices</a></p>
	        <p><a class="ui-state-default ui-corner-all" href="${models['BillingAccount']}">Billing Accounts</a></p>
	        <p><a class="ui-state-default ui-corner-all" href="${models['BillingTransaction']}">Billing Transactions</a></p>
	    </td>
	    <td></td>
	    <td></td>
	</tr>
</table>
		</td><td>
<table>
	<tr><th colspan="3">${_("Misc Tools")}</th></tr>
	<tr>
		<td>
			<ul>
				<li><a href="/admin/event_log">${_("Event Log")}</a></li>
				<li><a href="/admin/user_emails.csv">${_("Full User Email List")}</a></li>
				<li><a href="/admin/user_emails.csv?help_type=ind">${_("Ind User Email List")}</a></li>
				<li><a href="/admin/user_emails.csv?help_type=org">${_("Org User Email List")}</a></li>
			</ul>
		</td>
	</tr>
</table>
<table>
	<tr><th colspan="3">${_("Statistics")}</th></tr>
	<%
from civicboom.model.meta import Session
from civicboom.model import Content, User, Group, Media, FlaggedEntity
	%>
	<tr>
		<td>
			<ul>
				<li>
					${Session.query(Content).count()} ${_("bits of content")}
					(<a href="/admin/Content/models?Content--status=pending">${Session.query(Content).filter(Content.visible==False).count()} ${_("not visible")}</a>,
					<a href="/admin/FlaggedEntity/models">${Session.query(FlaggedEntity).count()} ${_("flagged")}</a>)
				</li>
				<li>
					${Session.query(User).count()} ${_("users")}
					(<a href="/admin/User/models?User--status=pending">${Session.query(User).filter(User.status=="pending").count()} ${_("pending")}</a>,
					<a href="/admin/User/models?User--status=suspended">${Session.query(User).filter(User.status=="suspended").count()} ${_("suspended")}</a>)
				</li>
				<li>${Session.query(Group).count()} ${_("groups")}</li>
				<li>${Session.query(Media).count()} ${_("uploads")}</li>
			</ul>
		</td>
	</tr>
</table>
<table>
	<tr><th colspan="3">${_("Full List")}</th></tr>
	<tr>
		<td>
			%for name in sorted(models):
			  <a style="display: inline;" href="${models[name]}">${name}</a>,
			%endfor
		</td>
	</tr>
</table>
	</table>
  %elif is_grid:
    ${h1(model_name)}
    <div class="ui-pager">
      ${pager|n}
    </div>
    <table class="layout-grid">
    ${fs.render()|n}
    </table>
    <p>
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url('new_%s' % member_name)}">
          <span class="ui-icon ui-icon-circle-plus"></span>
          ${F_('New')} ${model_name}
      </a>
    </p>
  %else:
    ${h1(model_name, href=model_url(collection_name))}
    %if action == 'show':
	  ${fs.render()|n}
      <p class="fa_field">
        <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url('edit_%s' % member_name, id=id)}">
          <span class="ui-icon ui-icon-pencil"></span>
          ${F_('Edit')}
        </a>
      </p>
    %elif action == 'edit':
      <form action="${model_url(member_name, id=id)}" method="POST" enctype="multipart/form-data">
        ${fs.render()|n}
        <input type="hidden" name="_method" value="PUT" />
        ${buttons()}
      </form>
    %else:
      <form action="${model_url(collection_name)}" method="POST" enctype="multipart/form-data">
        ${fs.render()|n}
        ${buttons()}
      </form>
    %endif
  %endif
<script type="text/javascript">
  var icons = document.getElementsByClassName('ui-icon')
  for (var i = 0; i < icons.length-1; i++) {
    icons[i].setAttribute('value', ' ');
  } 
</script>
</%def>
