<%inherit file="/frag/common/frag.mako"/>
##<%inherit file="/html/web/common/html_base.mako"/>

<%!
    import webhelpers.constants
%>

<%def name="body()">
    <%
        if d:
            self.account = d.get('payment', {})
            self.invalid = d.get('invalid', {})
        else:
            self.account = {}
            self.invalid = {}
        self.id = self.account.get('id')
    %>
    <div class="frag_whitewrap">
        ${h.form(h.url('payment', id=self.id, format='redirect'), method='PUT')}
        ${form_content(self)}
        <input type="submit" value="Save" class="button" />
        ${h.end_form()}
    </div>
</%def>

<%doc>
                % if 'invalid' in d and setting_name[0] in d['invalid']:
                    <div class="setting_error">
                        <span class="error-message">${d['invalid'][setting_name[0]]}</span>
                    </div>
                % endif
</%doc>

<%def name="form_content(self)">
    <%def name="invalid(name)">
        % if self.invalid and name in self.invalid:
                <span class="error">${self.invalid[name]}</span>
        % endif
    </%def>
    <style>
        label {
            display: inline-block;
            width: 11em;
        }
    </style>
    <p>
        Who is this payment account for?
    </p>
    <%def name="selectopt(value, current)">
        % if value==current:
            selected="selected"
        % endif
    </%def>
    <select name="name_type" id="name_type">
        <option ${selectopt(org, self.account.get('name_type'))} value="org">The company / org you work for</option>
        <option ${selectopt(org, self.account.get('name_type'))} value="ind">You personally, separate from any company</option>
    </select>
    ${invalid('name_type')}
    <br />
    <p class="org">
        <label for="org_name">Company Name:</label>
        <input type="text" id="org_name" name="org_name" value="${self.account.get('org_name','')}" />
        ${invalid('org_name')}
    </p>
    and / or
    <p class="ind">
        <label for="ind_name">Your Name:</label>
        <input type="text" id="ind_name" name="ind_name" value="${self.account.get('ind_name','')}" />
        ${invalid('ind_name')}
    </p>
    <p>
        <%
            billing_fields = [
            ('address_1', _('Line 1')),
            ('address_2', _('Line 2')),
            ('address_town', _('Town')),
            ('address_county', _('County / State')),
            ('address_postal', _('Postal code')),
            ]
        %>
        Billing Address:<br />
        % for field, title in billing_fields:
            <label for="${field}">${title}</label>
            <input type="text" id="${field}" name="${field}" value="${self.account.get(field,'')}" />
            ${invalid(field)}
            <br />
        % endfor
        <label for="address_country">Country:</label>
        <select id="address_country" name="address_country">
            % for code, country in webhelpers.constants.country_codes():
                <option
                    % if self.account.get('address_country') == code:
                        selected="selected"
                    % endif
                value="${code}">${country}</option>
            % endfor
        </select>
        ${invalid('address_country')}
    </p>
    <p>
        Agree to terms
    </p>
</%def>
