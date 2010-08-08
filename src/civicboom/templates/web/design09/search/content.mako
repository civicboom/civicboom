<%inherit file="/web/html_base.mako"/>
<%namespace name="cl" file="../includes/content_list.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Search")}</%def>

##------------------------------------------------------------------------------
## Navigation override - remove it
##------------------------------------------------------------------------------
##<%def name="navigation()"></%def>

##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
<%def name="styleOverides()">
#content_list {
	margin: auto;
}
#content_list TD {
	border: 1px solid black;
	padding: 4px;
	vertical-align: top;
}
TD.avatar {
	text-align: center;
	width: 80px;
}
IMG.avatar {
	border: 1px solid #888;
}
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	% if location:
		<%
		# we need to pass the session to GeoAlchemy functions
		from civicboom.model.meta import Session
		%>
			<p>${loc.minimap(
				width="100%", height="600px",
				lon=location[0],
				lat=location[1],
				zoom=location[2]
			)}

		<!-- JS to add to map -->
		<script>
		% for r in results:
my_marker = new mxn.Marker(new mxn.LatLonPoint(${location[1]}, ${location[0]}));
my_marker.setIcon('http://mapstraction.com/icon.gif');
my_marker.setLabel("${r.title}");
my_marker.setInfoBubble("<b>${r.title}</b><p>${r.content}");
map.addMarker(my_marker);
		% endfor
		</script>
	% endif

	% if len(list(results)) > 0:
		${cl.content_list(results)}
	% else:
		'${term}' did not match any articles
	% endif
</%def>
