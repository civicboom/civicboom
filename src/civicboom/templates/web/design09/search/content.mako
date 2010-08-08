<%inherit file="/web/html_base.mako"/>
<%namespace name="cl" file="../includes/content_list.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Search")}</%def>

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
	% if len(list(results)) > 0:
		% if "location" in request.GET:
		<a href="${url(
			controller='misc',
			action='georss',
			feed=url.current(
				format='xml',
				query=request.GET['query'],
				location=request.GET['location']
			)
		)}">View results on map</a>
		% endif
		<p>${cl.content_list(results)}
	% else:
		'${term}' did not match any articles
	% endif
</%def>
