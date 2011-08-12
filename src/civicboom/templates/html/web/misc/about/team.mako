<%inherit file="base.mako"/>
<%def name="title()">${_("The _site_name Team")}</%def>

<h1>The Civicboom Team</h1>

<style>
.team .photo {
	height: 150px;
	width:  122px;
}
.team TD {
	vertical-align: top;
	padding: 16px;
}
.team H2 {
	font-size: 2em;
}
</style>
<table class='team'>
	<tr>
		<td><img class="photo" src="/images/about/elizabeth.png"></td>
		<td>
			<h2>Elizabeth Hodgson: Founder & CEO</h2>
			<b>Conceived Civicboom.</b> Passionate about how
			digital technologies can empower and engage society
			in participatory and collaborative agendas. Elizabeth is
			a big fan of the great outdoors... when work allows.
			<p><a href="/members/civicboom"><img src="/images/about/civicboom.png"></a>
			   <a href="http://www.twitter.com/civicboom"    target="_blank"><img src="/images/about/twitter.png"></a>
			   <a href="http://uk.linkedin.com/in/elizabethhodgson"  target="_blank"><img src="/images/about/linkedin.png"></a>
			   <a href="mailto:contact@civicboom.com"><img src="/images/about/email.png"></a>
			</p>
		</td>
	</tr>
	<tr>
		<td><img class="photo" src="/images/about/allan.png"></td>
		<td>
			<h2>Allan Callaghan: Lead Developer</h2>
			<b>Builds Civicboom.</b> Responsible for the technical
			implementation and direction of Civicboom. When not
			locked away as a code monkey, Allan likes to rock out.
			<p><a href="http://www.linkedin.com/pub/allan-callaghan/15/825/47a"  target="_blank"><img src="/images/about/linkedin.png"></a></p>
		</td>
	</tr>
	<tr>
		<td><img class="photo" src="/images/about/shish.png"></td>
		<td>
			<h2>Chris "Shish" Girling: Server Manager</h2>
			<b>Drives Civicboom.</b> Keeps the website and API running
			smoothly, making sure it doesn't crash from the load when
			a massive story breaks. Ever practical, Shish spends his
			spare time adding useful features to his clothes...
			<p><a href="http://uk.linkedin.com/pub/chris-girling/28/612/baa" target="_blank"><img src="/images/about/linkedin.png"></a></p>
		</td>
	</tr>
  <tr>
    <td><img class="photo" src="/images/about/greg.png"></td>
    <td>
      <h2>Greg Miell: Developer</h2>
      <b>Extends Civicboom.</b> Develops new technologies to
      interface with the Civicboom platform. When not in the office,
      Greg can sometimes be caught drinking a pint or two of local ale.
      <p><a href="http://uk.linkedin.com/in/gregmiell"  target="_blank"><img src="/images/about/linkedin.png"></a></p>
    </td>
  </tr>
</table>


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
