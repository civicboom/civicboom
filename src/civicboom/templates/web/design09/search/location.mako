<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Search")}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

<form>
    <label for="myInput">Search our database:</label>
	<div style="width: 180px; padding-bottom: 2em;">
		<input id="location_name" name="location_name" type="text">
		<div id="location_comp"></div>
	</div>
	<input id="location_pos" name="location_pos" type="text">
    <input type="submit">
</form>

	% for row in results:
		${row.name}
	% endfor
<script>
autocomplete_location("location_name", "location_comp", "location_pos");
</script>
</%def>
