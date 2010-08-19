<%def name="location_picker(field_name='location', size='250px', lon=1.08, lat=51.28, zoom=13)">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>

<div style="width: ${size}; height: ${size}; border: 1px solid black;" id="${field_name}_div">
	<script type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAIi6se4J7Z6hKgcsUhgiErRQS76dJNGDaz2wU_zf_o-LlW8DpkhThfgwBtV5bzJz31JYsXf4OsNuZZw"></script>
	<script type="text/javascript" src="/javascript/mxn/mxn.js?(google)"></script>
	<script type="text/javascript">
	${field_name}_map = make_map('${field_name}_div', 'google', ${lat}, ${lon}, ${zoom}, '${field_name}');
	autocomplete_location("${field_name}", ${field_name}_map);
	</script>
</div>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13)">
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>
<script type="text/javascript" src="http://openlayers.org/api/OpenLayers.js"></script>
<script type="text/javascript" src="/javascript/mxn/mxn.js?(openlayers)"></script>
<script type="text/javascript">
	${name} = new mxn.Mapstraction("${name}_div", "openlayers");
	${name}.setCenterAndZoom(new mxn.LatLonPoint(${lat}, ${lon}), ${zoom});
	${name}.addControls({pan: false, zoom: false, map_type: false});
</script>
</%def>
