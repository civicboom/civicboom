<%inherit file="./widget_base.mako"/>
<%
    size_font       =  9
    size_header     = 24
    size_footer     = 20
    size_action_bar = 13
    size_content    = c.widget['height'] - size_header - size_footer - size_action_bar - 5 #there are 4 * 1px borders
    size_avatar     = 20
  
    
    #if not c.widget['owner']:
    #    c.widget['owner'] = d.get('content',dict()).get('creator')
    #if not c.widget['owner']:
    #    c.widget['owner'] = d.get('member')
    #if not c.widget['owner']:
    #    from civicboom.lib.database.get_cached import get_member
    #    owner_obj = get_member(c.id)
    #    if owner_obj:
    #        c.widget['owner'] = owner_obj.to_dict()
    if not isinstance(c.widget['owner'], dict):
        c.widget['owner'] = dict(avatar_url='', username='', name='')
    
    owner = c.widget['owner']
    title = c.widget['title']
    
    
%>
<div class="widget_border" style="border: 1px solid #${c.widget['color_border']}; font-size:${size_font}px; color:#${c.widget['color_font']};">

    ##----------------------------------------
    ## Header
    ##----------------------------------------
    <div class="widget_header" style="height:${size_header}px; background-color:#${c.widget['color_header']};">
        <div class="padding">
        <table><tr>
            <td>
                <a href="${h.url('member', id=owner['username'], subdomain='')}" target="_blank" title="${_('%s on _site_name') % owner['name'] or owner['username']}">
                    <img src="${owner['avatar_url']}" alt="${owner['username']}" style="height:${size_avatar}px;"/>
                </a>
            </td>
            <td class="title">	
                <a href="${h.url('member', id=owner['username'], subdomain='')}" target="_blank" title="${_('%s on _site_name') % owner['name'] or owner['username']}">
                    % if title:
                        ${title}
                    % else:
                        ${owner['name']}
                        ##insight: Share your news and opinion
                    % endif
                </a>
            </td>
        </tr></table>
        </div>
    </div>
    
    ##----------------------------------------
    ## Action Bar
    ##----------------------------------------
    
	<!--action_bar-->
    <div class="action_bar" style="height:${size_action_bar}px; background-color:#${c.widget['color_action_bar']}; border: 1px solid #${c.widget['color_border']}; border-left: none; border-right: none; ">
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
            <div class="padding">
        % if c.logged_in_persona:
            <a href="${h.url(controller='profile', action='index')}" target="_blank">
                ${c.logged_in_persona.username}
                <img src="${c.logged_in_persona.avatar_url}" style="max-height:1em;" onerror='this.onerror=null;this.src="/images/default_avatar.png"'/>
            </a>
        % else:
            <a href="${h.url('member_action', id=owner['username'], action='follow', subdomain='')}" target="_blank">
                ${_("Signup Signin")}
                ##to <span class="icon icon_boom" title="${_('_site_name')}"></span>
                ##<img src="/images/logo.png" alt="${_('_site_name')}" style="max-height:1.2em; vertical-align: middle;"/>
            </a>
        % endif
            </div>
        </div>
        ##<div class="clearboth_hack"></div>
    </div>
	<!--end action_bar-->

    ##----------------------------------------
    ## Content (Main) (scrollable vertically)
    ##----------------------------------------
    
    <div class="widget_content" style="height: ${size_content}px; background-color:#${c.widget['color_content']};">
        <div class="padding">
        ${next.body()}
        </div>
    </div>
    
    ##----------------------------------------
    ## Footer
    ##----------------------------------------
    <div class="widget_footer" style="height:${size_footer}px; background-color:#${c.widget['color_header']}; border-top: 1px solid #${c.widget['color_border']}">
        <div class="padding">
            <a class="icon icon_boom"      title="${_('Powered by _site_name')}" target="_blank" href="${h.url('/', subdomain='')}" style="float:right;"><span>${_('_site_name')}</span></a>
            <a class="icon icon_mobile"    title="${_('Mobile reporting')}"      target="_blank" href="${h.url(controller='misc', action='about', id='mobile', subdomain='')}"><span>Mobile</span></a>
            <a class="icon icon_widget"    title="${_('Embed this widget')}"                     href="${h.url(controller='misc', action='get_widget')}"><span>Embed</span></a>
            <a class="icon icon_rss"       title="${_('RSS')}"                   target="_blank" href="${h.url('member', id=owner['username'], format='rss', subdomain='')}"><span>RSS</span></a>
        </div>
    </div>
</div>