<%inherit file="base.mako"/>

<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

<%def name="title()">${_("Payment Plans")}</%def>

<%def name="body()">
    ${blurb()}
    ${upgrade_details()}
</%def>

<%def name="blurb()">
    <h1>${_('_site_name plans')}</h1>
    <p>
        ${_('_site_name is free to use')} - 
        ${_("we offer a limited version that's perfect for non-professionals who want to respond to requests and share their stories directly to news organisations.")}
    </p>
    <p>
        ${_('We also offer enhanced versions - the Pro Lite and the Pro Premium')}<br />
        ${_("There are no long-term commitments - just upgrade and pay on a month-by-month basis. If you want to revert to the free plan, you can. Hover over each of the features for more details.")}
    </p>
</%def>

<%def name="popup_()">
    <h1>Hold up!</h1>
    <p>You're trying to perform an action that is a paid-for service as part of the Premium account</p>
    
    ${upgrade_details(style="popup")}
</%def>


<%def name="upgrade_details(style=None)">
    <%
        plans = ['free', 'plus', 'corp']
        hilight_plan = 'plus'
        plan_details = {
            'free': {
                'title': _('Free'),
                'cost':  _('Free'),
            },
            'plus': {
                'title': _('Lite'),
                'cost':  _(u'£10/month'),
            },
            'corp': {
                'title': _('Pro'),
                'cost':  _(u'£300/month'),
            }
        }
        features = [
            {
                'title': _('Requests per 30 day period'),
                'who'  : ['free', 'plus', 'corp'],
                'values':['5', '20', 'Unlimited']
            },
            {
                'title': _('Scheduled requests'),
                'who'  : ['plus', 'corp'],
            },
            {
                'title': _('Multiple messaging'),
                'who'  : ['plus', 'corp'],
            },
            {
                'title': _('Post requests and get responses via own site'),
                'who'  : ['plus', 'corp'],
            },
            {
                'title': _('Basic Hubs'),
                'who'  : ['free'],
            },
            {
                'title': _('Up to 3 Pro Hubs'),
                'who'  : ['plus'],
            },
            {
                'title': _('Unlimited Pro Hubs (for multiple titles/sites)'),
                'who'  : ['corp'],
            },
        ]
    %>
    <table class="upgrade_plans">
        <thead>
            <tr>
                <td class="larger">${_('Features')}</td>
                % for plan in plans:
                    <td class="item ${'hilight' if plan == hilight_plan else ''}">
                        ${plan_details[plan]['title']}
                    </td>
                % endfor
            </tr>
        </thead>
        <tbody>
            % for feature in features:
                <tr>
                    <td class="title">${feature['title']}</td>
                    % for plan in plans:
                        <td class="item  ${'hilight' if plan == hilight_plan else ''}">
                            % if plan in feature['who']:
                                % if feature.get('values'):
                                    ${feature['values'][feature['who'].index(plan)]}
                                % else:
                                    <span class="icon16 i_accept"><span>Yes</span></span>
                                % endif
                            % else:
                                <span class="icon16 i_delete"><span>N/A</span></span>
                            % endif
                        </td>
                    % endfor
                </tr>
            % endfor
        </tbody>
        <tfoot>
            <tr class="foot">
                <td class="title">${_('Cost')}</td>
                % for plan in plans:
                    <td class="item  ${'hilight' if plan == hilight_plan else ''}">
                        ${plan_details[plan]['cost']}
                    </td>
                % endfor
            </tr>
            % if style == 'create_account':
                <tr class="upgrade" style="font-size: 125%">
                    <td></td>
                    % for plan in plans:
                        <td>
                            % if plan in ('plus','corp'):
                                <input class="button" type="submit" name="plan_${plan}" value="${_('Create')}" />
                            % endif
                        </td>
                    % endfor
                </tr>
            % else:
                <tr class="upgrade"
                % if style == 'regrade_plans':
                    style="font-size: 125%"
                % endif
                >
                    <td></td>
                    % for plan in plans:
                        <td>
                            % if plan in ('plus','corp'):
                                ${h.secure_link(
                                    h.url('payment_action', id='me', action='regrade', new_type=plan),
                                    _('Upgrade'),
                                    css_class="button"
                                )}
                            % endif
                        </td>
                    % endfor
##                    % if len(plans)-2 > 0:
##                        % for x in range(len(plans)-3):
##                            <td></td>
##                        % endfor
##                    % endif
                </tr>
            % endif
        </tfoot>
    </table>
    % if style != 'create_account':
        ${popup.popup_static('Upgrade your account', upgrade_popup, '', html_class="upgrade_popup")}
    % endif
</%def>

<%def name="upgrade_popup()">
    <p>If you want to upgrade or learn more, simply fill in the form below and one of our team will be in touch asap!</p>
    ${h.form(h.args_to_tuple(controller='misc', action='upgrade_request', format='redirect'), method='post', json_form_complete_actions="cb_frag_remove(current_element);")}
        <%
        upgrade_form_meta = (
            ('name'    , _('Name')    , ''),
            ('company' , _('Company') , '(optional)'),
            ('phone'   , _('Phone')   , ''),
            ('email'   , _('Email')   , ''),
            ('industry', _('Industry'), '(optional)'),
        )
        %>
        <table class="upgrade form">
            <tr>
                <td style="width: 10em;" class="label">
                    <label for="upgrade_enquiry">What is your enquiry regarding?</label>
                </td>
                <td>
                    <select id="upgrade_enquiry" name="upgrade_enquiry">
                        <option value="More information">${_('More information')}</option>
                        <option value="Upgrading my account">${_('Upgrading my account')}</option>
                    </select>
                </td>
            </tr>
            % for name, title, extra in upgrade_form_meta:
                <tr>
                    <td class="label">
                        <label for="upgrade_${name}">${title}</label>
                    </td>
                    <td>
                        <input type="text" id="upgrade_${name}" name="${name}" placeholder="${extra}">
                    </td>
                </tr>
            % endfor
            % if not c.logged_in_user:
                <tr>
                    <td>
                        Proove you're human
                    </td>
                    <td>
                        ${h.get_captcha(c.lang, 'white')}
                    </td>
                </tr>
            % endif
            <tr><td colspan="2">
                <input class="button" type="submit" value="Request Upgrade"/><br /><br />
            </td></tr>
        </table>
    ${h.end_form()}
</%def>
