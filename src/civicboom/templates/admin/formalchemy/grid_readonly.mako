# -*- coding: utf-8 -*-
<thead>
  <tr>
    %for field in collection.render_fields.itervalues():
      <th>${F_(field.label_text or collection.prettify(field.key))|h}</th>
    %endfor
  </tr>
  <tr>
  <form action="${url.current()}" method="GET">
    %for field in collection.render_fields.itervalues():
	  % if field.key == "edit":
      <th colspan="2"><input style="width: 100%;" type="submit" value="Search"></th>
	  % elif field.key == "delete":
      <!-- none -->
	  % else:
	    % if field.key in request.GET:
        <th><input type="text" style="width: 100%;" name="${field.key}" value="${request.GET[field.key]}"></th>
		% else:
        <th><input type="text" style="width: 100%;" name="${field.key}" value=""></th>
		% endif
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
