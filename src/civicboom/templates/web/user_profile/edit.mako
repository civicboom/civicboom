<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<table><tr>
	<img src="${c.viewing_user.avatar_url}">
	<br>${c.viewing_user.name}
	<br>(${c.viewing_user.username})

	<form action="${url.current(action='save', id=c.viewing_user.username)}" method="POST">
		<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
		<fieldset>
			<legend>${_("Avatar")}:</legend>
		% if c.viewing_user.config["avatar"]:
			Civicboom no longer manages user avatars itself, we now link to Gravatar, a service for
			letting users keep their avatars consistent all across the internet. We're keeping old
			avatars active while people switch over, but recommend switching.
			<p>Move to <a href="http://www.gravatar.com/">Gravatar</a>? <input type="checkbox" name="move_to_gravatar">
		% else:
			Manage your avatar with <a href="http://www.gravatar.com">gravatar.com</a>
		% endif
		</fieldset>
		<fieldset>
			<legend>${_("General Info")}:</legend>
			    Home Location: <input name="location" value="${c.viewing_user.config["location"]}">
			<br>Description: <textarea name="description">${c.viewing_user.config["description"]}</textarea>
			<br>Home page: <input name="home_page" value="${c.viewing_user.config["home_page"]}">
		</fieldset>
		<fieldset>
			<legend>${_("Aggregation")}:</legend>
			    Twitter username: <input name="twitter_username" value="${c.viewing_user.config["twitter_username"]}">
			<br>Twitter auth key: <input name="twitter_auth_key" value="${c.viewing_user.config["twitter_auth_key"]}">
			<br>Broadcast instant news: <input type="checkbox" name="broadcast_instant_news" value="${c.viewing_user.config["broadcast_instant_news"]}">
			<br>Broadcast content posts: <input type="checkbox" name="broadcast_content_posts" value="${c.viewing_user.config["broadcast_content_posts"]}">
		</fieldset>
		<input type="submit" value="Save">
	</form>
</tr></table>
</%def>
