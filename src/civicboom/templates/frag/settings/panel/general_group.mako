<%inherit file="/frag/common/frag.mako"/>
<%namespace name="popup" file="/html/web/common/popup_base.mako" />

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
            <br /><span class="error-message error">${d['invalid'][name]}</span>
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
    <!-- Toggle Section -->
    <script type="text/javascript">
        var icon_more = 'icon_plus';
        var icon_less = 'icon_down';
        function toggle_edit_section(jquery_element) {
            $(jquery_element).next().slideToggle();
            var icon = $(jquery_element).find('.icon');
            if (icon.hasClass('icon_plus')) {
                icon.removeClass(icon_more);
                icon.addClass(icon_less);
            }
            else if (icon.hasClass(icon_less)) {
                icon.removeClass(icon_less);
                icon.addClass(icon_more);
            }
        }
    </script>
    <div class="group_settings">
        <h1>
            ${_('Great! You want to create a _Group...')}<br />
            ${_('To do this fill out the following:')}
        </h1>
        ##<a href="">${_('What is a _Group?')}</a>
        <br /><br />
                <div>
                    <div class="number fl">1.</div>
                    <div class="group-block">
                        <label for="group_name">${_('Choose the _Group name:')}</label>
                        <input class="group-edit" type="text" id="group_name" name="name" value="${get_param('name')}" />
                        ${show_error('name')} ${show_error('username')}
                    </div>
                </div>
                <div class="number fl">2.</div>
                <div class="group-block">
                    <label for="group_description">${_("Describe what it's about:")}</label>
                    <textarea class="group-edit" name="description" id="group_description" placeholder="${_('This will have text that will be a top line description of what this _Group could be for.')}">${get_param('description')}</textarea><br />
                    ${show_error('description')}
                </div>
                <h3>${_('Optional:')}</h3>
                <div class="group-block">
                    <label for="website">${_('Website:')}</label>
                    <input type="text" name="website" id="website" value="${get_param('website')}" />
                    ${show_error('website')}
                </div>
                <div class="group-block">
                    <label for="avatar">${_('Avatar:')}</label>
                    <input type="file" name="avatar" id="avatar" />
                    ${show_error('avatar')}
                </div>
                <span class="number fl">3.</span>
                <div class="group-block">
                    <legend onclick="toggle_edit_section($(this));" class="edit_input">
                        <span class="label">${_('When others join your _Group what default role do you want them to have?')}</span>
                        <span class="icon16 i_plus"></span>
                    </legend>
                    <div class="hideable">
                        ${show_error('default_role')}
                        <ul>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'observer' else ''} value="observer" id="default_role_observer" />
                                    <label for="default_role_observer">${_('Observer')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Minimum access:</span>
                                    they can view drafts and comment on them.
                                </div>
                            </li>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'contributor' else ''} value="contributor" id="default_role_contributor" />
                                    <label for="default_role_contributor">${_('Contributor')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Basic access:</span>
                                    the above plus ability to create and edit drafts.
                                </div>
                            </li>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'editor' else ''} value="editor" id="default_role_editor" />
                                    <label for="default_role_editor">${_('Editor')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Medium access:</span>
                                    the above plus ability to post requests.
                                </div>
                            </li>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="radio" name="default_role" ${'checked="checked"' if get_param('default_role') == 'admin' else ''} value="admin" id="default_role_admin" />
                                    <label for="default_role_admin">${_('Administrator')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Maximum access:</span>
                                    the above plus the ability to invite others to join Hub and set member roles.
                                </div>
                            </li>
                        </ul>
                        ${_('Note: By creating this _Group you are automatically set as an Administrator.')}
                    </div>
                </div>
                <span class="number fl">4.</span>
                <div class="group-block">
                    <legend onclick="toggle_edit_section($(this));" class="edit_input">
                        <span class="label">${_('How do you want others to join this _Group?')}</span>
                        <span class="icon16 i_plus"></span>
                    </legend>
                    <div class="hideable">
                        ${show_error('join_mode')}
                        <ul>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'public' else ''} value="public" id="join_mode_public" />
                                    <label for="join_mode_public">${_('Open')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Minimum control:</span>
                                    Anyone can join this Hub and become a member as per default role setting. This means anyone beyond your chosen Hub members will be part of your "identity".
                                    <span class="error">Do not create an open Hub if you are not prepared for general access. For tighter join modes please see Public and Private options.</span>
                                </div>
                            </li>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite_and_request' else ''} value="invite_and_request" id="join_mode_invite_and_request" />
                                    <label for="join_mode_invite_and_request">${_('Public')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Medium control:</span>
                                    Anyone can request to join this Hub, and you can invite other's to join. You also have the ability to accept or decline requests to join.
                                </div>
                            </li>
                            <li>
                                <div class="fl">
                                    <input type="radio" class="quickchange" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite' else ''} value="invite" id="join_mode_invite" />
                                    <label for="join_mode_invite">${_('Private')}</label>
                                </div>
                                <div class="radio-right">
                                    <span class="b">Maximum control:</span>
                                    This gives you strictest control of who joins your Hub. It is invite only and as an administrator you decide who to invite.
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="${'' if c.logged_in_persona.has_account_required('plus') else 'disabled'}">
                    <span class="number fl">5.</span>
                    <div class="group-block">
                        <div class="fl">
                            <legend onclick="toggle_edit_section($(this));" class="edit_input">
                                <span class="label">${_('Member & content visibility')}</span>
                                <span class="icon16 i_plus"></span>
                                % if not c.logged_in_persona.has_account_required('plus'):
                                    <div class="upgrade">
                                        This requires a plus account. Please <a href="${h.url(controller='about', action='upgrade_plans')}">upgrade</a> if you want access to this feature
                                    </div>
                                % endif
                            </legend>
                            <div class="hideable">
                                % if c.logged_in_persona.has_account_required('plus'):
                                    <h3>${_("Member visibility")}</h3>
                                    ${show_error('member_visibility')}
                                    <ul>
                                        <li>
                                            <div class="fl">
                                                <input type="radio" class="quickchange" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'public' else ''} value="public" id="member_visibility_public" />
                                                <label for="member_visibility_public">${_('Open')}</label>
                                            </div>
                                            <div class="radio-right">
                                                Members of this Hub will be visible to anyone who views it - even if they are not a member.
                                            </div>
                                        </li>
                                        <li>
                                            <div class="fl">
                                                <input type="radio" class="quickchange" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'private' else ''} value="private" id="member_visibility_private" />
                                                <label for="member_visibility_private">${_('Hidden')}</label>
                                            </div>
                                            <div class="radio-right">
                                                Members of this Hub will be hidden to anyone viewing it - except administrators of the Hub.
                                            </div>
                                        </li>
                                    </ul>
                                    <h3>${_("Content default visibility")}</h3>
                                    ${show_error('default_content_visibility')}
                                    <ul>
                                        <li>
                                            <div class="fl">
                                                <input type="radio" class="quickchange" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'public' else ''} value="public" id="content_visibility_public" />
                                                <label for="content_visibility_public">${_('Open')}</label>
                                            </div>
                                            <div class="radio-right">
                                                Content created by this Hub will be visible to anyone who views it - even if they are not a member.
                                            </div>
                                        </li>
                                        <li>
                                            <div class="fl">
                                                <input type="radio" class="quickchange" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'private' else ''} value="private" id="content_visibility_private" />
                                                <label for="content_visibility_private">${_('Hidden')}</label>
                                            </div>
                                            <div class="radio-right">
                                                Content of this Hub will be hidden to anyone viewing it - except administrators of the Hub.
                                            </div>
                                        </li>
                                    </ul>
                                % endif
                            </div>
                        </div>
                        <div class="cb"></div>
                   </div>
               </div>

