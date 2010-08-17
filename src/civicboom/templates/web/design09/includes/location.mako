<%def name="autocomplete_location(field_name='location', map=True, size='250px')">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
% if map:
	${minimap(name=field_name+"_map", width=size, height=size, provider="google", box=field_name)}
% endif
<script>autocomplete_location("${field_name}", ${field_name}_map);</script>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13, overlay=None, marker=None, provider='openlayers', box=None)">
<!-- map div -->
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>

<!-- link to APIs -->
% if provider == "openlayers":
<script src="http://openlayers.org/api/OpenLayers.js"></script>
% elif provider == "google":
<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAIi6se4J7Z6hKgcsUhgiErRQS76dJNGDaz2wU_zf_o-LlW8DpkhThfgwBtV5bzJz31JYsXf4OsNuZZw" type="text/javascript"></script>
% endif

<!-- combine APIs -->
<script type="text/javascript" charset="utf-8" src="/javascript/mxn/mxn.js?(${provider})"></script>

<!-- use the combined API -->
<script type="text/javascript">
${name} = make_map('${name}_div', '${provider}', ${lat}, ${lon}, ${zoom}, '${overlay}', '${box}');
</script>
</%def>
