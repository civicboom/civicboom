<%namespace name="sl" file="/web/design09/includes/secure_link.mako" />

<div id="header">
  <div class="unit_a">
    <h1 class="mainLogo">
      <a href='/'>
        <img src='/styles/design09/logo_beta_overlay.png' alt='beta'                     style="position: absolute; max-width: 20px; margin-left: 120px;"/>
        <img src='/styles/design09/logo.png'              alt='${_("_site_name")}'/>
        <span>${_("_site_name")}</span>
      </a>
    </h1>
    
    <ul class="links_by_title">
      <li><a href='/' class="icon_large icon_home" style="padding: 0em; margin: 0em;"></a></li>
    </ul>
  </div>
    
  <div class="unit_b">
    <ul class="header_items">
      % if not c.logged_in_user:
        <li class='last_list_item'><a href="${url(controller='account', action='signin')}">${_("Sign in or Sign up")}</a></li>
      % else:
        <li><a href="${url(controller='profile', action='view', id=c.logged_in_user.username)}">${c.logged_in_user.name} (${c.logged_in_user.username})</a></li>
        <li><a href="${url(controller='profile', action='index')                             }">${_("Controls")}</a></li>
        <li class='last_list_item'>${sl.secure_link(url(controller='account', action='signout'), _("Sign out"))}</li>
      % endif
    </ul>
  
  </div>
    
  <div class="clearboth_hack"></div>
</div>
