<%inherit file="/html/web/common/html_base.mako"/>
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="footer()">${components.misc_footer()}</%def>
<%def name="contact_us()">
    <%
        popup.link(
            h.args_to_tuple(controller='misc', action='contact_us'),
            title = _('Contact us'),
            text  = h.literal("<span class='learn_more button'>%s</span>") % _('Contact us'),
        )
    %>
</%def>
<%def name="sign_up()">
    <a class="button" href="${url(controller='account', action='signin')}">
        ${_('Sign up')}
    </a>
</%def>

<div class="content_wrapper">
    <div class="content">
        ${next.body()}
    </div>
    ${nav()}
</div>

<%def name="nav()">
    <div class="nav">
        <p>
            <a href="${h.url(controller='misc', action='about', id='civicboom'  )}">${_("About")}</a>
            <a href="${h.url(controller='misc', action='about', id='organisations'  )}">${_("Organisations")}</a>
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
