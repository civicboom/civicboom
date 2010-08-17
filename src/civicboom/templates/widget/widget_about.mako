<%inherit file="./widget_content.mako"/>

<h2>What is Civicboom?</h2>
  <ul>
    <li>It is a tool that makes building a news story easier.</li>
  </ul>

<h2>What is this widget?</h2>
  <ul>
    <li>${c.widget_owner.username} is asking you for your news and insight, empowering you to participate in what matters to you.</li>
  </ul>
  
<h2>What is the Mobile App?</h2>
  <ul>
  <li>A simple, fast way for you to participate with eyewitness news coverage on the move.</li>
  </ul>
  
<p style="text-align: center; margin-top: 1em; font-weight: bold;"><a href="${h.url(controller="widget", action="signin")}">Get involved today!</a></p>