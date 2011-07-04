<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    rss_url   = False
    help_frag = 'settings'
%>

<%namespace name="loc" file="/html/web/common/location.mako"/>

<%def name="title()">${_("Edit your _Group settings")}</%def>

<%def name="body()">
    <%
        from civicboom.model.member import group_member_roles, group_join_mode, group_member_visibility, group_content_visibility
        
        def get_param(name):
            if 'settings' in d and name in d['settings']:
                return d['settings'][name]
            return ''
    %>
    <%def name="show_error(name)">
        % if 'invalid' in d and name in d['invalid']:
            <span class="error-message error">${d['invalid'][name]}</span>
        % endif
    </%def>


    ## Setup Form
    <%
        if 'action' not in d:
            d['action'] = 'edit'
    %>
    % if d['action']=='edit' and 'settings' in d:
        ## Editing Form
        ${h.form(h.url('setting', id=c.result.get('id', 'me')), method='PUT' , multipart=True)}
    % else:
        ## Creating Form
        ${h.form(h.url('groups', )                 , method='POST', multipart=True)}
    % endif
    <div style="display:none"><input type="hidden" name="panel" value="${c.result.get('panel')}" /></div>

    
    <fieldset>
      <!--<legend>${_("_Group")}</legend>-->
      <table class="group-table">
        <tr class="padding">
          <td colspan="2">${_("_Group name")}</td>
          <td colspan="5">
            <input class="group-edit" type="text" name="name" value="${get_param('name')}" placeholder="${_('Enter the public name of your _Group here')}"/>
          ${show_error('name')} ${show_error('username')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="2">${_("Description")}<br />Who it's for<br />and purpose</td>
          <td colspan="5">
            <textarea class="group-edit" name="description" id="group_description" placeholder="${_('This will have text that will be a top line description of what this _Group could be for.')}">${get_param('description')}</textarea><br />
            ${show_error('description')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="7">${_("Default member role")}</td>
        </tr>
        <tr>
          <td style="width: 10px">&nbsp;</td>
          <td colspan="6">
            <input type="radio" class="quickchange" name="default_role" ${'checked=checked' if get_param('default_role') == 'observer' else ''} value="observer" id="default_role_observer" /><label for="default_role_observer">${_('Observer')}</label>
            <span class="role_description"> - ${_('a member of a _Group who can only view content/drafts and comment')}</span>
          </td>
        </tr>
        <tr>
          <td style="width: 10px">&nbsp;</td>
          <td colspan="6">
            <input type="radio" class="quickchange" name="default_role" ${'checked=checked' if get_param('default_role') == 'contributor' else ''} value="contributor" id="default_role_contributor" /><label for="default_role_contributor">${_('Contributor')}</label>
            <span class="role_description"> - ${_('a member who can do the above and create and edit drafts')}</span>
          </td>
        </tr>
        <tr>
          <td style="width: 10px">&nbsp;</td>
          <td colspan="6">
            <input type="radio" class="quickchange" name="default_role" ${'checked=checked' if get_param('default_role') == 'editor' else ''} value="editor" id="default_role_editor" /><label for="default_role_editor">${_('Editor')}</label>
            <span class="role_description"> - ${_('a member who can do the above plus publish content')}</span>
          </td>
        </tr>
        <tr class="padding">
          <td style="width: 10px">&nbsp;</td>
          <td colspan="6">
            <input type="radio" class="quickchange" name="default_role" ${'checked="checked"' if get_param('default_role') == 'admin' else ''} value="admin" id="default_role_admin" /><label for="default_role_admin">${_('Administrator')}</label>
            <span class="role_description"> - ${_('a member who can do the above and invite others to join and set member roles')}</span><br />
          ${show_error('default_role')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="7" style="text-align: center;">
            ${_('Note: By creating this _Group you are automatically set as an Administrator.')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="7">${_("Join mode")}</td>
        </tr>
        <style>
        	.mo-help div {
        		display: none;
				position: absolute;
				z-index: 100;
				width: 200px;
				background-color: #FFF;
				padding: 12px;
				
				border: 1px solid #2a3a87;
			
				border-radius        : 0.2em;
				-moz-border-radius   : 0.2em;
				-webkit-border-radius: 0.2em;
			
				box-sizing: border-box;
				-moz-box-sizing: border-box;
				-webkit-box-sizing: border-box;
			}
        	.mo-marker { display: inline-block; font-weight: bold; font-size: 1.25em; width: 1.25em; }
        	.mo-help:hover div { display: block; }
        </style>
        <tr class="padding">
          <td>&nbsp;</td>
          <td style="width:7em">
            <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'public' else ''} value="public" id="join_mode_public" /><label for="join_mode_public">${_('Open')}</label>
            <span class="mo-help">
            	<span class="mo-marker">?</span>
            	<div class="mo-help-r">
            		${_('Anyone can join this Hub and become a member as per default role setting. This means anyone beyond your club/assoc/brand can have privileges to Observe / Contribute / Edit or Administrate your Hub as set above.')}<br />
            		${_('Do not create an open Hub if you are not prepared for general access. For tighter join modes please see Public and Private options.')}
            	</div>
            </span>
          </td>
          <td style="width:7em">
            <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite_and_request' else ''} value="invite_and_request" id="join_mode_invite_and_request" /><label for="join_mode_invite_and_request">${_('Public')}</label>
            <span class="mo-help">
            	<span class="mo-marker">?</span>
            	<div class="mo-help-r">
            		${_('Anyone can request to join this Hub, and you can invite others to join, you have the ability to accept or decline join requests. The Public setting gives you greater control on who joins the Hub.')}
            	</div>
            </span>
          </td>
          <td style="width:7em">
            <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite' else ''} value="invite" id="join_mode_invite" /><label for="join_mode_invite">${_('Private')}</label>
            <span class="mo-help">
            	<span class="mo-marker">?</span>
            	<div class="mo-help-r">
            		${_('This gives you strictest control of who joins your Hub. It is invite only, and as an administrator you decide who to invite.')}
            	</div>
            </span>
          </td>
          <td colspan="3">
            ${show_error('join_mode')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="4">${_("Member visibility")}</td>
          <td colspan="3">${_("Default content visibility")}</td>
        </tr>
        <tr class="padding">
          <td>&nbsp;</td>
          <td>
            <input type="radio" class="quickchange" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'public' else ''} value="public" id="member_visibility_public" /><label for="member_visibility_public">${_('Open')}</label>
            <span class="mo-help">
            	<span class="mo-marker">?</span>
            	<div class="mo-help-r">
            		${_('Members of this group will be visible to anyone who views the Hub, even if they are not a member.')}
            	</div>
            </span>
          </td>
          <td>
            <input type="radio" class="quickchange" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'private' else ''} value="private" id="member_visibility_private" /><label for="member_visibility_private">${_('Hidden')}</label>
            <span class="mo-help">
            	<span class="mo-marker">?</span>
            	<div class="mo-help-r">
            		${_('Members of the group will be hidden to anyone viewing the Hub, except administrators of the Hub.')}
            	</div>
            </span>
          </td>
          <td style="width: 20px">
            ${show_error('member_visibility')}
          </td>
          <td style="width:7em">
            <input type="radio" class="quickchange" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'public' else ''} value="public" id="content_visibility_public" /><label for="content_visibility_public">${_('Open')}</label>
          </td>
          <td>&nbsp;
            <input type="radio" class="quickchange" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'private' else ''} value="private" id="content_visibility_private" /><label for="content_visibility_private">${_('Hidden')}</label>
          </td>
          <td>${show_error('default_content_visibility')}</td>
        </tr>
        <tr class="padding">
          <td colspan="2"><label for="website">${_('Website:')}</label></td>
          <td colspan="4"><input type="text" name="website" id="website" value="${get_param('website')}" /></td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="2"><label for="avatar">${_('_Group avatar:')}</label></td>
          <td colspan="4"><input type="file" name="avatar" id="avatar" /></td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
        	<td colspan="5"><label for="permission">${_('This _Group represents an organisation and I have the permissions/rights to create it.')}</label></td>
          <td><input type="checkbox" name="permission" id="permission" /></td>
          <td style="width: 10px">&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="6">${_('Before clicking "Create" I confirm any logo/image I upload does not infringe upon any trademarks, third party copyrights, other such rights, or violate the user agreement.')}</td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="6">${_('I can also confirm that by clicking "Create" I have read and accepted the')} <a href="http://localhost/about/terms">${_('terms and conditions')}</a> ${_('associated with creating a _Group.')}</td>
          <td>&nbsp;</td>
        </tr>
        <tr>
          <td colspan="6" style="text-align: right;">
          % if d['action']=='edit':
            <input type="submit" name="submit" value="${_('Save _Group')}" class="button" />
          % else:
            <input type="submit" name="submit" value="${_('Create _Group')}" class="button" />
          % endif
          </td>
          <td>&nbsp;</td>
        </tr>
      </table>
    </fieldset>
    
    ${h.end_form()}
</%def>
