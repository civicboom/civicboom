<%inherit file="base_email.mako"/>

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