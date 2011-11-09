<%inherit file="/html/web/common/html_base.mako"/>
<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>

<%doc>
<!-- can't set max-width on a table in chrome; set it on the div, then set the table to full width... -->
<div class="layout">
<table><tr>

<td class="body page_border">
	${next.body()}
	<p style="height: 0px; margin: 0px;"><!-- hack to widen the table up to its max-width, while remaining shrinkable -->
	% for n in range(0, 50):
		&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
	% endfor
</td>

<td class="nav">
<ul class='toc'>
<li><a class="button" href="${h.url(controller='misc', action='about', id='civicboom'  )}">${_("About")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='faq'      )}">${_("FAQ")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='team'       )}">${_("Team")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='investors'  )}">${_("Investors")}</a>
<!--<li><a class="button" href="${h.url(controller='misc', action='about', id='press'      )}">${_("Press")}</a>-->
<li><p>
<li><a class="button" href="${h.url(controller='misc', action='about', id='upgrade_plans')}">${_("Upgrade Plans")}</a>
<li><p>
<li><a class="button" href="${h.url(controller='misc', action='about', id='mobile'     )}">${_("Mobile")}</a>
<li><a class="button" href="${h.url(controller='misc', action='about', id='mobile-map' )}">${_("Mobile Map")}</a>
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
</%doc>

<div class="content_wrapper">
    <div class="content">
        ${next.body()}
    </div>
    ${nav()}
</div>

${components.misc_footer()}

<%def name="nav()">
    <div class="nav">
        <p>
            <a href="${h.url(controller='misc', action='about', id='civicboom'  )}">${_("About")}</a>
            <a href="${h.url(controller='misc', action='about', id='faq'      )}">${_("FAQ")}</a>
            <a href="${h.url(controller='misc', action='about', id='team'       )}">${_("Team")}</a>
            <!--<a href="${h.url(controller='misc', action='about', id='investors'  )}">${_("Investors")}</a>-->
            <!--<li><a class="button" href="${h.url(controller='misc', action='about', id='press'      )}">${_("Press")}</a>-->
        <!--
        </p><p>
            <a href="${h.url(controller='misc', action='about', id='upgrade_plans')}">${_("Upgrade Plans")}</a>
        -->
        </p><p>
            <a href="${h.url(controller='misc', action='about', id='mobile'     )}">${_("Mobile")}</a>
            <a href="${h.url(controller='misc', action='about', id='mobile-map' )}">${_("Mobile Map")}</a>
        </p><p>
            <a href="${h.url(controller='misc', action='about', id='developers' )}">${_("Developers")}</a>
            <a href="${h.url(controller='misc', action='about', id='open-source')}">${_("Open Source")}</a>
        </p><p>
            <a href="${h.url(controller='misc', action='about', id='terms'      )}">${_("Terms")}</a>
            <a href="${h.url(controller='misc', action='about', id='privacy'    )}">${_("Privacy")}</a>
        </p>
    </div>
</%def>