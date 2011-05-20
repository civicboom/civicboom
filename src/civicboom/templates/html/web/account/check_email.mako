<%inherit file="/html/web/common/html_base.mako"/>

<%def name="title()">${_("Please check your email")}</%def>

<%def name="show_error(name)">
    ##% if 'group' in d and name in d['group'] and 'error' in d['group'][name]:
    % if d and 'invalid' in d and name in d['invalid']:
        <span class="error-message">${d['invalid'][name]}</span>
    % endif
</%def>


    <h1>Please check your email</h1>