<%inherit file="/html/widget/widget_base.mako"/>
<%

    owner = c.widget['owner']
    title = c.widget['title']

    size_font       =  9
    size_header     = 24
    size_footer     = 20
    if owner and owner.get('push_assignment'):
        size_footer += 16 # Add space for the give news button
    size_action_bar = 13
    size_content    = c.widget['height'] - size_header - size_footer - size_action_bar - 5 #there are 4 * 1px borders
    size_avatar     = 20
    
    self.size_content = size_content
        
%>
<div class="widget_border" style="border: 1px solid #${c.widget['color_border']}; font-size:${size_font}px; color:#${c.widget['color_font']};">

    ##----------------------------------------
    ## Header
    ##----------------------------------------
    <div class="widget_header" style="height:${size_header}px; background-color:#${c.widget['color_header']};">
        <div class="padding">
        <table><tr>
            <%
                owner_name = owner['name']
                owner_url  = h.url(controller='misc', action='titlepage', sub_domain='www')
                if owner['username']:
                    owner_url = h.url('member', id=owner['username'], sub_domain='www')
            %>
            <td>
                <a href="${owner_url}" target="_blank" title="${_('%s on _site_name') % owner_name}">
                    % if owner_name:
                    <img src="${owner['avatar_url']}" alt="${owner_name}"      style="height:${size_avatar}px;" onerror="this.onerror=null;this.src='/images/default/avatar.png'" />
                    % else:
                    <img src="/images/boom128.png"  alt="${_('_site_name')}" style="height:${size_avatar}px;" />
                    % endif
                </a>
            </td>
            <td class="title">	
                <a href="${owner_url}" target="_blank" title="${_('%s on _site_name') % owner_name}">
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
                ${c.logged_in_persona.name or c.logged_in_persona.username}
                <img src="${c.logged_in_persona.avatar_url}" style="max-height:1em;" onerror='this.onerror=null;this.src="/images/default/avatar.png"'/>
            </a>
        % elif owner['username']:
            <a href="${h.url('member_action', id=owner['username'], action='follow', sub_domain='www')}" target="_blank">
                ${_("Sign up/Sign in")}
            </a>
        % else:
            <a href="${h.url(controller='account', action='signin', sub_domain='www')}" target="_blank">
                ${_("Sign up/Sign in")}
                ##to <span class="icon16 i_boom" title="${_('_site_name')}"></span>
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

            % if owner and owner.get('push_assignment'):
            <p><a href="${h.url('new_content', target_type='article', parent_id=owner['push_assignment'], sub_domain="www")}" style="background-color:#${c.widget['color_action_bar']};" class="push_assignment_button">${_("Send us your stories")}</a></p>
            % endif
            
            <div style="float:right;">
            	<a class="icon16 i_help"  title="${_('About _site_name')}"      href="${h.url(controller='misc', action='about')                      }"                ><span>${_('About _site_name')     }</span></a>
            	<a class="icon16 i_boom"  title="${_('Powered by _site_name')}" href="${h.url(controller='misc', action='titlepage', sub_domain='www')}" target="_blank"><span>${_('Powered by _site_name')}</span></a>
            </div>
            <a class="icon16 i_mobile"    title="${_('Mobile reporting')}"   href="${h.url(controller='misc', action='about', id='mobile', sub_domain='www')}" target="_blank"><span>Mobile</span></a>
            ## AllanC - Broken when adding other widget types, will be reenabled later
            ##<a class="icon16 i_widget"    title="${_('Embed this widget')}"  href="${h.url(controller='misc', action='get_widget')                          }"                ><span>Embed </span></a>

            <%
                rss_url = ''
                
                if owner['username']:
                    rss_url = h.url('member', id=owner['username'], format='rss', sub_domain='www')
                    
                elif '/misc' not in h.current_url(): #do not show RSS link for misc pages as they are static
                    # Get current URL deatils - set format to RSS and remove widget variables
                    kwargs = {}
                    if c.web_params_to_kwargs:
                        args, kwargs = c.web_params_to_kwargs
                    # Remove the widget variables from URL
                    for key in [key for key in kwargs if config['setting.widget.var_prefix'] in key]:
                        del kwargs[key]
                    if 'format' in kwargs:
                        del kwargs['format']
                    if 'sub_domain' in kwargs:
                        del kwargs['sub_domain']
                    rss_url = h.url('current', format='rss', sub_domain='www', **kwargs)
                    
                    #rss_url = ''
                    #(args, kwargs)  = h.get_object_from_action_url()
                    #if args and ('member' in args or 'content' in args):
                    #    kwargs['format'] = 'rss'
                    #    rss_url = h.url(*args, **kwargs)
            %>
            % if rss_url:
            <a class="icon16 i_rss"       title="${_('RSS')}"                   target="_blank" href="${rss_url}"><span>RSS</span></a>
            % endif
        </div>
    </div>
</div>
