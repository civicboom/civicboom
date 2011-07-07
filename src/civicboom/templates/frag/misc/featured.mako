<%inherit file="/frag/common/frag.mako"/>
<%! import datetime %>

<%namespace name="frag_list"    file="/frag/common/frag_lists.mako" />
<%namespace name="components"   file="/html/web/common/components.mako"  />

##------------------------------------------------------------------------------
## Vars
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.advert_list = [] # List of advert/info box to display (empty by default, populated below)
        self.attr.title = _('Featured Content')
        
        # Adverts/info boxs
        # Logic for mini advert/info fragments from user prefs- used in the same way as the action_list - the logic is here, the display is in the template
        if c.logged_in_user:
            if not c.logged_in_user.config['advert_profile_mobile']:
                self.advert_list.append('advert_profile_mobile')
            if not c.logged_in_user.config['advert_profile_group']:
                self.advert_list.append('advert_profile_group')
    %>
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

    <%
        list_names = dict(
            sponsored_responded     = _('Most responses'),
            sponsored_assignment    = _('Top _assignment'),
            
            top_viewed_assignments  = _('Top _assignments'),
            most_responses          = _('What people are getting involved in'),
            near_me                 = _('Near me'),
            recent_assignments      = _('Recent _assignments'),
            recent                  = _('Just happened'),
        )
    %>
    
    ## Adverts
    % if c.logged_in_user:
        ${components.advert(content="Make news with the Civicboom mobile app!", href=h.url(controller="misc", action="about", id="mobile"), icon="mobile", config_key="advert_profile_mobile")}
        ## ${components.advert(content="Are you an organisation, journalist, blogger or in PR? GET STARTED HERE", href=h.url("new_group"), icon="group", config_key="advert_profile_group")}
    % endif
    
    <span style="clear: both; display: block;"></span>
    <div class="frag_top_row">
        <div class="frag_col">
            ## Featured content title
            <div class="frag_list">
                <h1>Featured content</h1>
            </div>
        
            % for (title, cb_list) in d['sponsored'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_list.sponsored_list(cb_list, title)}
            % endfor
            
            % for (title, cb_list) in d['featured'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_list.content_list(cb_list, title)}
            % endfor
        </div>
        <div style="padding: 0.15em"></div>
    </div>

</%def>