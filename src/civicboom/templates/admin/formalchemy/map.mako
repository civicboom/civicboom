<%
# default configuration options that will be used when
# no field options were set, e.g. with:
#
# Place = FieldSet(model.places.Place)
# Place.the_geom.set(options=[('zoom', 12), ..]) 

options = {}
options['default_lon'] = 10
options['default_lat'] = 45
options['zoom'] = 4
options['map_width'] = "100%"
options['map_height'] = 200
options['base_layer'] = 'new OpenLayers.Layer.WMS("WMS", "http://labs.metacarta.com/wms/vmap0", {layers: "basic"})'
options['openlayers_lib'] = '/javascript/_combined.maps.js'

%>

<script src="${openlayers_lib or options['openlayers_lib']}"></script>

<style>
.formmap_${field_name} {
    width: ${map_width or options['map_width']}px;
    height: ${map_height or options['map_height']}px;
    border: 1px solid #ccc;
}

.olControlAttribution {
    bottom: 2px; 
}

.olControlEditingToolbar .olControlModifyFeatureItemActive { 
    background-image: url("http://openlayers.org/api/theme/default/img/draw_point_on.png")
}
.olControlEditingToolbar .olControlModifyFeatureItemInactive { 
    background-image: url("http://openlayers.org/api/theme/default/img/draw_point_off.png")
}
</style>

<div>
    ${input_field}
    <div id="map_${field_name}" class="formmap_${field_name}"></div>
    <script type="text/javascript">
        <%include file="map_js.mako" />
        geoformalchemy.init_map(
                '${field_name}',
                ${read_only},
                ${is_collection},
                '${geometry_type}',
                ${default_lon or options['default_lon']},
                ${default_lat or options['default_lat']},
                ${zoom or options['zoom']},
				// FIXME: hack to force OSM
                //${base_layer or options['base_layer'] | n},
				new OpenLayers.Layer.OSM("OSM"),
                '${wkt}'
        );
    </script>
    <br />
</div>
