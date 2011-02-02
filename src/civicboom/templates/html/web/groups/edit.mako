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
  				<td colspan="2">${_("Group name")}</td>
  				<td colspan="5">
  		      <input class="group-edit" type="text" name="name" value="${get_param('name')}" placeholder="Enter the public name of your Group here"/>
          ${show_error('name')}
  				</td>
  			</tr>
  			<tr class="padding">
  				<td colspan="2">${_("Description")}<br />Who it's for<br />and purpose</td>
  				<td colspan="5">
  		      <textarea class="group-edit" name="description" id="group_description" placeholder="One two three">${get_param('description')}</textarea><br />
            ${show_error('description')}
  				</td>
  			</tr>
  			<tr class="padding">
  			  <td colspan="7">${_("Default member role")}</td>
  			</tr>
  			<tr>
  				<td style="width: 20px">&nbsp;</td>
  				<td colspan="5">
            <input type="radio" class="quickchange" name="default_role" value="observer" id="default_role_observer" /><label for="default_role_observer">Observer</label>
            <span class="role_description"> - a member of a group who can only view content/drafts and comment</span>
          </td>
          <td style="width: 20px">&nbsp;</td>
        </tr>
        <tr>
          <td style="width: 20px">&nbsp;</td>
          <td colspan="5">
            <input type="radio" class="quickchange" name="default_role" value="contributor" id="default_role_contributor" /><label for="default_role_contributor">Contributor</label>
            <span class="role_description"> - a member who can do the above and create and edit drafts</span>
          </td>
          <td style="width: 20px">&nbsp;</td>
        </tr>
        <tr>
          <td style="width: 20px">&nbsp;</td>
          <td colspan="5">
            <input type="radio" class="quickchange" name="default_role" value="editor" id="default_role_editor" /><label for="default_role_editor">Editor</label>
            <span class="role_description"> - a member who can do the above plus publish content</span>
          </td>
          <td style="width: 20px">&nbsp;</td>
        </tr>
        <tr class="padding">
          <td style="width: 20px">&nbsp;</td>
          <td colspan="5">
            <input type="radio" class="quickchange" name="default_role" value="admin" id="default_role_admin" /><label for="default_role_admin">Administrator</label>
            <span class="role_description"> - a member who can do the above and invite others to join and set member roles</span><br />
          ${show_error('default_role')}
  				</td>
  				<td style="width: 20px">&nbsp;</td>
  			</tr>
  			<tr class="padding">
  			  <td colspan="7" style="text-align: center;">
  			    Note: By creating this Group you are automatically set as an Administrator.
  			  </td>
  			</tr>
  			<tr class="padding">
          <td colspan="7">${_("Join mode")}</td>
  			</tr>
  			<tr class="padding">
          <td>&nbsp;</td>
          <td>
            <input type="radio" class="quickchange" name="join_mode" value="public" id="join_mode_public" /><label for="join_mode_public">Open?</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="join_mode" value="invite_and_request" id="join_mode_invite_and_request" /><label for="join_mode_invite_and_request">Public?</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="join_mode" value="invite" id="join_mode_invite" /><label for="join_mode_invite">Private?</label><br />
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
            <input type="radio" class="quickchange" name="content_visibility" value="public" id="content_visibility_public" /><label for="content_visibility_public">Open</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="content_visibility" value="private" id="content_visibility_private" /><label for="content_visibility_private">Hidden</label>
          </td>
          <td>${show_error('default_content_visibility')}</td>
          <td>
            <input type="radio" class="quickchange" name="member_visibility" value="public" id="member_visibility_public" /><label for="member_visibility_public">Open</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="member_visibility" value="private" id="member_visibility_private" /><label for="member_visibility_private">Hidden</label>
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
          <td colspan="6">I can also confirm that by clicking "Create" I have read and accepted the <a href="http://localhost/about/terms">terms and conditions</a> associated with creating a Group.</td>
          <td>&nbsp;</td>
        </tr>
  			<tr>
  				<td colspan="7" style="text-align: right;">
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
      var quickSelection = {'news': '0001',
                            'interest':'1100',
                            'educational':'2200',
                            'marketing':'0110',
                            'internal':'2211',
                            'workforce':'2211',
                            'creative':'0001',
                            'research':'2110'};
      var quickBlurb =     {'news': 'This is a news blurb',
                            'interest':'This is an interest blurb',
                            'educational':'This is an educational blurb',
                            'marketing':'This is a marketing blurb',
                            'internal':'This is an internal blurb',
                            'workforce':'This is a workforce blurb',
                            'creative':'This is a creative blurb',
                            'research':'This is a research blurb'};
      $(function () {
        if (!Modernizr.input.placeholder) {
          $('textarea#group_description').val($('textarea#group_description').attr('placeholder'));
          $('textarea#group_description').focus(function (e) {
            $(this).val('');
          });
          $('textarea#group_description').blur(function (e) {
            if ($(this).val() === '') $(this).val($(this).attr('placeholder'));
          });
          $('textarea#group_description').parents('form').submit(function (e) {
            if ($('textarea#group_description').val() === $('textarea#group_description').attr('placeholder')) $('textarea#group_description').val('');
          });
        }
        $('input.quickbutton').click(function () {
          var quickHilite = false
          $('td.quickchangehilite').removeClass('quickchangehilite');
          var quickName = $(this).attr('name');
          if (typeof quickSelection[quickName] != 'undefined') {
            if (quickSelection[quickName].length == 4) {
              for (var qI = 0; qI < 4; qI ++) {
                var quickValue = 1 * quickSelection[quickName][qI];
                $('[name='+quickOrder[qI]+']')[quickValue].checked = true;
                quickHilite = true;
              }
            }
          }
          ## Set placeholder (if not HTML5 update value if eq to old placeholder!)
          var oldPlaceholder = $('#group_description').attr('placeholder'); 
          $('#group_description').attr('placeholder', quickName);
          if ((!Modernizr.input.placeholder) && ($('#group_description').val() === oldPlaceholder))
            $('#group_description').val($('#group_description').attr('placeholder'));
          if (quickHilite) $('.quickchange:checked').parents('td').addClass('quickchangehilite');
          hiliteQuickButtons (quickSelection[quickName]);
        });
        
        function hiliteQuickButtons (quickString) {
          var quickHilite = false;
          $('.quickbutton').removeClass('quickhilite');
          for (var qS in quickSelection) {
            if (quickSelection[qS] == quickString) {
              $('.quickbutton[name='+qS+']').addClass('quickhilite');
              quickHilite = true;
            }
          }
          return quickHilite;
        }
        $('input.quickchange').click(function () {
          var quickString = '';
          for (var qI = 0; qI < 4; qI ++) {
            quickString = quickString + $('[name='+quickOrder[qI]+']').index($('[name='+quickOrder[qI]+']:checked'));
          }
          $('td.quickchangehilite').removeClass('quickchangehilite');
          if (hiliteQuickButtons (quickString)) $('.quickchange:checked').parents('td').addClass('quickchangehilite');
        });
      });
    </script>
    <form id="quick_group">
      <table class="">
        <tr class="padding">
         <td colspan="2" class="bold bigger">Need help?</td>
        <tr>
        <tr class="doublepadding">
          <td colspan="2">By clicking on one of the buttons below, you can create a "quick group", which will have pre-set defaults.
          (Try it out, click on a button and see the highlighted changes!)</td>
        <tr>
##        <tr class="padding">
##          <td colspan="2">
##            Would you like to create a group for:
##          </td>
##        </tr>
##        <tr class="padding">
##          <td>Open <input type="radio" name="quick_type" class="quicktype" value="open" /></td>
##          <td>Invite only <input type="radio" name="quick_type" class="quicktype" value="invite" /></td>
##        </tr>
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
        <tr class="doublepadding">
          <td><input class="button quickbutton" type="button" name="creative" value="Creative Collaboration" /></td>
          <td><input class="button quickbutton" type="button" name="research" value="Research" /></td>
        </tr>
        <tr class="padding">
          <td colspan="2" class="bold bigger center">OR</td>
        </tr>
        <tr>
          <td colspan="2" class="bold big">Create your own group by filling in the form to suit your needs.</td>
        </tr>
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
