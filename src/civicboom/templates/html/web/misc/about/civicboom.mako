<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name & FAQ")}</%def>

<img src="/images/boom128.png" style="float:right;">
<h1>Civicboom empowers you to connect, create
and collaborate on what matters to you.</h1>

<p><h2>How does it work? Simple.</h2>
1. A news organisation or journalist asks for stories.
2. Their readers respond with videos, photo, audio and text.
It really is that simple. </p>
 
<p><h2>Civicboom for journalists, bloggers, publishers,  media organisations</h2>
- Engage your audience
- Get relevant news stories
- Build your community</p>

<p><h2>Civicboom for individuals</h2>
- Share your stories and help make the news
- Report the unreported
- Get published and get recognition</p>


<p><h1><a href="/account/signin" class="button" style="float:right;"> Sign up </a></h1>
<h1>Don't just read it. Feed it.</h1>


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