<<<<<<< HEAD
        <div class="fl" style="width: 17em; padding-top: 1em;">
            By clicking "Create Hub" you confirm that you have read and accepted the <a onclick="$(this).siblings('.terms_and_conds').modal(); return false;"><u>terms and conditions</u></a>.
            ${popup.popup_static('terms and conditions', terms_and_conds, '', html_class="terms_and_conds")}
        </div>
        <div class="fr" style="padding-top: 1em;">
            % if d['action']=='edit':
                <input type="submit" name="submit" value="${_('Save _Group')}" class="button" />
            % else:
                <input type="submit" name="submit" value="${_('Create _Group')}" class="button" />
            % endif
        </div>
        <div class="cb"></div>
    </div>
=======
    
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
>>>>>>> 7d913780f3aa6a7a3953ec21f7e1e990a3a2cc21
    
    ${h.end_form()}
</%def>

<%def name="terms_and_conds()">
    <div class="information">
        <div class="popup-title">
            Hub terms and conditions:
        </div>
        <div class="popup-message" style="white-space: nowrap; padding-right:1.5em;">
            I warrant to Indiconews Ltd (owner of Civicboom.com) that I have permissions<br />
            and rights to create this Hub. I also confirm that any logo/image I upload does<br />
            not infringe upon any trademarks, third party copyrights, other such rights or<br />
            violate the user agreement. I hereby grant to Indiconews Ltd a non-exclusive,<br />
            non-transferrable license during the term of this Agreement to copy, use and<br />
            display on Civicboom any logos or trademarked materials provided for this Hub.<br />
        </div> 
    </div>
</%def>
