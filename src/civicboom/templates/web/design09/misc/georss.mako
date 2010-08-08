<%inherit file="/web/html_base.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

<%def name="body()">
<%
# we need to pass the session to GeoAlchemy functions
from civicboom.model.meta import Session
%>
${loc.minimap(
	width="100%", height="600px",
	#lon=location[0],
	#lat=location[1],
	#zoom=location[2],
	overlay=request.GET['feed']
)}
</%def>
