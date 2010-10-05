<%inherit file="/web/common/html_base.mako"/>
<%def name="title()">${_("Feed: ")+d['feed']['name']}</%def>

<style>
.and, .or, .not, .fil {
    padding: 16px;
    border: 1px solid black;
}   
.and {background: #AFA;}
.or  {background: #AAF;}
.not {background: #FAA;}
.fil {background: #FFF;}
</style>

<%
from civicboom.lib.search import html
%>
${html(d['feed']['query'])|n}
