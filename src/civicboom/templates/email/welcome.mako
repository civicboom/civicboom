<%inherit file="./base_email.mako"/>

<%def name="body()">

<h1>${registered_user.name or registered_user.username} - welcome to <a href="${h.url(controller='misc', action='titlepage', sub_domain='www', qualified=True)}">${_('_site_name')}!</a></h1>
<br />
<p>Through ${_('_site_name')} you are able to:</p>

<ul>
	<li>Participate and share your news</li>
	<li>Interact and respond to requests</li>
	<li>Gain recognition from content publishers and organisations</li>
</ul>
<br />
<p style="font-size: 120%">Get started now! <a style="font-weight: bold" href="${h.url('contents', list='assignments_active', sub_domain='www', qualified=True)}">CLICK HERE FOR LATEST REQUESTS</a></p>
<br />

<h2><i>Coming soon!</i></h2>
<p>Direct webcam and audio responses/requests - for a faster, richer collaboration experience.</p>
<br />

<p style="font-size: 120%; font-weight: bold">Got Android? <a href="${h.url(controller='about', action='mobile', sub_domain='www', qualified=True)}">Grab the app HERE!</a></p>
<br />

<p>Remember - we're in Beta and we need your help to make us better. So send us your feedback by clicking the Feedback button at the bottom left of every page.</p>
<br />

<p>Happy booming!</p>
<br />

${self.footer()}
</%def>
