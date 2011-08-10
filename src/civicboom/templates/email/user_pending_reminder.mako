<%inherit file="./base_email.mako"/>

<%def name="body()">
    <p>${_("We're really glad you joined _site_name.")}</p>
    <p>${_("We just wanted to give you a nudge, because it appears you've not verified your email to complete the sign up. ")}</p>
    <p>${_("To do this simply click on, or copy the following link into your browser: ")}<a href="${register_url}">${register_url}</a></p>
    <p>${_("Look forward to seeing you the other side!")}</p>
    ${self.footer()}
</%def>