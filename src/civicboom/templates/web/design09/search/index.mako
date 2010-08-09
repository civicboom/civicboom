<%inherit file="/web/html_base.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Search")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
<form action='${url(controller="search", action="content")}' method='GET'>
	Search For: <input type="text" name="query" value="">
	<br>Near: ${loc.autocomplete_location()}
	<input type="submit">
</form>
</%def>
