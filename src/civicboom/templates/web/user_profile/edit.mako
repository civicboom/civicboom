<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
  <img src="${c.viewing_user.avatar_url}">
  ${c.viewing_user.name}
  (${c.viewing_user.username})

  <p>Height: ${c.viewing_user.config["height"]}
</%def>
