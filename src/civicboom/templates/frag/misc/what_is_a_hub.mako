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
<div style="background: white; border-radius: 16px; padding: 16px; margin: 1em; width: 722px; margin: auto;" class="frag_whitewrap">
    <h1>${_('What is a _group?')}</h1>
    <p>&nbsp;</p>
    <p>
        ${_('A _Group is a collection of registered users, unified under one "identity" - be it as an organisation, title or issue from which requests for _articles can be created for others to reposed to. All _Groups can create a bespoke _widget.')}
    </p>
    <p>&nbsp;</p>
    <p>
        ${_('A _widget is a simple audience engagement "widget" that lives on a site through which people can directly post their stories and respond to requests for _articles.')}
    </p>
    <p>&nbsp;</p>
    <h2>${_('How to get and use a _Group today:')}</h2>
    <p>&nbsp;</p>
    <div style="position: relative;">
        <div class="cb">
            <div style="float: left"><h3>1.</h3></div>
            <div style="padding-left: 3em;">
                <div class="fl" style="width: 20em;">
                    <h3>${_('Click on create a _Group button')}</h3>
                    <br />
                    <p>${_('You can click here - or read on for full instructions and then create your _Group.')}</p>
                </div>
                <div class="fr" style="width: 30em;">
                    <a href="${h.url('new_group')}" class="button">${_('Create _Group')}</a>
                </div>
            </div>
        </div>
        <div class="cb">
            <p>&nbsp;</p>
            <div style="float: left"><h3>2.</h3></div>
            <div style="padding-left: 3em;">
                <div class="fl" style="width: 20em;">
                    <h3>${_('Create a name for the _Group. Eg: "The Daily Post", "Brentwood elections" or "Student protests".')}</h3>
                    <br />
                    <p>
                        ${_('Explain what the _Group is for. Eg: "Join us in making the news: Tell us your stories - send in videos, pictures and audio and help us report real news as it happens."')}
                    </p>
                    <br />
                    <p>
                        ${_('Fill in the other necessary fields and hit "Create _Group".')}
                    </p>
                </div>
                <div class="fr" style="width: 30em;">
                    <img src="/images/settings/hub-creation-1.png" />
                </div>
            </div>
        </div>
        <div class="cb">
            <p>&nbsp;</p>
            <div style="float: left"><h3>3.</h3></div>
            <div style="padding-left: 3em;">
                <div class="fl" style="width: 20em;">
                    <h3>${_('You will then be taken to your _Group page')}</h3>
                    <br />
                    <p>
                        ${_("Once you've created the _Group, click on the _Group profile (top right of every page) in the drop down list to access.")}
                    </p>
                    <br />
                    <br />
                    <div style="width: 20em" class="border_box">
                        <div style="width: 10em; margin:auto; margin-top: 1.5em; margin-bottom: 1.5em;">
                            <h3>4. GET STARTED!</h3>
                            <p style="font-size: 150%"><a href="${h.url('new_group')}" class="button">${_('Create _Group')}</a></p>
                        </div>
                    </div>
                </div>
                <div class="fr" style="width: 30em;">
                    <img src="/images/settings/hub-creation-2.png" />
                </div>
            </div>
        </div>
    </div>
    <div class="cb"></div>
    <p>&nbsp;</p>
    <div class="cb"></div>
</div>
<p>&nbsp;</p>
</%def>
