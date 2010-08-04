<%def name="autocomplete_location(field_name='location', map=True, size='250px')">
<script src="/javascript/_openlayers.js"></script>
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
% if map:
<div style="width: ${size}; height: ${size}px; border: 1px solid black;" id="${field_name}_mapdiv"></div>
<script>
${field_name}_map = new OpenLayers.Map("${field_name}_mapdiv", { controls: [] });
${field_name}_map.addLayer(new OpenLayers.Layer.OSM());
lonlat = new OpenLayers.LonLat(1.08,51.28).transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
          );
${field_name}_map.setCenter(lonlat, 13);
autocomplete_location("${field_name}_name", "${field_name}_comp", "${field_name}", ${field_name}_map);
</script>
% else:
<script>
autocomplete_location("${field_name}_name", "${field_name}_comp", "${field_name}", False);
</script>
% endif
</%def>
