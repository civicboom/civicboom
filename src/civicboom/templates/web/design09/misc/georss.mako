<%inherit file="/web/html_base.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

<%def name="body()">
% try:
	<% location = request.params.get("location", "0,20,2").split(",") %>
	<div style="width: 100%; height: 600px; border: 1px solid black;" id="map_div">
		<script type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAIi6se4J7Z6hKgcsUhgiErRQS76dJNGDaz2wU_zf_o-LlW8DpkhThfgwBtV5bzJz31JYsXf4OsNuZZw"></script>
		<script type="text/javascript" src="/javascript/mxn/mxn.js?(google)"></script>
		<script type="text/javascript">
			map_map = new mxn.Mapstraction("map_div", "google");
			map_map.setCenterAndZoom(new mxn.LatLonPoint(${float(location[1])}, ${float(location[0])}), ${int(location[2])});
			map_map.addLargeControls();
			map_map.addOverlay("http://alpha.civicboom.com${request.params.get('feed', '/search/content.xml')}");
		</script>
	</div>
% except:
	<span class="error">Error decoding location "${request.params.get("location", "")}"</span>
% endtry
</%def>
