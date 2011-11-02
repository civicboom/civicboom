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
        
        def get_param(name, default=''):
            if 'settings' in d and name in d['settings']:
                return d['settings'][name]
            return default
    %>
    <%def name="show_error(name)">
        % if 'invalid' in d and name in d['invalid']:
            <br /><span class="error-message error">${d['invalid'][name]}</span>
        % endif
    </%def>
    <%def name="show_errors(*names)">
        % if 'invalid' in d and set(names).intersection(set(d['invalid'].keys())):
            <br /><span class="error-message error">${_('Error')}</span>
        % endif
    </%def>


    ## Setup Form
    <%
        if 'action' not in d or c.controller == 'groups':
            d['action'] = 'edit'
    %>
    % if c.action != 'new' and c.controller !='groups':
        ## Editing Form
        ${h.form(h.url('setting', id=c.result.get('id', 'me')), method='PUT' , multipart=True)}
    % else:
        ## Creating Form
        ${h.form(h.url('groups', )                 , method='POST', multipart=True)}
    % endif
    <div style="display:none"><input type="hidden" name="panel" value="${c.result.get('panel')}" /></div>
    <div class="group_settings">
        <h1>
            % if c.controller == 'groups':
                ${_('Great! You want to create a _Group...')}<br />
                ${_('To do this fill out the following:')}
            % endif
        </h1>
        <!-- <a href="${h.url(controller='misc', action='what_is_a_hub')}">${_('What is a _Group?')}</a> -->

        <div id="accordion">
            <h4>1. ${_("Describe the _Group")}</h4>
            <div>
                <table>
                    <tr>
                        <td>
                            ${show_error('name')}
                            ${show_error('username')}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="group_name">${_('Choose the _Group name:')}</label>
                            <br><input class="group-edit" type="text" id="group_name" name="name" value="${get_param('name')}" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="group_description">${_("Describe what it's about:")}</label>
                            <br><textarea class="group-edit" name="description" id="group_description"
                                placeholder="${_('This will have text that will be a top line description of what this _Group could be for.')}">${get_param('description')}</textarea>
                            ${show_error('description')}

                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="website">${_('Website (Optional):')}</label>
                            <br><input type="text" name="website" id="website" value="${get_param('website')}" />
                            ${show_error('website')}

                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="avatar">${_('Avatar (Optional):')}</label>
                            <br><input type="file" name="avatar" id="avatar" />
                            ${show_error('avatar')}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            % if c.action == 'new':
                                <label for="create_push_assignment">${_("Receive stories directly (Optional):")}</label>
                                <br><input type="checkbox" name="create_push_assignment" id="create_push_assignment" />
                                ${_('Create an automatic "Send us your stories" _assignment')}
                            % endif
                        </td>
                    </tr>
                </table>
            </div>
                
            <h4>2. ${_('Choose how people should join the _Group')}</h4>
            <div>
                <table>
                    <tr>
                        <td></td>
                        <td>
                            ${show_error('join_mode')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="join_mode" ${'checked="checked"' if get_param('join_mode', 'invite_and_request') == 'invite_and_request' else ''} value="invite_and_request" id="join_mode_invite_and_request" />
                        </td>
                        <td>
                            <label for="join_mode_invite_and_request">${_('Request to join')}</label>
                            <br>${_('Anyone can request to join. Administrators have to approve the request')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite' else ''} value="invite" id="join_mode_invite" />
                        </td>
                        <td>
                            <label for="join_mode_invite">${_('Invitation only')}</label>
                            <br>${_('An administrator must invite members to join. The members can then accept the invitation')}
                        </td>
                    </tr>
                </table>
            </div>
                
            <h4>3. ${_('Set default permissions for new _users')}</h4>
            <div>
                <table>
                    <tr>
                        <td></td>
                        <td>
                            ${show_error('default_role')}
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            ${_('By creating this _Group you are automatically set as an Administrator, what should other members be by default?')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="default_role" ${'checked=checked' if get_param('default_role', 'observer') == 'observer' else ''} value="observer" id="default_role_observer" />
                        </td>
                        <td>
                            <label for="default_role_observer">${_('Observer')}</label>
                            <br>${_('can view drafts and make comments.')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'contributor' else ''} value="contributor" id="default_role_contributor" />
                        </td>
                        <td>
                            <label for="default_role_contributor">${_('Contributor')}</label>
                            <br>${_('ability to create and edit drafts.')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'editor' else ''} value="editor" id="default_role_editor" />
                        </td>
                        <td>
                            <label for="default_role_editor">${_('Editor')}</label>
                            <br>${_('ability to publish _assignments.')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="default_role" ${'checked="checked"' if get_param('default_role') == 'admin' else ''} value="admin" id="default_role_admin" />
                        </td>
                        <td>
                            <label for="default_role_admin">${_('Administrator')}</label>
                            <br>${_('the ability to invite others to join Hub and set member roles.')}
                        </td>
                    </tr>
                </table>
            </div>
                
            % if c.logged_in_persona.has_account_required('plus'):
            <h4>4. ${_('Member & content visibility')}</h4>
            <div>
                <table>
                    <tr>
                        <td></td>
                        <td>
                            ${show_errors('member_visibility', 'default_content_visibility')}
                            ${show_error('member_visibility')}
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="member_visibility" ${'checked="checked"' if get_param('member_visibility', 'public') == 'public' else ''} value="public" id="member_visibility_public" />
                        </td>
                        <td>
                            <label for="member_visibility_public">${_('Member list visible')}</label>
                            <br>Members of this Hub will be visible to anyone who views it - even if they are not a member.
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'private' else ''} value="private" id="member_visibility_private" />
                        </td>
                        <td>
                            <label for="member_visibility_private">${_('Member list hidden')}</label>
                            <br>${_("Only administrators will see who has joined the _group")}
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td>
                            <!--
                            <h3>${_("Content default visibility")}</h3>
                            ${show_error('default_content_visibility')}
                            -->
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility', 'public') == 'public' else ''} value="public" id="content_visibility_public" />
                        </td>
                        <td>
                            <label for="content_visibility_public">${_('Content should be public by default')}</label>
                            <br>Anyone can see published content unless explicitly hidden.
                        </td>
                    </tr>
                    <tr>
                        <td class="radio">
                            <input type="radio" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'private' else ''} value="private" id="content_visibility_private" />
                        </td>
                        <td>
                            <label for="content_visibility_private">${_('Content should be members-only by default')}</label>
                            <br>Content of this Hub will be hidden from the public unless explicitly shown.
                        </td>
                    </tr>
                </table>
            </div>
            % endif
        </div>
        <div class="fl" style="width: 17em; padding-top: 1em;">
            ${_('By clicking "%s" you confirm that you have read and accepted the ' % (_('Save _Group') if c.action != 'new' and c.controller != 'groups' else _('Create _Group')))} <a href="#" onclick="$(this).siblings('.terms_and_conds').modal(); return false;">${_('terms and conditions')}</a>.
            ${popup.popup_static('terms and conditions', terms_and_conds, '', html_class="terms_and_conds")}
            
        </div>
        <div class="fr" style="padding-top: 1em;">
            % if c.action != 'new' and c.controller != 'groups':
                <input type="submit" name="submit" value="${_('Save _Group')}" class="button" />
            % else:
                <input type="submit" name="submit" value="${_('Create _Group')}" class="button" />
            % endif
        </div>

        <script>
        $(function() {
            $("#accordion").accordion();
        });
        </script>
        <div class="cb"></div>
    </div>
    
    ${h.end_form()}
    
    ## AllanC - disabled for now .. still working on it, had other prioritys
    % if c.controller == 'settings':
        ## AllanC - by vertue of the fact they can see this page, they are already an administrator
        <br />
        ${h.secure_link(
            ##h.args_to_tuple('group', id=d['username'], format='redirect'),
            h.url('group', id=d['username']),
            method = "DELETE",
            value           = _("Delete _group"),
            confirm_text    = _("Are your sure you want to delete this group? (All content published by this group will be deleted. All members will be notified)"),
            ##json_form_complete_actions = "cb_frag_reload('%s', current_element); cb_frag_remove(current_element);" % h.url('member', id=self.id),
        )}
    % endif
</%def>

<%def name="terms_and_conds()">
    <div class="information">
        <div class="popup-title">
            Hub terms and conditions:
        </div>
        <div class="popup-message" style="white-space: nowrap; padding-right:1.5em;">
            ${_('''
            I warrant to Indiconews Ltd (owner of _site_name) that I have permissions<br />
            and rights to create this _Group. I also confirm that any logo/image I upload does<br />
            not infringe upon any trademarks, third party copyrights, other such rights or<br />
            violate the user agreement. I hereby grant to Indiconews Ltd a non-exclusive,<br />
            non-transferable license during the term of this Agreement to copy, use and<br />
            display on Civicboom any logos or trademarked materials provided for this _Group.<br />
            ''') | n}
        </div> 
    </div>
</%def>
