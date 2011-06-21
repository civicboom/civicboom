<%inherit file="base.mako"/>
<%def name="title()">${_("Credits")}</%def>

<h1>Open Source &amp; Credits</h1>

<p>Civicboom is built on open source foundations. As well as sending patches upstream
whenever we fix bugs or add features, the scripts and tools that we write internally
(but can be used as standalone programs) are available from
<a href="https://github.com/civicboom">our github page</a>.

<!--
bugs reported in other people's trackers:
http://code.google.com/p/page-speed/issues/detail?id=448 - png optimisation
https://bitbucket.org/bbangert/beaker/issue/62/some-way-to-set-httponly-cookies
https://bitbucket.org/bbangert/beaker/issue/63/secure-auto-cookie-setting
http://www.sqlalchemy.org/trac/ticket/2079 - unicode col with non-unicode default
http://trac.pythonpaste.org/pythonpaste/ticket/483 - urlparse.parse_qsl rather than cgi
https://bugs.launchpad.net/ubuntu/+source/lazr.uri/+bug/725124 - lazr missing __init__.py
-->
<div>
<b>Front End:</b>

<p>Web server / cache -
	<a href="http://nginx.org/">nginx</a> -
	BSD

<p>Media Player -
	<a href="http://flv-player.net/players/maxi/">FLV Player Maxi</a> -
	CC-By-SA -
	&copy; Neolao

<p>File Uploader -
	<a href="http://www.uploadify.com">Uploadify</a> -
	MIT -
	&copy; Ronnie Garcia, Travis Nickels

<p>Javascript niceness -
	<a href="http://jquery.com/">jQuery</a> -
	MIT

<p>Rich Text Editor -
	<a href="http://tinymce.moxiecode.com/">TinyMCE</a> -
	LGPLv2

<p>Feature detection -
	<a href="http://www.modernizr.com/">Modernizr</a> -
	MIT

<p>Icon Mapper -
	<a href="http://oranlooney.com/make-css-icons-python-image-library/">Script</a> -
	CC-By-SA -
	&copy; Oran Looney, Shish

</div>

<div>
<b>Back End:</b>

<p>Web Framework -
	<a href="http://pylonshq.com/">Pylons</a> -
	BSD -
	&copy; Ben Bangert, James Gardner, Philip Jenvey and contributors.
<!--
python-webhelpers - BSD
python-imaging    - BSD-like?
python-boto       - BSD-like? + amazon disclaimer
python-authkit    - MIT
python-memcache   - python v2
python-nose       - LGPLv2  [aggregated]
python-coverage   - BSDv2   [aggregated]
python-dns        - CNRI OPEN SOURCE GPL-COMPATIBLE LICENSE AGREEMENT
python-recaptcha  - MIT
python-decorator  - 2-clause BSD
python-lxml       - BSD + Python (plus some other bits which are explicitly marked as aggregated not linked)
python-pybabel    - BSD-like?

mako              - MIT
formalchemy       - MIT
python-magic      - PSF
GeoAlchemy        - MIT
GeoFormAlchemy    - MIT
twitter           - MIT
pexif             - MIT
-->

<p>DB Framework -
	<a href="http://pylonshq.com/">SQLAlchemy</a> -
	BSD -
	&copy; Michael Bayer and contributors.
<!--
python-psycopg2   - GPL + exception that proprietary use is allowed as long as
                    we only use the published psycopg API and don't touch the
					internals
					Newer versions are standard LGPLv3
-->

<p>Database -
	<a href="http://www.postgresql.org/">PostgreSQL</a> -
	<a href="http://www.postgresql.org/about/licence">PostgreSQL License</a> [MIT/BSD-like] -
	&copy; The PostgreSQL Global Development Group

<p>Cache -
	<a href="http://redis.io/">Redis</a>
	BSD

</div>

<div>
<b>Mapping:</b>

<p>Map data -
	<a href="http://www.openstreetmap.org/">OpenStreetMap</a> -
	CC-By-SA -
	&copy; OSM Contributors

<p>Map interaction -
	<a href="http://www.openlayers.org/">OpenLayers</a> -
	BSD -
	&copy; OpenLayers Contributors.

<!-- only used internally, our codebases are separate
<p>Map data loading -
	<a href="http://www.openlayers.org/">osm2pgsql</a> -
	GPLv2 -
	&copy; Jon Burgess, Artem Pavlenko
-->
</div>

<!-- these only appear in our internal test data
<div>
<b>Images:</b>

<p>KM Avatar -
	<a href="">Kent Messanger Group</a> -
	&copy;, fair use

<p>Mobiletest Avatar -
	<a href="http://www.flickr.com/photos/johnkarakatsanis/4805593861/">John.Karakatsanis</a> -
	CC-BY-SA
</div>
-->

<div>
<b>Icons:</b>

<p><a href="http://www.iconarchive.com/category/application/basic-icons-by-pixelmixer.html">Set 1</a>, <a href="http://www.iconarchive.com/category/application/basic-2-icons-by-pixelmixer.html">Set 2</a> -
	<a href="http://pixel-mixer.com/">pixel-mixer</a> -
	Commercial use allowed with link to pixel-mixer.com
</div>

<p>Social Network Icon Pack by Komodo Media, Rogie King is licensed under a Creative Commons Attribution-Share Alike 3.0 Unported License.</p>
<a href="http://www.komodomedia.com/download/#social-network-icon-pack">komodomedia.com</a>
Creative Commons License

<p>
    <a href="http://www.softicons.com/free-icons/toolbar-icons/16x16-free-toolbar-icons-by-aha-soft/mobile-icon">Aha-Soft</a> mobile icon
</p>


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
