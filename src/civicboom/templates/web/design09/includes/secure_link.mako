## the lack of newlines here is because we don't want whitespace to appear in the output
<%def name="secure_link(href, value='Submit', vals=[])"><form class="secure_link" action="${href}" method="POST">
<style>
.secure_link {display: inline;}
.secure_link INPUT {background: white; border: none;}
</style>
<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
% for k, v in vals:
<input type="hidden" name="${k}" value="${v}">
% endfor
<input type="submit" value="${value}"></form></%def>
