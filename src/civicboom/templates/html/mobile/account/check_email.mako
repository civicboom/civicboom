<%inherit file="/html/mobile/common/mobile_base.mako"/>


<%def name="title()">${_("Check your email")}</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
            ${self.title_logo()}
            <h1>${_("Great! You're nearly done!")}</h1>
            <h2>${_("An email has been sent to the email address you provided.")}</h2>
            <p>${_("Just click on the link in the email, follow the instructions to complete the sign up and enjoy full access to Civicboom!")}</p>
            <p>${_("Please note that all future notifications will be sent to your registered email. If you wish to update it, click on the Settings link in your profile once you've completed the sign up.")}</p>
            <p>${_("Happy booming!")}</p>
            <p>You can still <a href="${h.url('contents')}">${_('explore')}</a> the site before completeting registration.</a></p>
       </div>
    </div>
</%def>