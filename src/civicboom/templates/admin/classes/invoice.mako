<%namespace name="common" file="/admin/classes/common.mako" />

<%!
from civicboom.model.payment import Invoice
from civicboom.model.meta import Session
from civicboom.lib.base import render
%>

${common.errors(fieldset)}

<%
d = Session.query(Invoice).filter(Invoice.id==c.id).one()
%>

<table class="outer">
    <tr>
        <td>
<table>
    <tr><th colspan="2">${_("Overview")}</th></tr>
    ${common.render_short_field(fieldset.id)|n}
    ${common.render_short_field(fieldset.payment_account)|n}
    ${common.render_short_field(fieldset.status)|n}
    ${common.render_short_field(fieldset.timestamp)|n}
    ${common.render_short_field(fieldset.due_date)|n}
    ${common.render_short_field(fieldset.currency)|n}
    ${common.render_short_field(fieldset.tax_rate_code)|n}
    ${common.render_short_field(fieldset.tax_rate)|n}
</table>
        </td>
        <td>
<table>
    <tr><th colspan="2">${_("Invoice Preview")}</th></tr>
    <tr><td>
        ##Render Civicboom Invoice
        <div>
            ${render('/frag/payment_actions/invoice.mako', extra_vars=dict(d=d.to_dict('full')))}
        </div>
    </td></tr>
</table>

<!--         Invoice.id,
        Invoice.payment_account,
        Invoice.status,
        Invoice.timestamp,
        Invoice.due_date,
        Invoice.currency,
        Invoice.taxable,
        Invoice.tax_rate_code,
        Invoice.tax_rate, -->