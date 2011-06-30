<%inherit file="/frag/common/frag.mako"/>

<%def name="body()">
    <%
        organisations = {
            # request_id, display name
            '25': 'Kent Online',
            '100'  : 'Gradvine',
        }
    %>
    <div class="frag_col">
        <div class="frag_whitewrap">
            <h1>
                ${_('Great! You want to post a story...')}<br />
                ${_('You now have three choices:')}
            </h1>
        </div>
        <div class="frag_whitewrap">
            <div class="h1 fl">1.</div>
            <div style="padding-left: 2em;">
                <h1>${_('Post it directly to a news organisation for potential publication:')}</h1>
                <ul>
                    % for org in d['list']:
                        <li style="padding: 0.5em 0; display: table; width: 30.4em;" class="mo-help">
                            <div class="fl">${member_avatar(org)}</div>
                            <div style="display: inline-block; display: table-cell; vertical-align: middle; width: 18em;">
                                ${_('Post directly to %s') % org.get('name')}
                            </div>
                            <div class="mo-help-r" style="float: left;left: 4em; filter: none; opacity: 1; width: 20em;">
                                ${org.get('description')}
                            </div>
                            <div class="fr" style="padding-bottom: 0.75em;">${h.secure_link(
                                h.args_to_tuple('new_content', parent_id=org.get('push_assignment')) ,
                                value           = _("Post a story") ,
                                value_formatted = h.literal("<span class='button'>%s</span>") % _('Post a story') ,
                                json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , 
                            )}</div>
                            <div style="clear:both;"></div>
                        </li>
                    % endfor
                </ul>
                <div style="padding: 1em 0;">
##                    ${_('Are you a news organisation? Do you want to get news directly from source?')}
##                    <a href="${h.url(controller='misc', action='hub_organisation')}">${_('Click here to learn how.')}</a>
                </div>
            </div>
        </div>
        <div class="frag_whitewrap">
            <div class="h1 fl">2.</div>
            <div style="padding-left: 2em;">
                <h1 class="fl">${_('Post your story on Civicboom:')}</h1>
                <div class="fr" style="padding-top: 0.25em;">${h.secure_link(h.url('new_content', target_type='article'   ), _("Post a story") , css_class="button")}</div>
                <div style="clear:both;"></div>
            </div>
        </div>
        <div class="frag_whitewrap">
            <div class="h1 fl">3.</div>
            <div style="padding-left: 2em;">
                <h1 class="fl">${_('Respond to a request:')}</h1>
                <div class="fr" style="padding-top: 0.25em;"><a href="${h.url(controller='misc', action='featured')}" class="button" onclick="cb_frag($(this), '${h.url(controller='misc', action='featured', format='frag')}'); return false;">${_('See full list')}</a></div>
                <div style="clear:both;"></div>
            </div>
        </div>
    </div>
</%def>
