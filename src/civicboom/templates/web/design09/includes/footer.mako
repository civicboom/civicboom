<div id="footer" class="yui-g">

  <div class="yui-u first">
    <a href="mailto:feedback@civicboom.com" class='feedback_link'>${_("Please send us your Feedback")} <span class="icon_large icon_comment footer_feedback_icon">&nbsp;</span></a>
    <a href="${h.url(controller='misc', action='contact')}" class='more_contacts'>(${_("more contact details")})</a>    
  </div>
  
  <div class="yui-u unit_b">
    ##<ul>
    ##  <li><a href="${h.url_for(controller='frontpage', action='frontpage')  }">Frontpage</a></li>
    ##  <li><a href="${h.url_for(controller='misc'     , action='about')      }">About</a></li>
    ##  <li><a href="${h.url_for(controller='misc'     , action='get_started')}">Get Started</a></li>
    ##  <li><a href="${h.url_for(controller='frontpage', action='latest')     }">Latest</a></li>
    ##  <li class="last_list_item"><a href="${h.url_for(controller='search'  , action='newsmap')    }">News Map</a></li>
    ##</ul>

    ## AllanC - bit of a hack here, on the registration page or upload page we dont want users
    ##          being navigated away from a full form, so the legal links open in new windows.
    <%
      link_target = ''
      #if c.terms_open_in_new_window:
      #  link_target = ' target="_black"'
    %>
    <ul class="legal_list">
      <li                       ><a href="${h.url(controller='misc', action='about'      )}"               >${_("About")}</a></li>
      <li                       ><a href="${h.url(controller='misc', action='press'      )}"               >${_("Press Coverage")}</a></li>
      <li                       ><a href="${h.url(controller='misc', action='terms'      )}" ${link_target}>${_("Terms and Conditions")}</a></li>
      <li class="last_list_item"><a href="${h.url(controller='misc', action='privacy'    )}" ${link_target}>${_("Privacy policy")}</a></li>
    </ul>

    <div class="copyright">
		<span class="copyright_symbol">&copy;</span> 2009-2010 Indiconews Ltd,
		Map Data CC-By-SA by <a href="http://openstreetmap.org/">OpenStreetMap</a>
	</div>
  </div>
  
</div>
