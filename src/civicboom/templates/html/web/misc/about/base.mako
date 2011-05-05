<%inherit file="/html/web/common/html_base.mako"/>

<!-- can't set max-width on a table in chrome; set it on the div, then set the table to full width... -->
<div class="layout">
<table><tr>

<td class="body">${next.body()}</td>

<td class="nav">
<ul class='toc'>
<li><a class="button" href="${h.url(controller='misc', action='about', id='civicboom'  )}">${_("About")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='howto'      )}">${_("How to")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='team'       )}">${_("Team")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='investors'  )}">${_("Investors")}</a>
<!--<li><a class="button" href="${h.url(controller='misc', action='about', id='press'      )}">${_("Press")}</a>-->
<li><p>
<li><p><a class="button" href="${h.url(controller='misc', action='about', id='plans'   )}">${_("Payment Plans")}</a>
<li><p>
<li><a class="button" href="${h.url(controller='misc', action='about', id='mobile'     )}">${_("Mobile")}</a>
<li><p>
<li><a class="button" href="${h.url(controller='misc', action='about', id='developers' )}">${_("Developers")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='open-source')}">${_("Open Source")}</a>
<li><p>
<li><a class="button" href="${h.url(controller='misc', action='about', id='terms'      )}">${_("Terms")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='privacy'    )}">${_("Privacy")}</a>
</ul>
</td>

</tr></table>
</div>
