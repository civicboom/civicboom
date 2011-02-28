<%inherit file="base_email.mako"/>

<%def name="body()">
<p style="font-size: large;">${h.literal(c.email_content)}</p>
</%def>