<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name")}</%def>

<h1>${_("About _site_name")}</h1>

See the links on the right for details


<%def name="breadcrumbs()">
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url(controller='misc', action='about', id='index')}" itemprop="url">
		<span itemprop="title">About</span>
	</a>
</span>
&rarr;
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url(controller='misc', action='about', id='civicboom')}" itemprop="url">
		<span itemprop="title">Company</span>
	</a>
</span>
</%def>

