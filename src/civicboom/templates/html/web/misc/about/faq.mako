<%inherit file="base.mako"/>

<%def name="title()">${_("FAQ's for _site_name")}</%def>

<h1>${_("FAQ")}</h1>

${_('What is Civicboom?')}

${_('Civicboom lets people that need news stories get it from people that have it.')}

${_('How does it work?')}

${_('Civicboom works on two levels:')}

${_('1. Journalists, blogger, publishers, news organisations - get stories, videos, images and audio directly from your audience.')}
${_('2. People - you are the eyes and ears of a story and Civicboom is the tool that lets you share those stories directly with those that want and need them.')}


${_('What is the Boombox?')}
${_('A Boombox is a simple audience engagement "widget" that lives on a site through which people can directly post their stories and respond to requests for stories.')}  

${_('What can you do on the mobile app?')}
${_('You can respond to requests directly and share your news stories as they happen.')}

${_('What is an RSS feed?')}
${_('“RSS solves a problem for people who regularly use the web. It allows you to easily stay informed by retrieving the latest content from the sites you are interested in. You save time by not needing to visit each site individually. You ensure your privacy, by not needing to join each site's email newsletter.')}

${_('What is Creative Commons (CC) Attribution License?')}
${_('All content created has a Creative Commons License automatically attached to it when posted. The Creative Commons Attribution License 3.0 Unported means you are free:')} 
${_('To Share — to copy, distribute and transmit the work')}
${_('To Remix — to adapt the work')}
${_('To make commercial use of the work')}
${_('Attribution — You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).')} 

${_('What is a Hub?')}
${_('A Hub is a collection of registered users, unified under one "identity" - be it as an organisation, title or issue from which requests for stories can be created for others to reposed to. All Hubs can create a bespoke Boombox.')}

${_('What are the different roles in a Hub?')}
${_('Administrator: You have full privileges over the Hub; you can set member roles, create requests, invite and remove users from the Hub, publish and approve content, edit and delete drafts, and alter Hub settings.')}
${_('Editor: You can publish and approve content, create requests and edit and delete drafts.')}
${_('Contributor: You can create content and edit drafts.')}
${_('Observer: You can view drafts and comment on them, but not create or publish them.')}

${_('What happens when I switch Hubs')}
${_('All your actions-your requests, responses and content - will be posted under the name of that Hub.')}

${_('How do I switch Hubs?')}
${_('Hover your mouse over your profile picture in the top righthand corner of the screen. A list of Hubs you can access will be displayed, click one to switch into that Hub.)}

${_('How do I email content to others? Will I need to copy and paste it?')}
${_('In the “social sharing” section of any piece of content there is a series of icons (like Facebook and Twitter) click the envelope to share that content with others by email.')} 

${_('How do I share content via Twitter, Facebook and other social media?')}
${_('In the top right hand corner of any piece of content there is a series of icons, click the relevant icon to share via that site.')}

${_('How do multiple users work on the same draft?')}
${_('Create a draft whilst under the persona of a Hub, then other members Hub members can edit that draft. Note: you must be under the persona of a Hub for this to work, it will not work with individual users for privacy reasons.')}

${_('Why doesn't my notification counter go down after I've read my notifications?')}
 ${_('Click on one, it will open and show you the notification. After that, the notification counter will go down. Opening the notification list will not mark notifications as read and therefore not decrease the notification counter.')}

${_('Invite function')}
${_('- What: This allows you to invite others to join your hub.')}
${_('- How to: Go to the profile of the person you want to invite and click Invite')}
${_('- Accepting: After you are invited to a hub, you will receive a notification. This will enable you to join the hub at any time by clicking on its profile and join hub')}

${_('How do I change the status of my hub's members?')}
${_('Switch into the relevant hub. In the bottom left of your hub's profile, there will be a box showing members of the hub. Click on heading members (your mouse pointer will change to a hand when you hover over it). This will open a window where each member and their status is shown and from there it can be changed by selecting a new status from the drop-down. ')}

${_('What is a trusted follower?')}
${_('A trusted follower can see your your private content.')}

${_('What is private content?')}
${_('Private content is a premium feature that allows users to hide their content from the general public. ')}

${_('What is embedding?')}
${_('By embedding something you make it appear inside other webpages and blogs. For example, you might embed your request for news into site so that your readers can use it to give me their stories.')}

${_('Credit')}
${_('When you 'credit' a piece of media, you're saying you want to be credited if it is used by other people. ')}

${_('Booming')}
${_('Booming is used to highlight content you think is particularly relevant to you or your followers.')}



<%doc>
    <object width="640" height="390">
        <param name="movie" value="https://www.youtube.com/v/TJtHGK3OmoA?fs=1&amp;hl=en_US"></param>
        <param name="allowFullScreen" value="true"></param>
        <param name="allowscriptaccess" value="always"></param>
        <param name="wmode" value="transparent"></param>
        <embed src="https://www.youtube.com/v/TJtHGK3OmoA?fs=1&amp;hl=en_US" type="application/x-shockwave-flash"
            width="640" height="390" allowscriptaccess="always" allowfullscreen="true"
            wmode="transparent"></embed>
    </object>
</%doc>


<%def name="breadcrumbs()">
    <span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
        <a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
            <span itemprop="title">About</span>
        </a>
    </span>
    &rarr;
    <span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
        <a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
            <span itemprop="title">Company</span>
        </a>
    </span>
</%def>
