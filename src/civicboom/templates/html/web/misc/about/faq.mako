<%inherit file="base.mako"/>

<%def name="title()">${_("FAQ's for _site_name")}</%def>

<h1>${_("FAQ")}</h1>

<p>
<b>${_("What is Civicboom?")}</b>
<br />${_("Civicboom lets people that need news _articles get it from people that have it.")}
</p>

<p>
<b>${_("How does it work?")}</b>
${_("Civicboom works on two levels:")}
    <ol>
        <li>${_("Journalists, blogger, publishers, news organisations - get _articles, videos, images and audio directly from your audience.")}</li>
        <li>${_("People - you are the eyes and ears of a _article and Civicboom is the tool that lets you share those _articles directly with those that want and need them.")}</li>
    </ol>
</p>

<p>
<b>${_("What is booming?")}</b>
<br />${_("Booming this content will recommend it to your followers and the rest of the community.")}
</p>

<p>
<b>${_("What is Creative Commons (CC) Attribution License?")}</b>
<br />${_("All content created has a Creative Commons License automatically attached to it when posted. The Creative Commons Attribution License 3.0 Unported means you are free:")} 
<br />${_("To Share - to copy, distribute and transmit the work")}
<br />${_("To Remix - to adapt the work")}
<br />${_("To make commercial use of the work")}
<br />${_("Attribution - You must attribute the work in the manner specified by the author or licensor (but not in any way that suggests that they endorse you or your use of the work).")}
</p>

<p>
<b>${_("What is the _widget?")}</b>
<br />${_("The _widget is a simple audience engagement \"widget\", a window that can be embedded into your website or blog. It allows your readers to directly post their content and respond to requests for stories. ")}
</p>

<p>
<b>${_("How do I share content via Twitter, Facebook and other social media?")}</b>
<br />${_("In the top right hand corner of any piece of content there is a series of icons, click the relevant icon to share via that site.")}
</p>

<p>
<b>${_("What is an RSS feed?")}</b>
<br />${_("RSS solves a problem for people who regularly use the web. It allows you to easily stay informed by retrieving the latest content from the sites you are interested in. You save time by not needing to visit each site individually. You ensure your privacy, by not needing to join each site's email newsletter.")}
</p>

<p>
<b>${_("What can you do on the mobile app?")}</b>
<br />${_("You can respond to news requests directly and share your news _articles as they happen.")}
</p>

<p>
<b>${_("Why doesn't my notification counter go down after I've read my notifications?")}</b>
<br />${_("Click on one, it will open and show you the notification. After that, the notification counter will go down. Opening the notification list will not mark notifications as read and therefore not decrease the notification counter.")}
</p>

<p>
<b>${_("What is a Hub?")}</b>
<br />${_("A Hub is a collection of registered users, unified under one \"identity\" - be it as an organisation, title or issue from which requests for _articles can be created for others to reposed to. All Hubs can create a bespoke _widget.")}
</p>

<p>
<b>${_("What are the different roles in a Hub?")}</b>
<br />${_("Administrator: You have full privileges over the Hub; you can set member roles, create _article requests, invite and remove users from the Hub, publish and approve content, edit and delete _articles, and alter Hub settings.")}
<br />${_("Editor: You can publish and approve content, create _article requests and edit and delete _articles.")}
<br />${_("Contributor: You can create content and edit _articles.")}
<br />${_("Observer: You can view _articles and comment on them, but not create or publish them.")}
</p>

<p>
<b>${_("What happens when I switch Hubs")}</b>
<br />${_("All your actions-your _article requests, _responses and content - will be posted under the name of that Hub.")}
</p>

<p>
<b>${_("How do I switch Hubs?")}</b>
<br />${_("Hover your mouse over your profile picture in the top righthand corner of the screen. A list of Hubs you can access will be displayed, click one to switch into that Hub.")}
</p>

<p>
<b>${_("How do I email content to others? Will I need to copy and paste it?")}</b>
<br />${_("In the \"social sharing\" section of any piece of content there is a series of icons (like Facebook and Twitter) click the envelope to share that content with others by email.")}
</p>

<p>
<b>${_("What is private content?")}</b>
<br />${_("Private content is a premium feature that allows users to hide their content from the general public.")}
</p>

<p>
<b>${_("What is a trusted follower?")}</b>
<br />${_("A trusted follower can see your your private content.")}
</p>

<p>
<b>${_("How do multiple users work on the same _articles?")}</b>
<br />${_("Create a _articles whilst under the persona of a Hub, then other members Hub members can edit that _articles. Note: you must be under the persona of a Hub for this to work, it will not work with individual users for privacy reasons.")}
</p>

<p>
<b>${_("Invite function")}</b>
<ul>
    <li>${_("What: This allows you to invite others to join your hub.")}</li>
    <li>${_("How to: Go to the profile of the person you want to invite and click Invite")}</li>
    <li>${_("Accepting: After you are invited to a hub, you will receive a notification. This will enable you to join the hub at any time by clicking on its profile and join hub")}</li>
</ul>
</p>

<p>
<b>${_("How do I change the status of my hub's members?")}</b>
<br />${_("Switch into the relevant hub. In the bottom left of your hub's profile, there will be a box showing members of the hub. Click on heading members (your mouse pointer will change to a hand when you hover over it). This will open a window where each member and their status is shown and from there it can be changed by selecting a new status from the drop-down.")}
</p>

<p>
<b>${_("What is embedding?")}</b>
<br />${_("By embedding something you make it appear inside other webpages and blogs. For example, you might embed your request for news into site so that your readers can use it to give you their _articles.")}
</p>

<p>
<b>${_("What is credit?")}</b>
<br />${_("When you 'credit' a piece of media, you're saying you want to be credited if it is used by other people.")}
</p>

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
            <span itemprop="title">About</span>'
        </a>
    </span>
    &rarr;
    <span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
        <a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
            <span itemprop="title">Company</span>
        </a>
    </span>
</%def>
