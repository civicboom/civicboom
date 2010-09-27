<ul>
	<li>
		${h.secure_link(url('new_content'), _("Create _content"))}
		<div class="tooltip tooltip_icon"><span>${_("Uploading an _article allows you express your ideas, opinions and news to a wider community")}</span></div>
	</li>
	<li>
		<a href="${h.url(controller='search', action='content', type='assignment')}">${_("Find _assignments")}</a>
		<div class="tooltip tooltip_icon"><span>${_("Find open _assignments to respond to")}</span></div>
	</li>
</ul>

<form action="${h.url(controller='search', action='content')}" method='GET'>
	${_("Find")}:
	<input type="search" class="search_input" name="query" placeholder="News, opinions" />
	<input type="submit" class="search_submit" value="" />
</form>
