<%inherit file="/frag/common/frag.mako"/>
##<%inherit file="/html/web/common/html_base.mako"/>

<%!
    import webhelpers.constants
    country_codes = webhelpers.constants.country_codes()
    country_sort = ['GB', 'US']
    country_dict = dict(country_codes)
    country_map = []
    for key in country_sort:
        country_map.append((key, country_dict[key]))
        del country_dict[key]
    country_codes = [(key, country_dict[key]) for key in country_dict.keys()]
    country_codes.sort(key=lambda tup:tup[1])
    country_map.extend(country_codes)
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
        <input type="submit" value="${_('Save')}" class="button" />
        ${h.end_form()}
    </div>
</%def>

<%def name="form_content(self)">
    <%def name="invalid(name)">
        % if self.invalid and name in self.invalid:
                <span class="error">${self.invalid[name]}</span>
        % endif
    </%def>
    <p>
        ${_('Who is this payment account for?')}
    </p>
    <%def name="selectopt(value, current)">
        % if value==current:
            selected="selected"
        % endif
    </%def>
    <select name="name_type" id="name_type">
        <option ${selectopt('org', self.account.get('name_type'))} value="org">${_('The company / org you work for')}</option>
        <option ${selectopt('ind', self.account.get('name_type'))} value="ind">${_('You personally, separate from any company')}</option>
    </select>
    ${invalid('name_type')}
    <br />
    <p class="org">
        <label for="org_name">${_('Company Name')}:</label>
        <input type="text" id="org_name" name="org_name" value="${self.account.get('org_name','')}" />
        ${invalid('org_name')}
    </p>
    <p class="ind">
        <label for="ind_name">${_('Your Name')}:</label>
        <input type="text" id="ind_name" name="ind_name" value="${self.account.get('ind_name','')}" />
        ${invalid('ind_name')}
    </p>
    <%
        billing_fields = [
        ('address_1', _('Line 1')),
        ('address_2', _('Line 2')),
        ('address_town', _('Town')),
        ('address_county', _('County / State')),
        ('address_postal', _('Postal code')),
        ]
    %>
    <p>
        ${_('Billing Address')}:
    </p>
    % for field, title in billing_fields:
    <p>
        <label for="${field}">${title}</label>
        <input type="text" id="${field}" name="${field}" value="${self.account.get(field,'')}" />
        ${invalid(field)}
    </p>
    % endfor
    <p>
        <label for="address_country">${_('Country')}:</label>
        <select id="address_country" name="address_country">
            % for code, country in country_map:
                <option
                    % if self.account.get('address_country') == code:
                        selected="selected"
                    % endif
                value="${code}">${country}</option>
            % endfor
        </select>
        ${invalid('address_country')}
       
    </p>
</%def>
