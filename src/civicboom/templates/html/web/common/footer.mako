<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

<span class="copyright">
    ##<a href="mailto:feedback@civicboom.com">${_("Please send us your Feedback")}</a>
    ${popup.link(
        h.args_to_tuple(controller='misc', action='feedback'),
        title = _('Feedback'),
        text  = h.literal("<strong>%s</strong>" % _("Feedback")),
    )}

	${_(u"Website © Indiconews Ltd, articles © their respective authors")}
</span>



<a href="${h.url(controller='misc', action='about', id='civicboom')}">${_("About")}</a>
<!--<a href="${h.url(controller='misc', action='about', id='press'  )}">${_("Press")}</a>-->
<a href="${h.url(controller='misc', action='about', id='terms'  )}">${_("Terms")}</a>
<a href="${h.url(controller='misc', action='about', id='privacy')}">${_("Privacy")}</a>
<a href="${h.url(controller='misc', action='about', id='developers')}">${_("Developers")}</a>

<a class="icon16 twitter"  href="http://twitter.com/civicboom"                                       title="${_('follow us on twitter')         }"><span>Twitter</span></a>
<a class="icon16 facebook" href="http://www.facebook.com/home.php#!/pages/Civicboom/141877465841094" title="${_('join us on facebook')          }"><span>Facebook</span></a>
<a class="icon16 mobile"   href="${url(controller='misc', action='about', id='mobile')}"             title="${_('get the _site_name mobile app')}"><span>${("_site_name Mobile App")}</span></a>
