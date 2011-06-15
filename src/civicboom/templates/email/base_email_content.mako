<%inherit file="base_email.mako"/>

## AllanC - Could content_html be passed as a parmiter to body? and render_mako_def be called?

<%def name="body()">
    % if hasattr(self,'content_before'):
        ${self.content_before()}
    % endif

    % if hasattr(self, 'content'):
        ${self.content()}
    % else:
        <p style="font-size: large;">
            % try:
                ${h.literal(content_html)}
            % except:
                % try:
                ${h.literal(kwargs.get('content'))}
                % except:
                    <% raise Exception('email template has no content') %>
                % endtry
            % endtry
        </p>
    % endif
    
    % if hasattr(self,'content_after'):
        ${self.content_after()}
    % endif
</%def>