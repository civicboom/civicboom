# -*- coding: utf-8 -*-
<script>
function search_on(col) {
	v = prompt("Search based on "+col);
	if(v) {
		document.location.search = "?c=" + escape(col) + "&v=" + escape(v);
	}
}
</script>

<thead>
  <tr>
    %for field in collection.render_fields.itervalues():
      <th><a href="javascript:search_on('${field.key}');">${F_(field.label_text or collection.prettify(field.key))|h}</a></th>
    %endfor
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
