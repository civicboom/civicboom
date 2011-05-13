<%inherit file="./base_email.mako"/>

<%def name="body()">

<h1>Welcome to <a href="${h.url('', absolute=True)}">${_('_site_name')}!</a></h1>

<p>What you can do next:</p>

<h2>1. Set a request: </h2>
    <p>Ask your community what you want to know! Generate Followers and get people to participate in what matters to you.</p>

<h2>2. Share: </h2>
    <p>Share on Facebook, Twitter, LinkedIn and other sites.</p>

<h2>3. Make a Hub:</h2>
    <p> A Hub is your "group", a space that is specifically focused on one thing:  it could be an issue, an event, a club, company or brand, so make sure the title of your Hub reflects this (you can change it by clicking on "Hub Settings").</p>
    <p>If you do create a Hub, you are by default Admin. As Admin, you control your Hub and can decide what requests you set or content you publish. You also can decide to invite others who you trust to help "manage" the Hub (these are different to Followers, who are simply alerted to requests or content you publish).</p>

<h2>Got a website?</h2>
    <p>Pop the Hub widget into whatever page you want - customise it to your needs (colour, size) and copy and paste into your web page. (It's titled "Get widget" in top left corner of your Hub fragment - click on this an it'll open up your widget settings with details).</p>


<p>The widget is a simple way your audience or community can see what your asking directly - help them get involved with what matters to you. Whenever someone accepts or responds through your widget, they automatically become a Follower of that Hub - which means they are alerted whenever a new request or content is created by your Hub.</p>

<h2>Psst:</h2>
    <p>Your Hubs can create Sub-Hubs, so if you've created "My Town Local Events" Hub, you can then create a "Summer Festival" Hub which is attached to the My Town Local Events Hub. This way you can manage specific requests, associated with specific issue, events and ideas in an ordered way. </p>

<h2>Please remember we are in Beta</h2>
    <p>So if you have any problems, suggestions or are just tearing your hair out, hit the Feedback button at the bottom right of every page and share with our team. We're here to help!</p>

<h2>Need more help?</h2>
    <p>Check out the <a href="${h.url(controller='misc', action='about', id='howto', absolute=True)}">"How to" videos</a></p>

<p>
Thanks!<br/>
Civicboom Team<br/>
<a href="${h.url('', absolute=True)}">${_('_site_name')}</a>
</p>

</%def>