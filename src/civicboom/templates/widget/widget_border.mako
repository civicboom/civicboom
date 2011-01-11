<%inherit file="./widget_base.mako"/>

<%namespace name="member" file="/web/common/member.mako"/>

<%! import json %>

<%

# Height calculations
size_header        = 55
size_footer        = 60
size_action_bar    = 18
size_flash_message = 0
size_content       = 0

if c.result.get('message'):
	size_flash_message = 30;
if c.widget_height:
	size_content       = int(c.widget_height) - (size_header + size_footer + size_action_bar + size_flash_message) - 5 #borders mount up the 13 is the number of pixels of all the borders combined

c.widget_height_content = size_content - 8 #Used for the QR Code to ensure correct size (the -8 is a hack because the padding is gets in the way)
%>

##------------------------------------------------------------------------------
## Border
##------------------------------------------------------------------------------

<div class="widget_border">

	<% id = c.widget_owner.username %>

    ##----------------------------------------
    ## Header
    ##----------------------------------------
    
	<!--widget_header-->
    <div class="widget_header" style="height:${size_header}px;"><div class="widget_header_footer">
		## Floating about icon
		<a class="tooltip_icon" style="float: right;" href="${h.url_from_widget(controller='widget',action='about')}" title="${_('What is this?')}"></a>
		## Tables just work, CSS layouts are ****ing anoying ... 
		<table><tr>
			<td>${member.avatar(c.widget_owner.to_dict(), new_window=True)}</td>
			<td class="title">	
				<a href="${h.url('member', id=id)}" target="_blank">
				% if c.widget_title:
					${c.widget_title}
				% else:
					${c.widget_owner.name}
					##insight: Share your news and opinion
				% endif
				</a>
			</td>
        </tr></table>
    </div></div>
	<!--end widget_header-->
    
    ##----------------------------------------
    ## Action Bar
    ##----------------------------------------
    
	<!--action_bar-->
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
          % if c.logged_in_persona:
              <a href="${h.url(controller='profile', action='index')}" target="_blank">
				${c.logged_in_persona.username}
				<img src="${c.logged_in_persona.avatar_url}" style="max-height:1em;" onerror='this.onerror=null;this.src="/images/default_avatar.png"'/>
              </a>
          % else:
              <a href="${h.url_from_widget(controller='widget', action='signin')}">
				${_("Sign up or Sign in to")}
				<img src="/images/logo.png" alt="${_('_site_name')}" style="max-height:1.2em; vertical-align: middle;"/>
			  </a>
          % endif
          </div>
          <div class="clearboth_hack"></div>
    </div>
	<!--end action_bar-->
    
    ##----------------------------------------
    ## Flash Message
    ##----------------------------------------
    % if c.result['message'] != "":
        <div class="flash_message" style="height: ${size_flash_message}px" class="status_${c.result['status']}">
			<div style="padding: 0.25em;">
				${c.result['message']}
			</div>
		</div>
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
    
	<!--widget_footer-->
    <div class="widget_footer" style="height:${size_footer}px;"><div class="widget_header_footer">
        <div class="powered_by">
            ${_('Powered by')} <br/><a href="/" target="_blank"><img src="/images/logo.png" alt="${_('_site_name')} Logo" style="max-height: 1em;"/><span style="display: none;">${_('_site_name')}</span></a>
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
            <li><a target="_blank" class="icon icon_rss" href="${h.url('member', id=id, format='rss')}" title="${c.widget_owner.username} RSS Feed"><span>RSS</span></a></li>
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
