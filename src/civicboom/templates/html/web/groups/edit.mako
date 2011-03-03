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
    ${frag.frag_basic(title=_('%s _Group') % c.action.capitalize(), icon='group', frag_content=group_content)}
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
            <span class="error-message error">${d['invalid'][name]}</span>
        % endif
    </%def>


    ## Setup Form
    <%
        if 'action' not in d:
            d['action'] = 'create'
    %>
    % if d['action']=='edit' and 'group' in d:
        ## Editing Form
        ${h.form(h.url('group', id=get_param('id')), method='PUT' , multipart=True)}
    % else:
        ## Creating Form
        ${h.form(h.url('groups', )                 , method='POST', multipart=True)}
    % endif


    
    <fieldset>
  		<!--<legend>${_("_Group")}</legend>-->
  		<table class="group-table">
  			<tr class="padding">
  				<td colspan="2">${_("_Group name")}</td>
  				<td colspan="5">
  		      <input class="group-edit" type="text" name="name" value="${get_param('name')}" placeholder="${_('Enter the public name of your _Group here')}"/>
          ${show_error('name')}
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
  				<td style="width: 20px">&nbsp;</td>
  				<td colspan="5">
            <input type="radio" class="quickchange" name="default_role" ${'checked="checked"' if get_param('default_role') == 'observer' else ''} value="observer" id="default_role_observer" /><label for="default_role_observer">${_('Observer')}</label>
            <span class="role_description"> - ${_('a member of a _Group who can only view content/drafts and comment')}</span>
          </td>
          <td style="width: 20px">&nbsp;</td>
        </tr>
        <tr>
          <td style="width: 20px">&nbsp;</td>
          <td colspan="5">
            <input type="radio" class="quickchange" name="default_role" ${'checked="checked"' if get_param('default_role') == 'contributor' else ''} value="contributor" id="default_role_contributor" /><label for="default_role_contributor">${_('Contributor')}</label>
            <span class="role_description"> - ${_('a member who can do the above and create and edit drafts')}</span>
          </td>
          <td style="width: 20px">&nbsp;</td>
        </tr>
        <tr>
          <td style="width: 20px">&nbsp;</td>
          <td colspan="5">
            <input type="radio" class="quickchange" name="default_role" ${'checked="checked"' if get_param('default_role') == 'editor' else ''} value="editor" id="default_role_editor" /><label for="default_role_editor">${_('Editor')}</label>
            <span class="role_description"> - ${_('a member who can do the above plus publish content')}</span>
          </td>
          <td style="width: 20px">&nbsp;</td>
        </tr>
        <tr class="padding">
          <td style="width: 20px">&nbsp;</td>
          <td colspan="5">
            <input type="radio" class="quickchange" name="default_role" ${'checked="checked"' if get_param('default_role') == 'admin' else ''} value="admin" id="default_role_admin" /><label for="default_role_admin">${_('Administrator')}</label>
            <span class="role_description"> - ${_('a member who can do the above and invite others to join and set member roles')}</span><br />
          ${show_error('default_role')}
  				</td>
  				<td style="width: 20px">&nbsp;</td>
  			</tr>
  			<tr class="padding">
  			  <td colspan="7" style="text-align: center;">
  			    ${_('Note: By creating this _Group you are automatically set as an Administrator.')}
  			  </td>
  			</tr>
  			<tr class="padding">
          <td colspan="7">${_("Join mode")}</td>
  			</tr>
  			<tr class="padding">
          <td>&nbsp;</td>
          <td>
            <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'public' else ''} value="public" id="join_mode_public" /><label for="join_mode_public">${_('Open?')}</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite_and_request' else ''} value="invite_and_request" id="join_mode_invite_and_request" /><label for="join_mode_invite_and_request">${_('Public?')}</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite' else ''} value="invite" id="join_mode_invite" /><label for="join_mode_invite">${_('Private?')}</label><br />
          </td>
          <td colspan="3">
            ${show_error('join_mode')}
          </td>
        </tr>
        <tr class="padding">
          <td colspan="4">${_("Member visibility")}</td>
          <td colspan="3"><!--${_("Default content visibility")}--></td>
        </tr>
        <tr class="padding">
          <td>&nbsp;</td>
          <td>
            <input type="radio" class="quickchange" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'public' else ''} value="public" id="member_visibility_public" /><label for="member_visibility_public">${_('Open')}</label>
          </td>
          <td>
            <input type="radio" class="quickchange" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'private' else ''} value="private" id="member_visibility_private" /><label for="member_visibility_private">${_('Hidden')}</label>
          </td>
          <td style="width: 20px">
            ${show_error('member_visibility')}
          </td>
          <td>
            <!--<input type="radio" class="quickchange" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'public' else ''} value="public" id="content_visibility_public" /><label for="content_visibility_public">${_('Open')}</label>-->
          </td>
          <td>
            <!--<input type="radio" class="quickchange" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'private' else ''} value="private" id="content_visibility_private" /><label for="content_visibility_private">${_('Hidden')}</label>-->
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
##        <tr class="padding">
##          <td colspan="2"><label for="logo_file">or</label></td>
##          <td colspan="5">&nbsp;</td>
##        </tr>
##        <tr class="padding">
##          <td colspan="2"><label for="logo_url">${_('Logo URL:')}</label></td>
##          <td colspan="4"><input type="text" name="logo_url" id="logo_url" /></td>
##          <td>&nbsp;</td>
##        </tr>
          <td colspan="5"><label for="permission">${_('This _Group represents an organisation and I have the permissions/rights to create it.')}</label></td>
          <td><input type="checkbox" name="permission" id="permission"/>
          <td>&nbsp;</td>
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

