<%def name="autocomplete_location(field_name='location', map=True, size='250px')">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
% if map:
	${minimap(name=field_name+"_map", width=size, height=size)}
% endif
<script>autocomplete_location("${field_name}_name", "${field_name}_comp", "${field_name}", ${field_name}_map);</script>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13)">
<script src="/javascript/_openlayers.js"></script>
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>
<script>
${name} = new OpenLayers.Map("${name}_div", { controls: [] });
${name}.addLayer(new OpenLayers.Layer.OSM());
lonlat = new OpenLayers.LonLat(${lon},${lat}).transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
          );
${name}.setCenter(lonlat, ${zoom});
</script>
</%def>
