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
      <li><a href="${h.url(controller='misc'      , action='about'               )}">${_("About")}</a></li>
      <li><a href="${h.url(controller='search'    , action='reporter'            )}">${_("Search _reporters")}</a></li>
      <li><a href="${h.url(controller='assignment', action='view_all_assignments')}">${_("_assignment").capitalize()}</a></li>
    </ul>
  </div>
    
  <div class="unit_b">
    <ul class="header_items">
      % if not c.logged_in_user:
        <li class="last_list_item">
          <a href="${h.url(controller='account', action='signin')}">${_("Sign in or Sign up")}</a>
        </li>
        
      % else:
        <li class="username">${c.logged_in_user.username}</li>
        <li><a href="${h.url(controller='reporter', action='mynews')                               }">${_("Content grab")}</a></li>
        <li><a href="${h.url(controller='reporter', action='profile', id=c.logged_in_user.username)}">${_("Public")}      </a></li>
        <li><a href="${h.url(controller='reporter', action='myhome')                               }">${_("Private")}     </a>
        <%
          num_notifications = 0 #c.logged_in_user.number_of_new_notifications
        %>
        % if num_notifications > 0:
          <span class="notifications">${num_notifications}</span>
          ##${h.format_multiple_prefix(num_notifications, single="Notification")}
        % endif
        </li>
        <li                       ><a href="${h.url(controller='reporter', action='settings')}">${_("Settings")}</a></li>
        <li class="last_list_item"><a href="${h.url(controller='account', action='signout')  }">${_("Sign out")}</a></li>
      % endif
    </ul>
  
  </div>
    
  <div class="clearboth_hack"></div>
</div>
