<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="title()">${_('New Message')}</%def>
<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs 
        target = kwargs.get("target")
    %>
    
    <%self:page>
        ##<%def name="page_attr()"></%def>
        <%def name="page_header()">
            <h1>
                ${_("Send a message")}
                % if target:
                    to ${target}
                % endif
            </h1>
        </%def>
        <%def name="page_content()">
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
        </%def>
    </%self>
</%def>