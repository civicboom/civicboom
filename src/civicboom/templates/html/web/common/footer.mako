<span class="copyright">
	${_(u"Website © Indiconews Ltd, articles © their respective authors")}
</span>

<a href="mailto:feedback@civicboom.com">${_("Please send us your Feedback")}</a>

<a href="${h.url(controller='misc', action='about', id='civicboom')}">${_("About")}</a>
<!--<a href="${h.url(controller='misc', action='about', id='press'  )}">${_("Press")}</a>-->
<a href="${h.url(controller='misc', action='about', id='terms'  )}">${_("Terms")}</a>
<a href="${h.url(controller='misc', action='about', id='privacy')}">${_("Privacy")}</a>
<a href="${h.url(controller='misc', action='about', id='developers')}">${_("Developers")}</a>

<a class="icon icon_twitter"  href="http://twitter.com/civicboom"                                       title="${_('follow us on twitter')         }"><span>twitter</span></a>
<a class="icon icon_facebook" href="http://www.facebook.com/home.php#!/pages/Civicboom/141877465841094" title="${_('join us on facebook')          }"><span>Facebook</span></a>
<a class="icon icon_mobile"   href="${url(controller='misc', action='about', id='mobile')}"             title="${_('get the _site_name mobile app')}"><span>_site_name Mobile App</span></a>