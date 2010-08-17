<%def name="autocomplete_member(field_name='member', size='250px')">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
<script>autocomplete_member("${field_name}_name", "${field_name}_comp", "${field_name}");</script>
</%def>


<%def name="avatar(member)">
    ## Todo: use size? or class?
    <a href="${h.url(controller='profile', action='view', id=member.username)}"><img src="${member.avatar_url}" /></a>
</%def>