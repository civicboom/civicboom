<%inherit file="base_misc.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Welcome")}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
  
  <div id="titlepage" class="background_gradient_dark">
    <div class="site_description">
      ${_("_site_description")}.
      ##Interested? Then sign up to learn more.
    </div>

    
    <div class="learn_more">
      <p style="font-size: larger;">${_("Try us now")}</p>
      <p>${_("Organisations &amp; Media:")} <a class="learn_more_link" href="${h.url(controller='misc', action='get_started_organisations')}">${_("Learn more")}</a></p>
      <p>${_("Individuals:")}               <a class="learn_more_link" href="${h.url(controller='misc', action='get_started')}">${_("Learn more")}</a></p>
    </div>
    
    <div class="clearboth_hack"></div>
    
    <div class="signup">
      <form action="${h.url(controller='register', action='email')}" method="post">
        ##<fieldset><legend>${_("Sign up today")}</legend>
          <p><label for="email"   >${_("Email")}   </label><input type="text" id="email"    name="email"   /></p>
          <p><label for="username">${_("Username")}</label><input type="text" id="username" name="username"/></p>
          <input class="signup_submit" type="submit" name="submit" value="${_("Sign up")}"/>
          ##<p><label for="user_type_individual"  >${_("Individual")}  </label><input type="radio" id="user_type_individual"   name="user_type" value="individual"   checked='checked'/></p>
          ##<p><label for="user_type_organisation">${_("Organisation")}</label><input type="radio" id="user_type_organisation" name="user_type" value="organisation"                  /></p>
          
        ##</fieldset>
      </form>
    </div>

    <div class="bullets">
      <ul>
        <li><span class="list_bullet_number">1</span>${_("Add _site_name widget to your website. Request news and insight from your community or wider public")}</li>
        <li><span class="list_bullet_number">2</span>${_("Respond directly to _assignments by uploading relevant news and insight")}</li>
        <li><span class="list_bullet_number">3</span>${_("Get relevant content from your audience and participate directly in issues you care about")}</li>
      </ul>
    </div>

    <div class="example_container">
      <div class="examples">
        <div class="yui-g">
          <div class="yui-u first">
            <a href="${h.url(controller='misc', action='widget_details')}">
            <p class="example_title">${_("Trial the widget now")}</p>
            <img class="example_image" src="/images/misc/widget_preview.png" alt="widget preview"/>
            <ul><li>${_("Widget skins available in 2 colours.")}</li><li>${_("Size customised to fit your website.")}</li></ul>
            ##<img class="view_widget_link" src="/images/misc/view_widget_detail_button.png" alt="view widget in detail"/>
            <strong>${_("Read more!")}</strong>
            </a>
          </div>
          <div class="yui-u">
            <a href="${h.url(controller="misc", action="get_mobile")}">
            <p class="example_title">${_("Trial the mobile app now")}</p>
            <img class="example_image" src="/images/misc/mobile_preview.png" alt="mobile preview"/>
            ##<strong></strong>
            ##Get the civicboom mobile application now
            ${_("Participate in the news agenda directly from you mobile phone.")}
            <strong>${_("Read more!")}</strong>
            ##respond directly from mobile phone with video, text, images. Get footage. Get published.
            </a>
            <br/><br/>
            <div class="tooltip tooltip_special_qrcode">
				${_("Download the Android app now")}
				<span>${_("Scan the QR code below with your Android mobile phone<br/>(or simply search for Civicboom on your mobile phone's marketplace)")|n}
				<img src="/images/misc/android_civicboom_QR.png" alt="market://search?q=pname:com.civicboom.mobileapp"/></span>
			</div>
            ##<strong>Mobile application launching Spring 2010:</strong> Send out news alerts and call-to-action requests; respond directly from mobile phone with video, text, images. Get footage. Get published.
          </div>
        </div>
      </div>
    </div>

  
    <div class="clearboth_hack"></div>

    <div class="affiliates">
      ##<p style="font-weight: bold;">These organisations are using ${_("_site_name")}. Join them by signing up.</p>
      <div>
        ##<a href="http://www.swns.com/"            ><img class="affiliate_icon" alt="South West News Service"   src="http://www.swns.com/images/swns.png"                                           style="max-width: 180px; padding-top: 1em;"/></a>
        ##<a href="http://www.hackneycitizen.co.uk/"><img class="affiliate_icon" alt="Hackney Citizen"           src="http://www.hackneycitizen.co.uk/wp-content/themes/mimbo2.2/images/logo.gif"/></a>
        ##<a href="http://www.sendmoneyhome.org/"   ><img class="affiliate_icon" alt="Sendmoneyhome.org"         src="http://www.sendmoneyhome.org/images/SMH-LOGO.gif"                          /></a>
        ##<a href="http://www.maidstone.gov.uk/"    ><img class="affiliate_icon" alt="Maidstone Borough Council" src="http://www.maidstone.gov.uk/templates/default/css/system/img/mbcLogo.png"  /></a>
        ##<a href="http://www.adhocfilms.com/"      ><img class="affiliate_icon" alt="Ad Hoc Films"              src="http://www.adhocfilms.com/images/adhoclogo_large.png"                      /></a>
        ##<a href="http://www.50in50.co.uk/"        ><img class="affiliate_icon" alt="50in50"                    src="/images/affiliate_icons/50in50.png"                                        /></a>
        ##<a href="http://www.peopleunited.org.uk/" ><img class="affiliate_icon" alt="People United"             src="http://www.peopleunited.org.uk/images/top_logo.jpg"                        /></a>
      </div>
    </div>
    
  </div>

</%def>
