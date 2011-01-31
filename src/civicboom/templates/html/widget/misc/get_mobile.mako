<%inherit file="/html/widget/common/widget_content.mako"/>

<div class="get_mobile">
    <p class="content_title">${_("Android mobile application")}</p>
    <p>${_("Scan the QR code below with your Android phone to get the app now!")}</p>
    <p style="clear:both; font-weight: bold; margin-top: 0.5em;">Alternatively</p>
    <ul>
        <li>${_("Search for _site_name with your Android phone")}</li>
          ##<li>Visit ${c.site_name} at the Android Marketplace <a target="_blank" href="http://www.android.com/market/#app=${c.site_name}">here</a></li>
    </ul>
  
    <div style="display: block; text-align: center;">    
        <a href="/images/misc/mobile_screenshot1.png" target="_blank"><img src="/images/misc/mobile_screenshot1.png" alt="${_('Screenshot of the Mobile App')}" style="max-width: 45%;  margin: 0.25em;"/></a>
        <a href="/images/misc/mobile_screenshot2.png" target="_blank"><img src="/images/misc/mobile_screenshot2.png" alt="${_('Screenshot of the Mobile App')}" style="max-width: 45%;  margin: 0.25em;"/></a>    
        <br/>
        <%
          qr_image = "android_civicboom_QR.png"
          qr_url   = "market://search?q=pname:com.civicboom.mobileapp"
        %>
        <a href="/images/misc/${qr_image}" target="_blank"><img src="/images/misc/${qr_image}" alt="${qr_url}" style="max-width: 100%; max-height:${c.widget_height_content}px;"/></a>
    </div>

</div>