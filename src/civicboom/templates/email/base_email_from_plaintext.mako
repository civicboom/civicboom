<%inherit file="base_email.mako"/>
## Could content_html be passed as a parmiter to body? and render_mako_def be called?
<%def name="body()">
    % if hasattr(self,'plaintext_before'):
    ${self.plaintext_before()}
    % endif
    \
    <p style="font-size: large;">${h.literal(content_html)}</p>
    \
    % if hasattr(self,'plaintext_after'):
    ${self.plaintext_after()}
    % endif
</%def>