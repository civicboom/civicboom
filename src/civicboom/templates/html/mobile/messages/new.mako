<%inherit file="/html/mobile/common/mobile_base.mako"/>


<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs
        
        target = kwargs.get("target")
        
    %>
    <div data-role="page">
        <div data-role="header">
            <h1>
                Send a message
                % if target:
                    to ${target}
                % endif
            </h1>
        </div>
        <div data-role="content">
            ${h.form(h.args_to_tuple('messages', format='redirect'), json_form_complete_actions="$('.ui-dialog').dialog('close');)")}
                <div data-role="fieldcontain">
                    % if target:
                        <input type="hidden" name="target" value="${target}"/>
                        To: <b>${target}</b>
                    % else:
                        <label for="target">Target</label>
                        <input type="text" name="target" value="" />
                    % endif
                    <br />
                    
                    <label for="subject">Subject</label>
                    <input type="text" name="subject" value="${kwargs.get("subject", "")}">
                    <br />
                    
                    <label for="content">Content</label>
                    <textarea name="content"></textarea>
                    <input type="submit" value="${_("Send")}">
                </div>
            ${h.end_form()}
        </div>
    </div>
</%def>

        % if kwargs.get("target"):
        <input type="hidden" name="target" value="${kwargs.get("target")}"/>
        % else:
        <tr>
            <td>${_("To")}&nbsp;</td>
            <td><input type="text"   name="target" value=""/></td>
        </tr>
        % endif