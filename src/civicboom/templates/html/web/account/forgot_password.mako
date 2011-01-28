<%inherit file="/html/web/common/html_base.mako"/>

<%def name="title()">${_("Forgot Password")}</%def>

<%def name="show_error(name)">
    ##% if 'group' in d and name in d['group'] and 'error' in d['group'][name]:
    % if d and 'invalid' in d and name in d['invalid']:
        <span class="error-message">${d['invalid'][name]}</span>
    % endif
</%def>


    <form action="${h.url('current', hash=c.hash)}" method="post">
            <table class="form">
                    <tr>
                            <th colspan="3">${_("Forgot Password")}</th>
                    </tr>
                    <tr>
                            <td><label for="password_new">${_("New Password")}</label></td>
                            <td><input type="password" id="password_new" name="password_new" /></td>
                            <td>${show_error('password_new')}</td>
                    </tr>
                    <tr>
                            <td><label for="password_new_confirm">${_("New Password (again)")}</label></td>
                            <td><input type="password" id="password_new_confirm" name="password_new_confirm" /></td>
                            <td>${show_error('password_new_confirm')}</td>
                    </tr>
                    <tr>
                            <td colspan="3"><input type="submit" name="submit" value="${_("Change Password")}"/></td>
                    </tr>
            </table>
    </form>