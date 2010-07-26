<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
  <img src="${c.viewing_user.avatar_url}">
  ${c.viewing_user.name}
  (${c.viewing_user.username})

  <p>Following:
  % for f in c.viewing_user.following:
    ${f.name}
  % endfor

  <p>Followers:
  % for f in c.viewing_user.followers:
    ${f.name}
  % endfor
</%def>
