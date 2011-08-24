<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

<div class="links">
<a href="${h.url(controller='misc', action='about', id='civicboom')}">${_("About")}</a>
<!--<a href="${h.url(controller='misc', action='about', id='press'  )}">${_("Press")}</a>-->
<a href="${h.url(controller='misc', action='about', id='terms'  )}">${_("Terms")}</a>
<a href="${h.url(controller='misc', action='about', id='privacy')}">${_("Privacy")}</a>
<a href="${h.url(controller='misc', action='about', id='developers')}">${_("Developers")}</a>

<a class="icon16 i_twitter"  href="http://twitter.com/civicboom"                                       title="${_('Follow us on Twitter')         }"    target="_blank"><span>Twitter</span></a>
<a class="icon16 i_facebook" href="http://www.facebook.com/home.php#!/pages/Civicboom/141877465841094" title="${_('Join us on Facebook')          }"    target="_blank"><span>Facebook</span></a>
<a class="icon16 i_mobile"   href="${url(controller='misc', action='about', id='mobile')}"             title="${_('Get the _site_name mobile app')}"><span>${_("_site_name Mobile App")}</span></a>
</div>

<div class="copyright">
    ##<a href="mailto:feedback@civicboom.com">${_("Please send us your Feedback")}</a>
    ${popup.link(
        h.args_to_tuple(controller='misc', action='feedback'),
        title = _('Feedback'),
        text  = h.literal("<strong>%s</strong>" % _("Feedback")),
    )}

	${_(u"Website © Indiconews Ltd, articles © their respective authors")}
    - ${_("Version:")}
    % if config['development_mode']:
        <b>Dev</b>
    % else:
        ${request.environ['app_version']}
    % endif
    
</div>
