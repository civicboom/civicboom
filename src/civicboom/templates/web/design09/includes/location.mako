<%def name="autocomplete_location(field_name='location', map=True, size='250px')">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
% if map:
	${minimap(name=field_name+"_map", width=size, height=size)}
% endif
<script>autocomplete_location("${field_name}", ${field_name}_map);</script>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13, overlay=None)">
<!-- map div -->
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>

<!-- link to APIs -->
<script src="/javascript/_openlayers.js"></script>

<!-- combine APIs -->
<script type="text/javascript" charset="utf-8" src="/javascript/mxn/mxn.js?(openlayers)"></script>

<!-- use the combined API -->
<script type="text/javascript">
	${name} = new mxn.Mapstraction('${name}_div','openlayers');
	${name}.setCenterAndZoom(new mxn.LatLonPoint(${lat}, ${lon}), ${zoom});
	${name}.addControls({
		pan: false,
		zoom: false,
		map_type: false
	});
	% if overlay:
	${name}.addOverlay("${overlay}");
	% endif
</script>
</%def>
