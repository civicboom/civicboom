<%def name="autocomplete_location(field_name='location')">
	<div style="width: 180px; padding-bottom: 2em;">
		<input id="${field_name}_name" name="${field_name}_name" type="text">
		<div id="${field_name}_comp"></div>
		<input id="${field_name}" name="${field_name}" type="hidden">
		<script>autocomplete_location("${field_name}_name", "${field_name}_comp", "${field_name}");</script>
	</div>
</%def>
