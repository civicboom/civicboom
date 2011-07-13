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
    % if c.action=='edit':
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
            % if not c.action=='edit':
                ${_('Great! You want to create a _Group...')}<br />
                ${_('To do this fill out the following:')}
            % endif
        </h1>
        <a href="${h.url(controller='misc', action='what_is_a_hub')}">${_('What is a _Group?')}</a>
        <br /><br />
                <fieldset>
                    <div class="number fl">1.</div>
                    <div class="group-block">
                        <label for="group_name">${_('Choose the _Group name:')}</label>
                        <input class="group-edit" type="text" id="group_name" name="name" value="${get_param('name')}" />
                        ${show_error('name')} ${show_error('username')}
                    </div>
                </fieldset>
                <fieldset>
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
                    <div class="group-block wide_label">
                        <label for="create_push_assignment">${_("Add an automatic 'Send your stories' request to this _Group's _Widget and profile?")}</label>
                        <input type="checkbox" name="create_push_assignment" id="create_push_assignment" />
                    </div>
                </fieldset>
                <fieldset>
                    <span class="number fl">3.</span>
                    <div class="group-block">
                        <div onclick="toggle_edit_section($(this));" class="edit_input">
                            <span class="label">${_('When others join your _Group what default role do you want them to have?')}</span>
                            <span class="icon16 i_plus"></span>
                        </div>
                        <div class="hideable">
                            ${show_error('default_role')}
                            <ul>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'observer' else ''} value="observer" id="default_role_observer" />
                                        <label for="default_role_observer">${_('Observer')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Minimum access:')}</span>
                                        ${_('they can view drafts and comment on them')}
                                    </div>
                                </li>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'contributor' else ''} value="contributor" id="default_role_contributor" />
                                        <label for="default_role_contributor">${_('Contributor')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Basic access:')}</span>
                                        ${_('the above plus ability to create and edit drafts.')}
                                    </div>
                                </li>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="default_role" ${'checked=checked' if get_param('default_role') == 'editor' else ''} value="editor" id="default_role_editor" />
                                        <label for="default_role_editor">${_('Editor')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Medium access:')}</span>
                                        ${_('the above plus ability to post requests.')}
                                    </div>
                                </li>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="default_role" ${'checked="checked"' if get_param('default_role') == 'admin' else ''} value="admin" id="default_role_admin" />
                                        <label for="default_role_admin">${_('Administrator')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Maximum access:')}</span>
                                        ${_('the above plus the ability to invite others to join Hub and set member roles.')}
                                    </div>
                                </li>
                            </ul>
                            ${_('Note: By creating this _Group you are automatically set as an Administrator.')}
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <span class="number fl">4.</span>
                    <div class="group-block">
                        <div onclick="toggle_edit_section($(this));" class="edit_input">
                            <span class="label">${_('How do you want others to join this _Group?')}</span>
                            <span class="icon16 i_plus"></span>
                        </div>
                        <div class="hideable">
                            ${show_error('join_mode')}
                            <ul>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'public' else ''} value="public" id="join_mode_public" />
                                        <label for="join_mode_public">${_('Open')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Minimum control:')}</span>
                                        ${_('Anyone can join this Hub and become a member as per default role setting. This means anyone beyond your chosen Hub members will be part of your "identity".')}
                                        <span class="error">${_('Do not create an open Hub if you are not prepared for general access. For tighter join modes please see Public and Private options.')}</span>
                                    </div>
                                </li>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite_and_request' else ''} value="invite_and_request" id="join_mode_invite_and_request" />
                                        <label for="join_mode_invite_and_request">${_('Public')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Medium control:')}</span>
                                        ${_('Anyone can request to join this Hub, and you can invite others to join. You also have the ability to accept or decline requests to join.')}
                                    </div>
                                </li>
                                <li>
                                    <div class="fl">
                                        <input type="radio" class="radio" name="join_mode" ${'checked="checked"' if get_param('join_mode') == 'invite' else ''} value="invite" id="join_mode_invite" />
                                        <label for="join_mode_invite">${_('Private')}</label>
                                    </div>
                                    <div class="radio-right">
                                        <span class="b">${_('Maximum control:')}</span>
                                        ${_('This gives you strictest control of who joins your Hub. It is invite only and as an administrator you decide who to invite.')}
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <div class="${'' if c.logged_in_persona.has_account_required('plus') else 'setting-disabled'}">
                        <span class="number fl">5.</span>
                        <div class="group-block">
                            <div class="fl">
                                <div onclick="toggle_edit_section($(this));" class="edit_input">
                                    <span class="label">${_('Member & content visibility')}</span>
                                    <span class="icon16 i_plus"></span>
                                    % if not c.logged_in_persona.has_account_required('plus'):
                                        <div class="upgrade">
                                            ${_('This requires a plus account. Please <a href="%s">upgrade</a> if you want access to this feature.') % (h.url(controller='about', action='upgrade_plans')) | n }
                                        </div>
                                    % endif
                                </div>
                                <div class="hideable">
                                    % if c.logged_in_persona.has_account_required('plus'):
                                        <h3>${_("Member visibility")}</h3>
                                        ${show_error('member_visibility')}
                                        <ul>
                                            <li>
                                                <div class="fl">
                                                    <input type="radio" class="radio" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'public' else ''} value="public" id="member_visibility_public" />
                                                    <label for="member_visibility_public">${_('Open')}</label>
                                                </div>
                                                <div class="radio-right">
                                                    Members of this Hub will be visible to anyone who views it - even if they are not a member.
                                                </div>
                                            </li>
                                            <li>
                                                <div class="fl">
                                                    <input type="radio" class="radio" name="member_visibility" ${'checked="checked"' if get_param('member_visibility') == 'private' else ''} value="private" id="member_visibility_private" />
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
                                                    <input type="radio" class="radio" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'public' else ''} value="public" id="content_visibility_public" />
                                                    <label for="content_visibility_public">${_('Open')}</label>
                                                </div>
                                                <div class="radio-right">
                                                    Content created by this Hub will be visible to anyone who views it - even if they are not a member.
                                                </div>
                                            </li>
                                            <li>
                                                <div class="fl">
                                                    <input type="radio" class="radio" name="default_content_visibility" ${'checked="checked"' if get_param('default_content_visibility') == 'private' else ''} value="private" id="content_visibility_private" />
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
                </fieldset>
        <div class="fl" style="width: 17em; padding-top: 1em;">
            ${_('By clicking "%s" you confirm that you have read and accepted the ' % (_('Save _Group') if c.action=='edit' else _('Create _Group')))} <a href="#" onclick="$(this).siblings('.terms_and_conds').modal(); return false;">${_('terms and conditions')}</a>.
            ${popup.popup_static('terms and conditions', terms_and_conds, '', html_class="terms_and_conds")}
        </div>
        <div class="fr" style="padding-top: 1em;">
            <% print c %>
            % if c.action=='edit':
                <input type="submit" name="submit" value="${_('Save _Group')}" class="button" />
            % else:
                <input type="submit" name="submit" value="${_('Create _Group')}" class="button" />
            % endif
        </div>
        <div class="cb"></div>
    </div>
    
    ${h.end_form()}
</%def>

<%def name="terms_and_conds()">
    <div class="information">
        <div class="popup-title">
            Hub terms and conditions:
        </div>
        <div class="popup-message" style="white-space: nowrap; padding-right:1.5em;">
            ${_('''
            I warrant to Indiconews Ltd (owner of Civicboom.com) that I have permissions<br />
            and rights to create this _Group. I also confirm that any logo/image I upload does<br />
            not infringe upon any trademarks, third party copyrights, other such rights or<br />
            violate the user agreement. I hereby grant to Indiconews Ltd a non-exclusive,<br />
            non-transferrable license during the term of this Agreement to copy, use and<br />
            display on Civicboom any logos or trademarked materials provided for this _Group.<br />
            ''') | n}
        </div> 
    </div>
</%def>
