<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="components"      file="/html/mobile/common/components.mako" />

<%def name="page_title()">
    ${_("Sign in")}
</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
            ${components.title_logo()}
            <h1>Great! You're nearly done!</h1>
            <h2>An email has been sent to the email address you provided.</h2>
            <p>Just click on the link in the email, follow the instructions to complete the sign up and enjoy full access to Civicboom!</p>
            <p>Please note that all future notifications will be sent to your registered email. If you wish to update it, click on the Settings link in your profile once you've completed the sign up.</p>
            <h2>Happy booming!</h2>
       </div>
    </div>
</%def>