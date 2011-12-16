<%!
    config_key = ''
%>

<%def name="body()">
    ${next.body()}

    ${h.form(h.args_to_tuple(controller='settings', id=c.logged_in_user.username, action='update'), method='put')}
        ${_("Don't show me this again")}
        <input type='checkbox' name='${self.attr.config_key}' value='True' onclick="$(this).closest('form').submit(); $.modal.close();" />
        <input class='hide_if_js' type='submit' name='submit' value='submit'/>
    </form>
</%def>