<%inherit file="/web/common/html_base.mako"/>
<%def name="title()">${_("The _site_name Team")}</%def>

<article class="col">

<%include file="toc.mako" />

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
			<p><a href="#"><img src="/images/about/civicboom.png"></a>
			   <a href="#"><img src="/images/about/twitter.png"></a>
			   <a href="http://www.linkedin.com/profile/view?id=24462121&authType=name&authToken=E3z4&goback=.nmp_*1_*1_*1_*1_*1_*1&trk=NUS_UNIU_SHARE-prfl"><img src="/images/about/linkedin.png"></a>
		</td>
	</tr>
	<tr>
		<td><img class="photo" src="/images/about/allan.png"></td>
		<td>
			<h2>Allan Callaghan: Lead Developer</h2>
			<b>Builds Civicboom.</b> Responsible for the technical
			implementation and direction of Civicboom. When not
			locked away as a code monkey, Allan likes to rock out.
			<p><a href="http://www.linkedin.com/profile/view?id=52803166&authType=name&authToken=46ld&goback=.nmp_*1_*1_*1_*1_*1_*1&trk=nus_variable_vname"><img src="/images/about/linkedin.png"></a>
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
			<p><a href="http://www.linkedin.com/profile/view?id=97070386&authType=name&authToken=b03B&goback=.nmp_*1_*1_*1_*1_*1_*1&trk=nus_variable_vname"><img src="/images/about/linkedin.png"></a>
		</td>
	</tr>
	<tr>
		<td colspan="2">
			<h2>In the wings...</h2>
			    Mark Hodgson: Co-Founder
			<br>Emily Chong: Co-Founder and Non-Exec
			<br>Jesse Wolfe: Technology Advisor and Non-Exec
			<br>Paul Andrews: Non-Exec
		</td>
	</tr>
</table>

</article>
