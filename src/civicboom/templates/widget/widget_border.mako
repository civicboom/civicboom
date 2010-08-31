<%inherit file="./widget_base.mako"/>

<%namespace name="member" file="/web/design09/includes/member.mako"/>

<%
	import json

    # Height calculations
    size_header        = 70
    size_footer        = 60
    size_action_bar    = 18
    size_flash_message = 0
    size_content       = 0
    
    if session.has_key('flash_message'):
		size_flash_message = 30;
		try:
			msg = json.loads(session.get('flash_message'))
		except ValueError:
			msg = {"status": "error", "message": session.get('flash_message')}
		msg_status = msg["status"]
		msg_msg = msg["message"]
    if c.widget_height:
		size_content       = int(c.widget_height) - (size_header + size_footer + size_action_bar + size_flash_message) - 5 #borders mount up the 13 is the number of pixels of all the borders combined
    
    c.widget_height_content = size_content - 8 #Used for the QR Code to ensure correct size (the -8 is a hack because the padding is gets in the way)
%>

##------------------------------------------------------------------------------
## Border
##------------------------------------------------------------------------------

<div class="widget_border">

    ##----------------------------------------
    ## Header
    ##----------------------------------------
    
    <div class="widget_header" style="height:${size_header}px;"><div class="widget_header_footer">
    
        <div class="widget_reporter_thumbnail">
            ##<a href="${h.url(controller='reporter', action='profile', id=c.widget_owner.username)}" target="_blank">
            <img src="${c.widget_owner.avatar_url}" />
            ##</a>
            <a class="action button_style_1 inverted" href="${h.url(controller='reporter', action='followReporter', id=c.widget_owner.id)}">Follow</a>
        </div>
        <a class="tooltip_icon" style="float: right;" href="${h.url_from_widget(controller='widget',action='about')}" title="What is this?"></a>
        ##<span class="widget_header_title">
        <a class="widget_header_title" href="${h.url(controller='reporter', action='profile', id=c.widget_owner.username)}" target="_blank">
        ##${reporter_includes.reporter_full(c.widget_owner,class_="widget_reporter_thumbnail")}
        % if c.widget_title:
            ${c.widget_title}
        % else:
            ${c.widget_owner.username}
            ##insight: Share your news and opinion
        % endif
        ##</span>
        </a>
        ##<a class="button button_style_1 inverted" href="${h.url_from_widget(controller='reporter', action='followReporter', id=c.widget_owner.id)}">Follow</a>

        <div class="clearboth_hack"></div>
    </div></div><!--end widget_header-->
    
    ##----------------------------------------
    ## Action Bar
    ##----------------------------------------
    
    <div class="action_bar" style="height:${size_action_bar}px;">
          ##----------------------------------------
          ## Overrideable (normally back)
          ##----------------------------------------
          <div class="action_bar_element" style="float:left;">
              <%def name="widget_actions()">
              </%def>
              ${self.widget_actions()}
          </div>
      
          ##----------------------------------------
          ## Sign in/up
          ##----------------------------------------
          <div class="action_bar_element" style="float:right;">
          % if c.logged_in_user:
              <p>${_("Logged in")} <a href="${h.url_from_widget(controller='reporter', action='myhome')}" target="_blank">
              ${c.logged_in_user.username}
              <img src="${c.logged_in_user.avatar_url}" style="max-height:1em;"/>
              </a></p>
          % else:
              <a href="${h.url_from_widget(controller='widget', action='signin')}">Sign up or Sign in to <img src="/design09/logo.png" alt="${_('_site_name')}" style="max-height:1.2em; vertical-align: middle;"/></a>
          % endif
          </div>
          <div class="clearboth_hack"></div>
    </div>
    
    ##----------------------------------------
    ## Session messages
    ##----------------------------------------
    % if session.has_key('flash_message'):
        <div class="flash_message" style="height: ${size_flash_message}px" class="status_${msg_status}"><div style="padding: 0.25em;">${msg_msg}</div></div>
        <%
          del session['flash_message']
          session.save()
        %>
    % endif
    
    ##----------------------------------------
    ## Content (Main) (scrollable vertically)
    ##----------------------------------------
    
    <div class="widget_main" style="height: ${size_content}px;">    
        ##----------------------------------------
        ## Content (next template)
        ##----------------------------------------    
        ${next.body()}
    </div>
    
    ##----------------------------------------
    ## Footer
    ##----------------------------------------
    
    <div class="widget_footer" style="height:${size_footer}px;"><div class="widget_header_footer">
        <div class="powered_by">
            ${_('Powered by')} <br/><a href="/" target="_blank"><img src="/styles/design09/logo.png" alt="${_('_site_name')} Logo" style="max-height: 1em;"/><span style="display: none;">${_('_site_name')}</span></a>
        </div>
      
      
        <ul>
          <li class="widget_item_popup">
            <a class="icon icon_mobile" href="${h.url_from_widget(controller='widget', action='get_mobile')}">
                ${_('Mobile reporting')}
            </a>
          </li>
          % if c.widget_owner:
          <li class="widget_item_popup">
            <a href="${h.url_from_widget(controller='widget', action='get_widget')}">
                ${_('Embed this widget')}
            </a>
          </li>
          % endif
        </ul>
        
        ##----------------------------------------
        ## Feeds links
        ##----------------------------------------
        
        % if c.widget_owner:
        <ul class="widget_icon_list">
            ##<li><%include file="/design09/gadget/get_gadget_link_button.mako"/></li>
            <li><a target="_blank" class="icon icon_rss" href="${h.url(controller='rss',action='reporter',id=c.widget_owner.username)}" title="${c.widget_owner.username} RSS Feed"><span>RSS</span></a></li>
            ##% if c.widget_owner.twitter_username:
            ##  <li><a target="_blank" class="icon icon_twitter" href="http://twitter.com/${c.widget_owner.twitter_username}" title="${c.widget_owner.username} on twitter"><span>twitter</span></a></li>
            ##% endif
            <li>&nbsp;</li>
        </ul>
        % endif
        
    </div></div><!--end widget_footer-->
    
</div><!--end widget_border-->

##------------------------------------------------------------------------------
## Old Popup reference
##------------------------------------------------------------------------------

<%doc>
## inside       <li class="widget_item_popup">

<%def name="mobile_reporting_popup()">
<div class="popup_content widget_content">
  <p class="content_title">Comming soon!</p>
  <p>Report directly from your mobile phone</p>
</div>
</%def>

<%def name="signup_popup()">
<div class="popup_content widget_content">
  <p class="content_title">Signup to Civicboom</p>
  <p>sign up + auto_follow + alert organisation to widget signup</p>
</div>
</%def>

<%def name="get_widget_popup()">
<div class="popup_content widget_content">
##widget_get_widget.mako
</div>
</%def>
</%doc>
