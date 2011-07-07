<%inherit file="base.mako"/>
<%def name="title()">${_("_site_name Mobile")}</%def>

<style>
.mobile {
	width: 100%;
}
.mobile TD {
	width: 33%;
	vertical-align: center;
	text-align: center;
	font-size: 1.3em;
}
.mobile TD .button {
	font-size: 1.7em;
	background: orange;
}
</style>

<h1>${_("Make news with the _site_name mobile app")}</h1>

<p>&nbsp;

<table class="mobile"><tr>

<td style="text-align: left;">
<h3>${_("Ask for news out in the field:")}</h3>
${_("Post directly to your organisation's website _widget")}

<p><h3>${_("Get _article _assignments:")}</h3>
${_("Respond in an instant")}

<P><h3>${_("Post _articles from the scene:")}</h3>
${_("Get your news")} <i>${_("in")}</i> ${_("the news")}
</td>

<td>
<img src="/images/about/mobile/phone.png" alt="mobile phone" height="230">
</td>

<td>
<h3>${_("Get the Android app now:")}</h3>
<img src="/images/about/mobile/android.png" alt="android">
<br><a class="button" href="http://market.android.com/details?id=com.civicboom.mobile2" target="blank">Download</a>
</td>

</tr></table>

<p>&nbsp;
<hr>
<p>&nbsp;

<!--
<a href="http://market.android.com/details?id=com.civicboom.mobile2"><img src="/images/about/qr_mobile2.png" style="float: right;"></a>

<h1>${_('_site_name Mobile')}</h1>

<ul class="bulleted">
<li>${_("Get requests directly via your Android mobile")}
<li>${_("Respond in an instant")}
<li>${_("Upload images, video, text and audio")}
</ul>

<p>&nbsp;

<h1>${_("How to get the app")}</h1>
${_("Scan the barcode (opposite) into your phone by using the barcode reader on your handset")}
(If you don't have the barcode reader, you can download the app directly from the
<a href="http://market.android.com/details?id=com.civicboom.mobile2">Android marketplace</a> on your handset)

<p>&nbsp;
-->

<h1>${_("Signed up to _site_name via Facebook, Twitter, LinkedIn, etc? Then once you've downloaded the app:")}</h1>

<ol class="bulleted">
<li>${_("Go to your")} <a href="/settings/me/password">${_("password and mobile access page")}</a>
<li>${_("Make a note of your username")}
<li>${_("Create a password")}
<li>${_("Log into the mobile app on your handset with your username and password")}
</ol>


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
