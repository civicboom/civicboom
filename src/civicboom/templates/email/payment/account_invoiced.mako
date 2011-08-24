<%inherit file="./base_email.mako"/>

<%def name="body()">

<h1>Your account has been invoiced</h1>
<br />
<p>
    Please login and check your payment account for further information.
</p>
<p>Happy booming!</p>
<br />

${self.footer()}
</%def>
