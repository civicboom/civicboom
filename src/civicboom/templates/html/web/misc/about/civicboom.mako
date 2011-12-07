<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name & FAQ")}</%def>

<style type="text/css">
    #about-civicboom h1, #about-civicboom h2 {
        padding-top: 1em;
    }
    
    #about-civicboom p {
        line-height: 200%;
    }
    
    #about-civicboom .content a {
        color: #4974b8 !important;
    }
    
    #about-civicboom .content a:hover {
        color: #FF8814 !important;
    }
    
    #about-civicboom .graphic {
        max-width: 300px;
        margin-top: 2em;
        margin-bottom: 1em;
    }
</style>

<div id="about-civicboom">

<img src="/images/logo-v3-411x90.png" class="logo" />
<h1>${_('_site_name is a platform that empowers organisations and their audience to collaborate in generating rich media content')}</h1>
<img src="/images/misc/titlepage/banner_graphic.png" class="graphic" />
<p>${_('Put simply, the Civicboom process is that a content-seeker can set a request for specific content. Then by using our customised mobile app or by uploading to the plug & go site, a content-giver can respond with rich-media directly to that request. All incoming rich-media content can then be managed by the content-seeker, and directed to a customisable plugin to be embedded on a website.')}</p>

<h2>${_('Key terms')}</h2>
<p>${_('Request = Ask for content')}</p>
<p>${_('Respond = Send content')}</p>
<p>${_('Content = All geolocated ')}<a href="http://en.wikipedia.org/wiki/Interactive_media">${_('rich media')}</a></p>
<p>${_('Content-seeker/gatherer = An Organisation')}</p>
<p>${_('Content-giver = An Individual')}</p>
<p>${_('Individual = Collectively the Audience')}</p>
<p>${_('Organisation = Typically an individual acting for content-driven entity')}</p>

<h1>${_('_site_name for Individuals')}
<h2>${_('Context')}</h2>
<p>${_('There has always been a fundamental need to ask questions and get responses. Traditionally, in small communities this was possible by face-to-face communication, but as society has grown it has become impractical for one person to communicate with everyone, everyday. First newspapers and printed media entered the scene, offering content and insight to a broader crowd. Then came the digital age.')}</p>
<br />
<p>${_('With modern-day communication tools it is possible to search for and locate the content that is relevant to you and your interests. Technology consistently refines this ability, and now the potential of the Internet is better known with the advent of the smart phone, this content is available to everyone, anywhere at all times.')}</p>

<h2>${_('The Problem')}</h2>
<p>${_('There remains a significant flaw in one vital area: the effective contribution of personal opinions from the audience. ')}</p>
<br />
<p>${_('Audience generated content is too removed from those whose job it is to engage with and interpret the audience. Current technologies only allow the community to respond publicly and directly, but do not facilitate deeper, more detailed responses nor incorporate the contribution of rich media.')}</p>

<h2>${_('Out Solution')}</h2>
<p>${_('Civicboom is a new open-community engagement platform. It provides a suite of tools to facilitate and manage specific requests for rich media content. In effect, it is a customisable channel between audience-facing organisations, and the members of the audience itself. ')}</p>
<br />
<p>${_('This channel supports content created through the use of:')}</p>
<ul>
    <li>${_('Plugins - designed to encourage engagement from website visitors.')}</li>
    <li>${_('Native Mobile Apps - designed to allow responses to requests with geolocated content. ')}</li>
    <li>${_('Content can also be suggested to specific organisations unprompted.')}</li>
</ul>
<br />
<p>${_('Rather than having opinions interpreted by potentially biased media organisations - the community is given a voice of its own. By providing the tools to request for and suggest content, we hope that local communities, governments and organisations can be encouraged to collaborate. ')}</p>
<br />
<p>${_('We believe that the provision of such tools will invigorate democracy, inform decision making and stimulate the fourth estate.')}</p>

