<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name & FAQ")}</%def>

<img src="/images/boom128.png" style="float:right;">
<h1>${_("_site_name connects the people that have stories to the people who want stories. How does it work? Simple.")}</h1>

<ol>
	<li>${_('A journalist, blogger, publisher or media organisation asks for stories.')}</li>
	<li>${_('Their audience responds directly with videos, photo, audio and text.')}</li>
	</ol>
</p>
 
<p><h2>${_('Civicboom for journalists, bloggers, publishers,  media organisations:')}</h2>
<ul>
	<li>${_('Engage your audience')}</li>
	<li>${_('Get relevant news _articles')}</li>
	<li>${_('Build your community')}</li>
</ul>
</p>

<p><h2>${_('Civicboom for individuals')}</h2>
<ul>
	<li>${_('Share your _articles and help make the news')}</li>
	<li>${_('Report the unreported')}</li>
	<li>${_('Get published and get recognition')}</li>
</ul>
</p>

<p><h1><a href="/account/signin" class="button" style="float:right;"> ${_("Sign up")} </a></h1>
<h1>${_("_tagline")}</h1>


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
