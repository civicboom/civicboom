<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name & FAQ")}</%def>

<style type="text/css">
    h2 {
        padding-top: 1em;
    }
    
    ul li {
        list-style: disc;
        margin-left: 2em;
        line-height: 200%;
    }
    
    .graphic {
        float: right;
        padding-left: 2em;
    }
</style>

<h1>${_('_site_name is a platform that lets organisations and their audience collaborate in generating _content:')}</h1>
<img src="/images/misc/titlepage/banner_graphic.png" class="graphic" style="max-width: 300px; margin: 1em auto 1em auto;"/>

<h2>${_('Definition of Terms:')}</h2>
<p>${_('The definition of news as a commodity has changed. We at _site_name propose that news should now be seen as rich media content. This news is now available from a large number of possible sources [the audience] using a particular medium [smart phones] via a large number of channels [e-mail, micro- blogging, blogging and social networks]. Accordingly, the modern news-seeker is any individual that works in a content-driven industry.')}</p>
<p>${_('Bearing this altered definition in mind, _site_name is a channel concerned with facilitating the efficient flow and management of news.')}</p>

<h2>${_('The Opportunity:')}</h2>
<p>${_('Arguably every industry relies in some capacity [directly or indirectly] on audience generated news.')}</p>
<p>${_('All those that rely directly on news are currently in a state of flux, and are having to adapt fast to technological innovations in media with finite resources. All this is being done in the face of an ongoing decline in offline revenues.')}</p>
<p>${_("_site_name propose that these industries are being unnecessarily inefficient with their resources in their sourcing of news. We suggest that through the assimilation of _site_name\'s API technology into existing news-gathering workflows, there is an opportunity for a significant improvement in this level of efficiency.")}</p>

<h2>${_('The Problem:')}</h2>
<p>${_('With the emergence of the smart phone, rather than being an active gatherer, the modern news-seeker is increasingly concerned with the management of large volumes of news that has already been collected. The audience have become the news-gatherers and accordingly there is now a surplus of news. Therefore, the problems that are emerging are:')}</p>
<ul>
    <li>${_('that the quality of news is diluted by volume')}</li>
    <li>${_('that there is no convenient channel that can host all rich-media formats')}</li>
    <li>${_('that no available customisable channel can be adapted to fit existing digital news workflows')}</li>
</ul>

<h2>${_('_site_name:')}</h2>
<p>${_('_site_name is an online platform and tool allowing content-driven organisations and individuals to work together in generating news as rich media content.')}</p>
<p>${_('As a more attractive selling point, _site_name is constructed from its own open platform or application programming interface [API]. Because _site_name has its own open API, it is customisable - meaning that the simple concept above can be tailored and applied to different industry workflows through the development of an application or plugin.')}</p>

<h2>${_('Our Solution:')}</h2>
<p>${_('Our aim is to develop _site_name as the answer to topical concerns over the future role of news-seekers by creating a particularly well-constructed and adaptable API. This API can then be exploited by content-driven organisations that have a need to create solutions to their workflow inefficiencies.')}</p>
<p>${_("We realise that our value is in assisting the audience to channel content to content-requesters. Accordingly, we have a free basic service ['plug and go' version] with limited access, but it will always be accessible to content-providers because they are the asset.")}</p>
<p>${_('In essence, the concept is that a content-seeker can request specific content, then, by using a customised _site_name mobile app, a content-giver can respond with rich-media or information directly to that request. That content can then be managed by the content-seeker and directed to a customisable plugin to be embedded on a website.')}</p>

<h2>${_('Find us at:')}</h2>
<p><a href="http://www.programmableweb.com/api/civicboom">${_('Programmable Web')}</a></p>
<p><a href="http://civic.mit.edu/projects/community/civicboom">${_('MIT Centre For Civic Media')}</a></p>