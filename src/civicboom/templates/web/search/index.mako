<%inherit file="/web/common/html_base.mako"/>
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
	<br>Near: ${loc.location_picker()}
	<br>During:
	<input type="text" class="datepicker" name="from"> -
	<input type="text" class="datepicker" name="to">
	<script type="text/javascript">
	$(function() {
		$(".datepicker").datepicker();
	});
	</script>
	<input type="submit">
</form>
</%def>
