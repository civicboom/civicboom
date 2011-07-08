<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name & FAQ")}</%def>

<img src="/images/boom128.png" style="float:right;">
<h1>Civicboom connects the people that have news want the </h1>

<p><h2>${_('How does it work? Simple.')}</h2>
${_('1. A news organisation or journalist asks for _articles.')}
${_('2. Their readers respond with videos, photo, audio and text.')}
${_('It really is that simple.')} </p>
 
<p><h2>${_('Civicboom for journalists, bloggers, publishers,  media organisations')}</h2>
${_('- Engage your audience')}
${_('- Get relevant news _articles')}
${_('- Build your community')}</p>

<p><h2>${_('Civicboom for individuals')}</h2>
${_('- Share your _articles and help make the news')}
${_('- Report the unreported')}
${_('- Get published and get recognition')}</p>


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
