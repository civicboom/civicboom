<%inherit file="../../common/widget_content.mako"/>

<h2>${_("What is _site_name?")}</h2>
<ul>
	<li>It is a tool that makes building a news story easier.</li>
</ul>

<h2>${_("What is this widget?")}</h2>
<ul>
    <%
        name = ""
        try:
            name = c.widget['owner']['name']
        except:
            pass
    %>
	<li>${name} is asking you for your news and insight, empowering you to participate in what matters to you.</li>
</ul>
  
<h2>${_("What is the Mobile App?")}</h2>
<ul>
	<li>A simple, fast way for you to participate with eyewitness news coverage on the move.</li>
</ul>
  
<p style="text-align: center; margin-top: 1em; font-weight: bold;">
<a href="${h.url(controller="widget", action="signin")}">${_("Get involved today!")}</a>
</p>
