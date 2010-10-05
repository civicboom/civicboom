<%inherit file="/web/common/html_base.mako"/>
<%namespace name="cl" file="/web/design09/includes/content_list.mako"/>
##<%namespace name="loc" file="../includes/location.mako"/>

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
	% if len(d['list']) > 0:
    <%doc>
		<br><a href="${url.current(
			format='xml',
			query=request.params.get('query'),
			location=request.params.get('location')
		)}">RSS feed of results</a>

		<br><a href="${url(
			controller='misc',
			action='georss',
			location=request.params.get('location'),
			feed=url.current(
				format='xml',
				query=request.params.get('query'),
				location=request.params.get('location')
			)
		)}">View results on map</a>
    </%doc>
		<p>${cl.content_list(d['list'])}
	% else:
		'${term}' did not match any articles
	% endif
</%def>