<h2>${_('Civicboom: An Open Platform')}</h2>
<p>${_('We are an open platform, therefore the entire data-set of requests and responses are available through a public ')}<a href="http://www.programmableweb.com/api/civicboom">${_('API [Application Programing Interface]')}</a>${_('. Independent developers and organisations are able to integrate our technology with their own systems, or use it to create new mobile applications, graphs, video display walls, news feeds and more. The data is open for the public to see, use and interact with.')}</p>
<br />
<p>${_('It is ironic that the advent of the Internet should have caused a such dislocation of direct community engagement. Although it should not be the case, people are somehow insulated from meaningful and direct interactions by technology. ')}</p>
<br />
<p>${_('We believe that open-data and open-source projects accessed in conjunction with civic open platforms, like Civicboom, are the answer to this. The team is committed to building better ways to communicate meaning, and we strive to bring this level of innovation to the public.')}</p>
<br />
<p>${_('The public has a voice, and it must be heard. Rather than isolating people, technology should allow them to feel closer to their community. We are building the Civicboom platform to allow communities to re-engage.')}</p>
<br />
<p>${_("The future is now. Let's get involved.")}</p>

<h1>${_('_site_name for Organisations')}</h1>
<p>${_('Civicboom is a platform that makes content-driven organisations more efficient. This is achieved through the provision of tools, features and services needed to create a customised channel for the efficient flow and management of content from their audience.')}</p>

<h2>${_('The Context of the Problem')}</h2>
<p>${_('Most modern industries rely in some capacity [directly or indirectly] on audience generated content. Many of those industries are currently in a state of flux, and are having to adapt fast to technological innovations in media and its delivery, with limited resources. In particular, the emergence of the smart phone has meant that the audience have become the content-gatherers, and accordingly there is now a surplus of content.')}</p>
<br />
<p>${_('Consider the example of Journalism; the most obvious example of a content-driven industry. It is now a consensus viewpoint that journalists are less involved with active news gathering, and increasingly involved with news management and verification.')}</p>
<br />
<p>${_('Armed with smart phones, the audience have proved the concept of Citizen Journalism to be popular by emulating the journalists themselves. Effectively, technology has caused a reassignment of emphasis away from activities associated with gathering, and towards activities associated with collection.')}</p>
<br />
<p>${_('Recently new internet communication platforms have provided a means by which individuals can gather and push content more effectively to those that can interpret it on a grander scale.')}</p>
<br />
<p>${_('However, we at Civicboom propose that these existing platforms are flawed by not fully accommodating deeper, rich media responses. In addition, they do not provide sufficient options to manage content, or to customise the applications of solutions they offer to specific work-flows inefficiencies.')}</p>

<h2>${_('The Problem')}</h2>
<p>${_('Therefore, the problems that we have identified are:')}</p>
<ul>
    <li>${_('that the quality of content is diluted by volume;')}</li>
    <li>${_('that there is no customisable open platform to request for content directly from an audience;')}</li>
    <li>${_('that there is no convenient channel able to sufficiently host all rich-media formats;')}</li>
    <li>${_('that there are very few open platforms designed specifically for a question and answer structure;')}</li>
    <li>${_('that there are very few platforms able to be effectively scaled to larger audiences;')}</li>
    <li>${_('that there are very few platforms that can be adapted to fit a range of evolving digital work-flows.')}</li>
</ul>

<h2>${_('Our Solution')}</h2>
<p>${_('Civicboom is an online platform and suite of tools which allows content-driven organisations and individuals to work together in generating rich media content.')}</p>
<br />
<p>${_('As a more attractive selling point, Civicboom is constructed from its own open platform with an application programming interface [API]. Because Civicboom has its own open platform, it is customisable - meaning that the simple concept above can be tailored and applied to different industry work-flows through the development of an application [app] or plugin.')}</p>
<br />
<p>${_('For organisations, we offer two packages to be tailored according to your requirements:')}</p>
<ol>
    <li><b>${_('Plug & Go + Limited Services:')}</b>${_(' Access to the site as it is, with the additional use of certain content management tools and features.')}</li>
    <li><b>${_('API + Extensive Services:')}</b>${_(' Access to our API, and the provision of a customised solution to your internal or external engagement inefficiencies.')}</li>
</ol>

<h2>${_('For more information on either please contact either')}</h2>
<a href="mailto:e.hodgson@civicboom.com"><p>${_('e.hodgson@civicboom.com')}</p></a>
<a href="mailto:t.foster@civicboom.com"><p>${_('t.foster@civicboom.com')}</p></a>

<h2>${_('Find us at:')}</h2>
<p><a href="http://www.programmableweb.com/api/civicboom">${_('Programmable Web')}</a></p>
<p><a href="http://civic.mit.edu/projects/community/civicboom">${_('MIT Centre For Civic Media')}</a></p>

</div>
