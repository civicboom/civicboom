# -*- coding: utf-8 -*-
<style>
#searchrow INPUT {
	width: 100%;
}
</style>
<thead>
  <tr>
    %for field in collection.render_fields.itervalues():
      <th>${F_(field.label_text or collection.prettify(field.key))|h}</th>
    %endfor
  </tr>
  <tr id="searchrow">
  <form action="${h.url('current')}" method="GET">
    %for field in collection.render_fields.itervalues():
	  % if field.key == "edit":
      <th colspan="2"><input type="submit" value="Search"></th>
	  % elif field.key == "delete":
      <!-- none -->
	  % else:
	  <th>${field.render()|n}</th>
	  % endif
    %endfor
  </form>
  </tr>
</thead>

<tbody>
%for i, row in enumerate(collection.rows):
  <% collection._set_active(row) %>
  <tr class="${i % 2 and 'odd' or 'even'}">
  %for field in collection.render_fields.itervalues():
    <td>${field.render_readonly()|n}</td>
  %endfor
  </tr>
%endfor
</tbody>
