<%inherit file="base.mako"/>
<%def name="title()">${_("Investors")}</%def>

<h1>Investors</h1>
<!--<p>After Seeding Funding and Round 1 external investment we are
now in the process of opening up Round 2 investment discussions
to further expand the Civicboom platform.</p>-->
<p>Round 3 investment completed june 2011.</p>
<p>Round 4 business plan available to FSA qualified investors.</p>

<h2>Interested parties</h2>
<p>Please email <a href="mailto:investors@civicboom.com">investors@civicboom.com</a></p>

##<h2>Interested in Investing?</h2>
##<p>Please contact ...</p>


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
