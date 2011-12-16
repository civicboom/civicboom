<%inherit file="/html/web/common/html_base.mako"/>
<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("Welcome")}</%def>
<%def name="footer()">${components.misc_footer()}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="content_wrapper">
        ${banner()}
        ${cols()}
    </div>
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
        ## AllanC - hacked in the beta - sorry greg ... tidy this up
        <span style="position: absolute; left: 200px; top:24px; font-weight: bold;">beta</span> 
        
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
        <img src="images/misc/titlepage/banner_graphic.png" class="graphic"/>
        <div class="text">
            <p class="headline">${_('Channel your _content')}, <br />${_('make yourself heard')}</p>
            <p class="tagline">
                ${_('Connecting those who ')}<b>want</b>${_(' _content,')}<br />
                ${_('with the people that ')}<b>have</b>${_(' it')}<br />
            </p>
            <a href="${url(controller='account', action='signin')}">
                <div class="signup_btn">
                    <div class="link_wrapper">
                        <span class="main"><b>${_('Sign up now!')}</b></span>
                    </div>
                </div>
            </a>
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Cols
##------------------------------------------------------------------------------
<%def name="cols()">
    <div class="cols">
        ## Left col - individuals
        <div class="col">
            <div class="col-img">
                <img src="images/misc/titlepage/audience.png" />
            </div>
            <h1>${_('Have _content to give?')}</h1>
            <ul>
                <li><b>${_("Capture & send ")}</b>${_("_content directly")}</li>
                <li><b>${_("Participate ")}</b>${_("in debate")}</li>
                <li><b>${_("Get recognition ")}</b>${_("for your _content")}</li>
                <%doc>
                <li>${_('Participate in debate')}</li>
                <li>${_('Capture & send _content straight to organisations')}</li>
                <li>${_('Get recognition for your _content')}</li>
                </%doc>
            </ul>
        </div>
        
        ## Middle col - organisations
        <div class="col">
            <div class="col-img">
                <img src="images/misc/titlepage/organisation.png" />
            </div>
            <h1>${_('Want _content to use?')}</h1>
            <ul>
                <li><b>${_("Engage ")}</b>${_("_content directly")}</li>
                <li><b>${_("Manage ")}</b>${_("_content directly")}</li>
                <li>${_("Custom ")}<b>${_("Apps ")}</b>${_("and ")}<b>${_("Plugins")}</b></li>
                <%doc>
                <li>${_('Engage your audience by requesting _content directly')}</li>
                <li>${_('Innovative & secure workflow efficiency solutions')}</li>
                <li>${_('Build customised apps, plugins & management tools using our API')}</li>
                </%doc>
            </ul>
            <a href="${h.url(controller='about', action='organisations')}" class="button" style="margin: 10px 20px">Find out more</a>
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
</%def>
