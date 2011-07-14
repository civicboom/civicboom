<%inherit file="/frag/common/frag.mako"/>
<%namespace name="member_includes" file="/html/web/common/member.mako"     />

<%def name="member_avatar(member, img_class='')">
    ${member_includes.avatar(member, class_='thumbnail', img_class=img_class)}
</%def>

<%def name="body()">
    <div class="frag_col">
        <div class="new-article">
            <div class="frag_whitewrap">
                <h1>
                    ${_('Great! You want to post a story...')}<br />
                    ${_('You now have three choices:')}
                </h1>
            </div>
            <div class="frag_whitewrap na-orgs">
                <div class="h1 fl">1.</div>
                <div class="na-padleft">
                    <h1>${_('Post it directly to a news organisation for potential publication:')}</h1>
                    <ul>
                        % for org in d['list']:
                            <li class="mo-help">
                                <div class="fl">${member_avatar(org)}</div>
                                <div class="na-org-text">
                                    ${_('Post directly to %s') % org.get('name')}
                                </div>
                                <div class="pr">
                                    <div class="mo-help-l">
                                        ${org.get('description')}
                                    </div>
                                </div>
                                <div class="fr">${h.secure_link(
                                    h.args_to_tuple('new_content', parent_id=org.get('push_assignment')) ,
                                    value           = _("Post a story") ,
                                    value_formatted = h.literal("<span class='button'>%s</span>") % _('Post a story') ,
                                    json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , 
                                )}</div>
                                <div class="cb"></div>
                            </li>
                        % endfor
                    </ul>
                    <div style="padding: 1em 0;">
    ##                    ${_('Are you a news organisation? Do you want to get news directly from source?')}
    ##                    <a href="${h.url(controller='misc', action='hub_organisation')}">${_('Click here to learn how.')}</a>
                    </div>
                </div>
            </div>
            <div class="frag_whitewrap na-other">
                <div class="h1 fl">2.</div>
                <div class="na-padleft">
                    <h1 class="fl">${_('Post your story on Civicboom:')}</h1>
                    <div class="fr">${h.secure_link(h.url('new_content', target_type='article'   ), _("Post a story") , css_class="button")}</div>
                    <div class="cb"></div>
                </div>
            </div>
            <div class="frag_whitewrap na-other">
                <div class="h1 fl">3.</div>
                <div class="na-padleft">
                    <h1 class="fl">${_('Respond to a request:')}</h1>
                    <div class="fr"><a href="${h.url(controller='contents', target_type='assignment', action='index')}" class="button" onclick="cb_frag($(this), '${h.url(controller='contents', target_type='assignment', action='index', format='frag')}'); return false;">${_('See full list')}</a></div>
                    <div class="cb"></div>
                </div>
            </div>
        </div>
    </div>
</%def>
