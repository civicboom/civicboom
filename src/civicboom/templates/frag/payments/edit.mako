<%inherit file="/frag/common/frag.mako"/>
##<%inherit file="/html/web/common/html_base.mako"/>

<%!
    import webhelpers.constants
%>

<%def name="body()">
    <%
        if d:
            self.account = d.get('payment', {})
        else:
            self.account = {}
        self.id = self.account.get('id')
    %>
    <div class="frag_whitewrap">
        ${h.form('/payments/1')}
        ${h.form(h.args_to_tuple('payment', id=self.id, format="redirect"),
            method       = 'PUT',
        )}
        <h1>Just a few details before we can upgrade your account</h1>
        <p>
            Who is this payment account for?
        </p>
        <select name="name_type" id="name_type">
            <option value="org">The company / org you work for</option>
            <option value="ind">You personally, separate from any company</option>
        </select>
        <br />
        <p class="org">
            <label for="org_name">Company Name:</label>
            <input type="text" id="org_name" name="org_name" value="${self.account.get('org_name','')}" />
        </p>
        or
        <p class="ind">
            <label for="ind_name">Your Name:</label>
            <input type="text" id="ind_name" name="ind_name" value="${self.account.get('ind_name','')}" />
        </p>
        <p>
            Billing Address:<br />
            <label for="address_1">Line 1:</label><input type="text" id="address_1" name="address_1" value="${self.account.get('address_1','')}" /><br />
            <label for="address_2">Line 2:</label><input type="text" id="address_2" name="address_2" value="${self.account.get('address_2','')}" /><br />
            <label for="address_town">Town:</label><input type="text" id="address_town" name="address_town" value="${self.account.get('address_town','')}" /><br />
            <label for="address_county">County / State:</label><input type="text" id="address_county" name="address_county" value="${self.account.get('address_county','')}" /><br />
            <label for="address_country">Country:</label>
                <select id="address_country" name="address_country">
                    % for code, country in webhelpers.constants.country_codes():
                        <option
                            % if self.account.get('address_country') == code:
                                selected="selected"
                            % endif
                        value="${code}">${country}</option>
                    % endfor
                </select><br />
            <label for="address_postal">Postal code:</label>
            <input type="text" id="address_postal" name="address_postal" value="${self.account.get('address_postal','')}" /><br />
        </p>
        <p>
            Agree to terms
        </p>
        <input type="submit" value="Save" class="button" />
        ${h.end_form()}
    </div>
</%def>