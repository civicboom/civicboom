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
        ${_('A _Group is a group of users unified under one identity such as a publication title, blog, issue or news org. When a user switches "in" to a _Group, all their actions - _article _assignments, _responses, etc - are made in the name of that _Group rather than of the individual user. Every _Group has a _Widget.')}
    </p>
    <p>&nbsp;</p>
    <p>
        ${_('A _widget is a simple "widget" - a window - that can be embedded into your website or blog. It allows your audience to directly post their content and respond to _assignments for _articles.')}
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
                    <h3>${_('Create a name for the _Group. E.g: "The Daily Post", "Brentwood elections" or "Student protests".')}</h3>
                    <br />
                    <p>
                        ${_('Explain what the _Group is for. E.g: "Join us in making the news: Tell us your stories - send in videos, pictures and audio and help us report real news as it happens."')}
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
                        <div style="width: 10em; margin:auto; margin-top: 1.5em; margin-bottom: 1.5em; text-align: center;">
                            <h3>4. ${_("GET STARTED!")}</h3>
                            <p style="font-size: 150%"><a href="${h.url('new_group')}" class="button">${_('Create _Group')}</a></p>
                            <a style="font-size: 80%;" href="${url(controller='profile', action='index')}">No thanks, take me back to my profile</a>
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
