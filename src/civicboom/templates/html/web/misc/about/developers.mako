<%inherit file="base.mako"/>
<%def name="title()">${_("Civicboom For Developers")}</%def>

<h1>Civicboom For Developers</h1>

<p>We want you to create new ways of using Civicboom.
We have no idea what will be built - but that's the fun part. We hope to
see some interesting creations that bring Civicboom to life for yourselves.

<p><a class="button" style="width: 200px" href="/doc/">API documentation</a>
<p><a class="button" style="width: 200px" href="${url(controller='misc', action='about', id='developer-terms')}">API Terms & Conditions</a>

<p>Email <a href="mailto:developers@civicboom.com">developers@civicboom.com</a> if you have questions or suggestions


<%def name="breadcrumbs()">
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
		<span itemprop="title">About</span>
	</a>
</span>
&rarr;
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
		<span itemprop="title">Technology</span>
	</a>
</span>
</%def>
