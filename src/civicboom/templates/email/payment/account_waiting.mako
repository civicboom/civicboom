<%inherit file="../base_email.mako"/>

<%def name="body()">

<h1>An outstanding invoice is close to being overdue</h1>
<br />
<p>
    Please login and check your payment account for further information, once an account is overdue it is likely to be disabled at any time.
</p>
<p>Happy booming!</p>
<br />

${self.footer()}
</%def>
