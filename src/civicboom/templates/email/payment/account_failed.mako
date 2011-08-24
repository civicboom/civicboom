<%inherit file="./base_email.mako"/>

<%def name="body()">

<h1>Your account has been disabled</h1>
<br />
<p>
    Your account has been disabled due to an invoice being left outstanding, this means you will have limited access to the features on the site.
</p>
<p>
    Please login and check your account as soon as possible.
</p>
<p>Happy booming!</p>
<br />

${self.footer()}
</%def>
