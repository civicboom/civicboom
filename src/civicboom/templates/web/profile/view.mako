<%inherit file="/web/layout_3cols.mako"/>

<%def name="col_left()">
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

<%def name="col_right()">
</%def>

<%def name="body()">
</%def>
