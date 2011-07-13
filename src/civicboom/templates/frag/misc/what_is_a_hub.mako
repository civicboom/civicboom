<%namespace name="components" file="/html/web/common/components.mako" />

##------------------------------------------------------------------------------
## Imports
##------------------------------------------------------------------------------
<%!

%>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<div class="frag_whitewrap">
    <h1>${_('What is a hub?')}</h1>
    <p>&nbsp;</p>
    <p>
        ${_('A Hub is a collection of registered users, unified under one "identity" - be it as an organisation, title or issue from which requests for stories can be created for others to reposed to. All Hubs can create a bespoke Boombox.')}
    </p>
    <p>&nbsp;</p>
    <p>
        ${_('A Boombox is a simple audience engagement "widget" that lives on a site through which people can directly post their stories and respond to requests for stories.')}
    </p>
    <p>&nbsp;</p>
    <h2>${('How to get and use a Hub today:')}</h2>
    <p>&nbsp;</p>
    <div style="position: relative;">
        <div class="cb">
            <div style="float: left"><h3>1.</h3></div>
            <div style="padding-left: 3em;">
                <div class="fl" style="width: 25em;">
                    <h3>${_('Click on create a Hub button')}</h3>
                </div>
                <div class="fr" style="width: 25em;">
                    <a href="${h.url('new_group')}" class="button">${_('Create _Group')}</a>
                </div>
            </div>
        </div>
        <div class="cb">
            <p>&nbsp;</p>
            <div style="float: left"><h3>2.</h3></div>
            <div style="padding-left: 3em;">
                <div class="fl" style="width: 25em;">
                    <h3>${_('Create a name for the Hub. Eg: "The Daily Post", "Brentwood elections" or "Student protests".')}</h3>
                    <p>
                        ${_('Explain what the Hub is for. Eg: "Join us in making the news: Tell us your stories - send in videos, pictures and audio and help us report real news as it happens."')}
                    </p>
                    <p>
                        ${_('Fill in the other necessary fields and hit "Create Hub".')}
                    </p>
                </div>
                <div class="fr" style="width: 25em;">
                    <img src="/images/settings/hub-creation-1.png" />
                </div>
            </div>
        </div>
        <div class="cb">
            <p>&nbsp;</p>
            <div style="float: left"><h3>3.</h3></div>
            <div style="padding-left: 3em;">
                <div class="fl" style="width: 25em;">
                    <h3>${_("Once you've created the Hub, click on the Hub profile (top right of every page) in the drop down list to access.")}</h3>
                    <div class="create_hub">
                        <h3>4. GET STARTED!</h3>
                        <div class="special_button">
                            <a href="${h.url('new_group')}">
                                <span class="button">
                                    Create Hub
                                </span>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="fr" style="width: 25em;">
                    <img src="/images/settings/hub-creation-2.png" />
                </div>
            </div>
        </div>
    </div>
    <div class="cb"></div>
    <p>&nbsp;</p>
    <div class="cb"></div>
</div>
</%def>