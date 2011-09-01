<%inherit file="/html/mobile/common/mobile_base.mako"/>

<% args, kwargs = c.web_params_to_kwargs %>

<%def name="body()">
    <div data-role="page">
        <div data-role="header">
        
        </div>
        <div data-role="content">
            <% args, kwargs = c.web_params_to_kwargs %>
            ${h.form(h.args_to_tuple('messages', format='redirect'), json_form_complete_actions="$('.ui-dialog').dialog('close');)")}
                <div data-role="fieldcontain">
                    <input type="hidden" name="target" value="${kwargs.get("target")}"/>
                    <label for="subject"></label>
                    <input type="text" name="subject" value="${kwargs.get("subject", "")}">
                    <textarea name="content"></textarea>
                    <input type="submit" value="${_("Send")}">
                </div>
            ${h.end_form()}

        </div>
    </div>
</%def>