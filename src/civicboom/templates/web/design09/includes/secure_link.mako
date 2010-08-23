## the lack of newlines here is because we don't want whitespace to appear in the output
<%def name="secure_link(href, value='Submit', vals=[], css_class='')"><%
import hashlib
hhash = hashlib.md5(str([href, value, vals])).hexdigest()[0:4]
%><span class="secure_link"><!--
--><span id="span_${hhash}"><form id="form_${hhash}" action="${href}" method="POST">
<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
% for k, v in vals:
<input type="hidden" name="${k}" value="${v}">
% endfor
<input type="submit" value="${value}"></form></span><!--
--><a
	id="link_${hhash}"
	style="display: none;"
	href="${href}"
	class="${css_class}"
	onClick="secure_submit_${hhash}(); return false;"
>${value}</a><script>
document.getElementById("span_${hhash}").style.display = "none";
document.getElementById("link_${hhash}").style.display = "inline";
function secure_submit_${hhash}() {document.getElementById("form_${hhash}").submit();}
</script></span></%def>
