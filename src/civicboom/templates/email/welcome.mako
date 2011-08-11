<%inherit file="./base_email.mako"/>

<%def name="body()">
    <h1>${registered_user.name or registered_user.username} - welcome to <a href="${h.url(controller='misc', action='titlepage', protocol='https', sub_domain='www', qualified=True)}">${_('_site_name')}!</a></h1>
    <br />
    <p>We're glad you're here!</p>
    <br />
    <p>By using ${_('_site_name')}, you are able to ask for stories and respond to them directly in an organised, manageable way.</p>
    <br />
    
    <p><b>So let's get you started:</b></p>
    <br />
    <p><b>1. Create your profile:</b> if you've not done this already, sign in to your account and tell people what you're all about.</p>
    <br />
    <p><b>2. Get involved:</b> respond to requests for stories news OR create a requests for story and news.</p>
    <br />
    <p><b>3. Share:</b> as the saying goes, you have to be in it to win it - which is why we've made it easy share your requests on Twitter, Facebook and LinkedIn etc. The more you share, the more chances you have of getting that story picked up, or sent in.</p>
    <br />
    <p><b>4. Grab the mobile app:</b>  you can set "lite" requests, respond directly to requests as they come in and upload your stories out in the field.</p>
    <br />
    <br />
    
    <p>Psst: If you're an organisation using Civicboom, don't forget to create a Hub and use the associated audience engagement tools.</p>
    <br />
    <p>Remember - we're in Beta and we need you to help us make it better for you. So send us feedback by clicking the Feedback button at the bottom left of every page.</p>
    <br />
    
    <p>Happy booming!</p>
    <br />
    
    ${self.footer()}
</%def>
