<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("Welcome")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="content_wrapper">
        ${banner()}
        ${cols()}
    </div>
    ${components.misc_footer()}
</%def>

##------------------------------------------------------------------------------
## Header
##------------------------------------------------------------------------------
<%def name="header()">
    <div class="misc_header">
        ## logo image
        <a href='/'>
            <img  class='logo_img'     src='${h.wh_url("public", "images/logo-v3-411x90.png")}'    alt='${_("_site_name")}'>
        </a>
        <span class='beta_overlay'>beta</span> 
        
        ## header links
        <span class="links">
            <a href="${h.url(controller='misc', action='about', id='civicboom')}">${_("About _site_name")}</a>
            <a href="${h.url(controller='misc', action='about', id='faq'  )}">${_("FAQ")}</a>
            <a href="http://civicboom.wordpress.com/" target="_blank">${_("Blog")}</a>
            <a href="mailto:contact@civicboom.com">${_("Contact")}</a>
            <a href="${url(controller='account', action='signin')}">${_("Sign in")}</a>
        </span>
    </div>
</%def>

##------------------------------------------------------------------------------
## Banner
##------------------------------------------------------------------------------
<%def name="banner()">
    <div class="banner">
        <%doc>
        <div class="col-top">
            <h1>${_('Channel your _content ')}${_('make yourself heard')}</h1>
        </div>
        </%doc>
        <div class="col-left">
                    <h1>${_('Channel your _content ')}${_('make yourself heard')}</h1>
            <img src="images/misc/titlepage/banner_graphic.png" class="graphic"/>
            <div class="signup">
                <a href="${url(controller='account', action='signin')}">Sign Up</a>
            </div>
        </div>
        <div class="col-right">
            <div class="info-box" id="individuals">
                <h1>${_('What you can do')}</h1>
                <img src="/images/misc/titlepage/individual_graphic.png" />
                <p>
                    <ul>
                        <li>${_('Request for information that caters to your needs and interests.')}</li>
                        <li>${_('Capture and contribute your unique _content and ideas.')}</li>
                        <li>${_('Communicate directly with organisations and the masses.')}</li>
                        ## <li>${_('Receive recognition and feedback for _content.')}</li>
                        ## <li>${_('Progress as a contributor and improve your _content.')}</li>
                        <li>${_('Engage in discussion and feedback whilst developing your ideas.')}</li>
                    </ul>
                </p>
            </div>
            <div class="info-box" id="organisations">
                <h1>${_('_site_name for Organisations')}</h1>
                <img src="/images/misc/titlepage/organisation_graphic.png" />
                <p>
                    <ul>
                        <li>${_('Request and access _content and turn information into valuable knowledge.')}</li>
                        <li>${_('Benefit your business by directly engaging with your audiences.')}</li>
                        <li>${_('Customise _site_name for your organisation with our innovative and flexible API.')}</li>
                        <li>${_('Develop custom apps, plugins and management tools for your needs.')}</li>
                        ## <li>${_("Explore and utilise our dynamic platform's communication opportunities.")}</li>
                        ## <li>${_('Improve business rapport by recognising and rewarding audiences.')}</li>
                    </ul>    
                </p>
            </div>
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Cols
##------------------------------------------------------------------------------
<%def name="cols()">

    <%doc>
    <div class="cols">
        ## Left col - individuals
        <div class="col">
            <div class="col-img">
                <img src="images/misc/titlepage/audience.png" />
            </div>
            <h1>${_('Individuals')}</h1>
            <ul>
                <li>${_('Participate in debate')}</li>
                <li>${_('Capture & send _content straight to organisations')}</li>
                <li>${_('Get recognition for your _content')}</li>
            </ul>
        </div>
        
        ## Middle col - organisations
        <div class="col">
            <div class="col-img">
                <img src="images/misc/titlepage/organisation.png" />
            </div>
            <h1>${_('Organisations')}</h1>
            <ul>
                <li>${_('Engage your audience by requesting _content directly')}</li>
                <li>${_('Innovative & secure workflow efficiency solutions')}</li>
                <li>${_('Build customised apps, plugins & management tools using our API')}</li>
            </ul>
        </div>
        
        ## Right col - mobile
        <div class="col">
            <a href="http://market.android.com/details?id=com.civicboom.mobile2" target="blank">
                <div class="col-img">
                    <img src="images/misc/titlepage/mobile-col.png" />
                </div>
            </a>
            <h1>${_('Get _site_name on your mobile')}</h1>
            <a href="http://market.android.com/details?id=com.civicboom.mobile2" target="blank">
                <div class="android_btn">
                    <img src="/images/about/mobile/android.png" alt="android">
                    <h3>${_("Get the Android App now")}</h3>
                </div>
            </a>
        </div>
    </div>
    </%doc>
</%def>