##------------------------------------------------------------------------------
## Quick group
##------------------------------------------------------------------------------

<%def name="quick_group()">
    ${frag.frag_basic(title=_('Quick _Group'), icon='group', frag_content=quick_group_content)}
</%def>
<%def name="quick_group_content()">
    <script type="text/javascript">
      var quickOrder = ['default_role', 'join_mode', 'member_visibility']; //'default_content_visibility' 0,0,0,1,1,1,0,1
      var quickSelection = {'news': '001',
                            'interest':'110',
                            'educational':'220',
                            'marketing':'010',
                            'internal':'221',
                            'business':'221',
                            'creative':'001',
                            'research':'210'};
      var quickBlurb =     {'news': '${_("Connect with your community and audience by creating _Groups for your titles, sections or issues. Send out breaking news requests, get coverage directly from the source and utilise the power of the crowd. Empower the community you serve to be part of news and its creation.")}',
                            'interest':'${_("Create a _Group and crowdsource social action, motivate advocacy from your community, generate real case studies and stories for your publications, heighten awareness, build a movement. Use the creativity of your community to heighten awareness on issues you need to know about.")}',
                            'educational':'${_("Students can create _Groups on specific topics - evolve ideas together, share your creative work, tap into the wider community, build your portfolio. University departments can utilise the collective wisdom of their students to develop and improve courses and reach new audiences.")}',
                            'marketing':'${_("Get first hand experience and feedback directly form your customers and target audiences. What products do your consumers want? How can you improve? Set requests through your _Group and ask the crowd.")}',
                            'internal':'${_("Create a private _Group and empower your employees to submit ideas, upload their reports from events, share experiences - good and bad. Identify champions, learn from your workforce: they have the insight to help make your workplace and business better for all.")}',
                            'business':'${_("Work with your partners and customers: use _Groups to push out new products, get engagement on hot topics associated with your industry, build a community around your brand, and improve brand awareness to wider audiences.")}',
                            'creative':'${_("From documentary makers to designers and everything in between, ask the crowd - photos, text, videos, audio. Empower people to share their experience, authenticity and creativity for your project through a _Group.")}',
                            'research':'${_("Work in a closed, private _Group with key people in your organisation or trusted external sources in research on any topic you choose.")}' };
      function changePlaceholder (jquery_object, text) {
        if (typeof text === 'undefined') var text = '';
        var oldPlaceholder = jquery_object.attr('placeholder'); 
        jquery_object.attr('placeholder', text);
        if ((!Modernizr.input.placeholder) && (jquery_object.val() === oldPlaceholder))
          jquery_object.val(jquery_object.attr('placeholder'));
      }
      $(function () {
      var defaultDescPlaceholder = $('textarea#group_description').attr('placeholder');
        if (!Modernizr.input.placeholder) {
          if ($('textarea#group_description').val() == '')
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
            if (quickSelection[quickName].length == quickOrder.length) {
              for (var qI = 0; qI < quickOrder.length; qI ++) {
                var quickValue = 1 * quickSelection[quickName][qI];
                $('[name='+quickOrder[qI]+']')[quickValue].checked = true;
                quickHilite = true;
              }
            }
          }
          changePlaceholder ($('#group_description'), quickBlurb[quickName]);
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
          for (var qI = 0; qI < quickOrder.length; qI ++) {
            quickString = quickString + $('[name='+quickOrder[qI]+']').index($('[name='+quickOrder[qI]+']:checked'));
          }
          $('td.quickchangehilite').removeClass('quickchangehilite');
          if (hiliteQuickButtons (quickString)) $('.quickchange:checked').parents('td').addClass('quickchangehilite');
          changePlaceholder ($('#group_description'), defaultDescPlaceholder);
        });
      });
    </script>
    <form id="quick_group">
      <table class="">
        <tr class="padding">
         <td colspan="2" class="bold bigger">Need help?</td>
        </tr>
        <tr class="doublepadding">
          <td colspan="2">${_('By clicking on one of the buttons below, you can create a "Quick _Group", which will have pre-set defaults. (Try it out, click on a button and see the highlighted changes!)')}</td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="news" value="${_('News Organisation')}" /></td>
          <td><input class="button quickbutton" type="button" name="interest" value="${_('Interest Group / Charity')}" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="educational" value="${_('Educational Establishment')}" /></td>
          <td><input class="button quickbutton" type="button" name="marketing" value="${_('Marketing')}" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="internal" value="${_('Internal Communications')}" /></td>
          <td><input class="button quickbutton" type="button" name="business" value="${_('Business')}" /></td>
        </tr>
        <tr class="doublepadding">
          <td><input class="button quickbutton" type="button" name="creative" value="${_('Creative Collaboration')}" /></td>
          <td><input class="button quickbutton" type="button" name="research" value="${_('Research')}" /></td>
        </tr>
        <tr class="padding">
          <td colspan="2" class="bold bigger center">OR</td>
        </tr>
        <tr>
          <td colspan="2" class="bold big">${_('Create your own _Group by filling in the form to suit your needs.')}</td>
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
