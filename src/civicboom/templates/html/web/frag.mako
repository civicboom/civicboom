<%doc>
<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">
  ## TODO - if frag has title, use that
</%def>


<%def name="body(frag='help/settings.mako')">
	<%
        self.attr.frags = 'frag'
        self.attr.frag  = frag
	%>
</%def>

<%def name="frag()">
	##<!--#include virtual=""-->
    <%
		frag = "/frag/%s" % self.attr.frag
	%>
    <%include file=frag />
</%def>
</%doc>
