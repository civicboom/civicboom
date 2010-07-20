<%def name="render_short_field(field)">
% if field.requires_label:
	<tr class="input_row">
		<td><label class="${field.is_required() and 'field_req' or 'field_opt'}" for="${field.renderer.name}">${[field.label_text, fieldset.prettify(field.key)][int(field.label_text is None)]|h}</label></td>
		<td>
			${field.render()|n}
			% if 'instructions' in field.metadata:
				<span class="instructions">${field.metadata['instructions']}</span>
			% endif
			% for error in field.errors:
				<span class="field_error">${_(error)}</span>
			% endfor
		</td>
	</tr>
% else:
	<tr>
		<td colspan="2">${field.render()|n}</td>
	</tr>
% endif
</%def>

<%def name="style()">
<style>
TD > INPUT[type="text"],
TD > TEXTAREA,
TD > SELECT {
	width: 100%;
}
TD > TEXTAREA {
	height: 150px;
}
.input_row TD:first-child {
	vertical-align: middle;
	text-align: right;
}
TABLE.outer {
	width: 90%;
	margin: auto;
}
TABLE.outer > TBODY > TR > TD {
	border: none;
	width: 50%;
}
TABLE.outer TABLE {
	width: 95%;
}
</style>
</%def>

<%def name="errors(fieldset)">
	% for error in fieldset.errors.get(None, []):
		<div class="fieldset_error">
			${_(error)}
		</div>
	% endfor
</%def>
