<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = group
        if c.action == 'new':
            self.attr.frags = [quick_group, group]
            self.attr.frag_col_sizes = [1, 2]
    %>
</%def>


##------------------------------------------------------------------------------
## new/edit group
##------------------------------------------------------------------------------

<%def name="group()">
    ${frag.frag_basic(title=_('%s group') % c.action.capitalize(), icon='group', frag_content=group_content)}
</%def>
<%def name="group_content()">
    <%
        from civicboom.model.member import group_member_roles, group_join_mode, group_member_visibility, group_content_visibility
        
        def get_param(name):
            if 'group' in d and name in d['group']:
                return d['group'][name]
            return ''
    %>
    <%def name="show_error(name)">
        ##% if 'group' in d and name in d['group'] and 'error' in d['group'][name]:
        % if 'invalid' in d and name in d['invalid']:
            <span class="error-message">${d['invalid'][name]}</span>
        % endif
    </%def>



    ## Setup Form
    <%
        if 'action' not in d:
            d['action'] = 'create'
    %>
    % if d['action']=='edit' and 'group' in d:
        ## Editing Form
        ${h.form(h.url('group', id=get_param('id')), method='put')}
    % else:
        ## Creating Form
        ${h.form(h.url('groups', ), method='post')}
    % endif


    
    <fieldset>
  		<!--<legend>${_("Group")}</legend>-->
  		<table class='group-table'>
  			<tr class="padding">
  				<td colspan="2">${_("Group Name")}</td>
  				<td colspan="5">
  		      <input class="group-edit" type="text" name="name" value="${get_param('name')}"/>
          ${show_error('name')}
  				</td>
  			</tr>
  			<tr class="padding">
  				<td colspan="2">${_("Description")}</td>
  				<td colspan="5">
  		      <textarea class="group-edit" name="description">${get_param('description')}</textarea><br />
            ${show_error('description')}
  				</td>
  			</tr>
  			<tr class="padding">
  			  <td colspan="7">${_("Default member role")}</td>
  			</tr>
  			<tr class="padding">
  				<td style="width: 20px">&nbsp;</td>
  				<td colspan="6">
            <input type="radio" name="default_role" value="observer" id="default_role_observer" /><label for="default_role_observer">Observer</label><br />
            <input type="radio" name="default_role" value="contributor" id="default_role_contributor" /><label for="default_role_contributor">Contributor</label><br />
            <input type="radio" name="default_role" value="editor" id="default_role_editor" /><label for="default_role_editor">Editor</label><br />
            <input type="radio" name="default_role" value="admin" id="default_role_admin" /><label for="default_role_admin">Administrator</label><br />
          ${show_error('default_role')}
  				</td>
  			</tr>
  			<tr class="padding">
          <td colspan="7">${_("Join mode")}</td>
  			</tr>
  			<tr class="padding">
          <td>&nbsp;</td>
          <td>
            <input type="radio" name="join_mode" value="public" id="join_mode_public" /><label for="join_mode_public">Open?</label>
          </td>
          <td>
            <input type="radio" name="join_mode" value="invite_and_request" id="join_mode_invite_and_request" /><label for="join_mode_invite_and_request">Public?</label>
          </td>
          <td>
            <input type="radio" name="join_mode" value="invite" id="join_mode_invite" /><label for="join_mode_invite">Private?</label><br />
          </td>
          <td colspan="3">
            ${show_error('join_mode')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="4">${_("Default content visibility")}</td>
          <td colspan="3">${_("Member visibility")}</td>
        </tr>
        <tr class="padding">
          <td>&nbsp;</td>
          <td>
            <input type="radio" name="content_visibility" value="public" id="content_visibility_public" /><label for="content_visibility_public">Open</label>
          </td>
          <td>
            <input type="radio" name="content_visibility" value="private" id="content_visibility_private" /><label for="content_visibility_private">Hidden</label>
          </td>
          <td>${show_error('default_content_visibility')}</td>
          <td>
            <input type="radio" name="member_visibility" value="public" id="member_visibility_public" /><label for="member_visibility_public">Open</label>
          </td>
          <td>
            <input type="radio" name="member_visibility" value="private" id="member_visibility_private" /><label for="member_visibility_private">Hidden</label>
          </td>
          <td style="width: 20px">
            ${show_error('member_visibility')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="2"><label for="website">Website:</label></td>
          <td colspan="4"><input type="text" name="website" id="website" /></td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="2"><label for="logo_file">Logo File:</label></td>
          <td colspan="4"><input type="file" name="logo_file" id="logo_file" /></td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="2"><label for="logo_file">or</label></td>
          <td colspan="5">&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="2"><label for="logo_url">Logo URL:</label></td>
          <td colspan="4"><input type="text" name="logo_url" id="logo_url" /></td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="5"><label for="permission">This Group represents an organisation and I have the permissions/rights to create it.</label></td>
          <td><input type="checkbox" name="permission" id="permission"/>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="6">Before clicking "Create" I confirm any logo/image I upload does not infringe upon any trademarks,
          third party copyrights, other such rights, or violate the user agreement.</td>
          <td>&nbsp;</td>
        </tr>
        <tr class="padding">
          <td colspan="6">I can also confirm that by clicking "Create" I have read and accepted the <a href="#">terms and conditions</a> associated with creating a group.</td>
          <td>&nbsp;</td>
        </tr>
  			<tr>
  				<td colspan="2">
  				% if d['action']=='edit':
  					<input type="submit" name="submit" value="${_('Save Group')}" class="button" />
  				% else:
  					<input type="submit" name="submit" value="${_('Create Group')}" class="button" />
  				% endif
  				</td>
  			</tr>
      </table>
    </fieldset>
    
    ${h.end_form()}
</%def>

##------------------------------------------------------------------------------
## Quick group
##------------------------------------------------------------------------------

<%def name="quick_group()">
    ${frag.frag_basic(title=_('Quick group'), icon='group', frag_content=quick_group_content)}
</%def>
<%def name="quick_group_content()">
    <script type="text/javascript">
      var quickOrder = ['default_role', 'join_mode', 'content_visibility', 'member_visibility'];
      var quickSelection = {'news': '0001', 'interest':'1000', 'educational':'1100', 'marketing':'0110',
                            'internal':'1211', 'workforce':'1000', 'creative':'1000', 'research':'1000'};
      $(function () {
        $('input.quickbutton').click(function () {
          $('input.quickbutton').removeClass('quickhilite');
          var quickName = $(this).attr('name');
          if (typeof quickSelection[quickName] != 'undefined') {
            if (quickSelection[quickName].length == 4) {
              for (var qI = 0; qI < 4; qI ++) {
                var quickValue = 1 * quickSelection[quickName][qI];
                $('[name='+quickOrder[qI]+']')[quickValue].checked = true;
              }
            }
          }
          $(this).addClass('quickhilite');
        });
        $('input.quicktype').click(function () {
          switch ($(this).attr('value')) {
            case 'open':
              $('[name=join_mode]')[0].checked = true;
              break;
            case 'invite':
              $('[name=join_mode]')[2].checked = true;
              break;
          }
        });
      });
    </script>
    <form id="quick_group">
      <table class="">
        <tr class="padding">
          <td colspan="2">What type of group would you like to create?</td>
        </tr>
        <tr class="padding">
          <td>Open <input type="radio" name="quick_type" class="quicktype" value="open" /></td>
          <td>Invite only <input type="radio" name="quick_type" class="quicktype" value="invite" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="news" value="News Organisation" /></td>
          <td><input class="button quickbutton" type="button" name="interest" value="Interest Group" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="educational" value="Educational Establishment" /></td>
          <td><input class="button quickbutton" type="button" name="marketing" value="Marketing" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="internal" value="Internal Communications" /></td>
          <td><input class="button quickbutton" type="button" name="workforce" value="Workforce" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="creative" value="Creative Collaboration" /></td>
          <td><input class="button quickbutton" type="button" name="research" value="Research" /></td>
        </tr>
        <tr class="padding">
          <td colspan="2">Info here!</td>
        <tr>
        <tr>
          <td colspan="2">More Info Here!</td>
        <tr>
      </table>
    </form>
</%def>


##------------------------------------------------------------------------------
## Deprication
##------------------------------------------------------------------------------

<%doc>
    Radio button temp example
    <%
    if ():
        type_selected = "checked='checked' "
    else:
        type_selected = ""
    %>
    ##<option value="${newsarticle_type.id}" ${type_selected}>${newsarticle_type.type}</option>
    <input type="radio" name="newsarticle_type" value="${newsarticle_type.id}" ${type_selected}/>${newsarticle_type.type}</a>
</%doc>
