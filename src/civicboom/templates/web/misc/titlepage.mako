<%inherit file="/web/common/html_base.mako"/>

<%def name="title()">${_("Welcome")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <table style="display: inline-block; vertical-align: middle;"><tr>
        <td></td>
        <td>${what_is()}</td>
        <td>${mobile()}</td>
    </tr></table>
</%def>


##------------------------------------------------------------------------------
## What is
##------------------------------------------------------------------------------

<%def name="what_is()">
    <section class='description'>
        <div style="float: right; padding-bottom: 1em;">
            <a class="button" href="${url(controller='account', action='signin')}">${_('Sign up')}</a>
        </div>
        
        <div class='description_container'>
            <h1>${_('What is _site_name?')}</h1>
            <table class="steps_container"><tr>
                <td class="step_current">
                    <div style="position: relative; top:0em;">
                    <div class="step_back">
                        left
                    </div>
                    <div class="step_next">
                        right
                    </div>
                    
                    <p>current plan</p>
                    <p>figro</p>
                    <p>iewnf</p>
                    <p>rgrg</p>
                    </div>
                </td>
                <td class="step_description">
                    description
                </td>
                <div style="clear: both;"></div>
            </tr></table>
        </div>
        
        <a style="float:right;" class="button" href="${url(controller='misc', action='about')}">${_('Learn More')}</a>
        <p>${_('Dont just read it, feed it')}</p>
        
        <div style="clear: both; padding: 0.5em;"></div>
        
        <a style="float:right; color: black; background: none;" class="button" href="${url(controller='misc', action='about')}">${_('Get in touch')}</a>
        <p>${_('Are you an organisation? Do you want to know how Civicboom can help you')}</p>
    </section>
</%def>

##------------------------------------------------------------------------------
## Mobile
##------------------------------------------------------------------------------

<%def name="mobile()">
    <section class="mobile">
        <h2>${_('Grab the _site_name app')}</h2>
        <img src="/images/misc/mobile_nonpreview.png">
        <p>${_('Comming soon:')}</p>
        <ul>
            <li>Blackberry</li>
            <li>iPhone</li>
        </ul>
    </section>
</%def>



##------------------------------------------------------------------------------
## Old
##------------------------------------------------------------------------------

<%doc>
<section class="signup">
Already have a social media account?
<br>&nbsp;
<br><img src="/images/misc/socmed-signup.png">
<br>&nbsp;
<br><a href="/account/signin" class="button">Signup</a>
</section>

<section class="mobile">
<img src="/images/misc/mobile_nonpreview.png">
<br>Civicboom for your mobile
</section>

<section class="blurb">
<br>"We work across wide-ranging communication
<br>channels with clients who are visionaries in
<br>their fields. By actively building close working
<br>relationships we connect people."
</section>

</%doc>