<%inherit file="base.mako"/>

<%def name="title()">${_("FAQ's for _site_name")}</%def>

<h1>${_("FAQ")}</h1>

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
