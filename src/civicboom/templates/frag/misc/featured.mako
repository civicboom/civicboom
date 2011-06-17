<%inherit file="/frag/common/frag.mako"/>
<%! import datetime %>

<%namespace name="frag_list"    file="/frag/common/frag_lists.mako" />

##------------------------------------------------------------------------------
## Vars
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.advert_list = [] # List of advert/info box to display (empty by default, populated below)
        self.attr.title = _('Featured Content')
        
        # Adverts/info boxs
        # Logic for mini advert/info fragments from user prefs- used in the same way as the action_list - the logic is here, the display is in the template
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
            sponsored_assignment    = _('Top _request'),
            sponsored_responded     = _('Most responded'),
            
            top_viewed_assignments  = _('Top _requests'),
            most_responses          = _('What people are getting involved in'),
            near_me                 = _('Near me'),
            recent_assignments      = _('Recent _requests'),
            recent                  = _('Just happened'),
        )
    %>
    
    ${advert(content="Report your news from your Android mobile!", href=h.url(controller="misc", action="about", id="mobile"), icon="mobile", config_key="advert_profile_mobile")}
    ${advert(content="Are you an organisation, journalist, blogger or in PR? GET STARTED HERE", href=h.url("new_group"), icon="group", config_key="advert_profile_group")}
    <span style="clear: both; display: block;"></span>
    <div class="frag_top_row">        
        ## --- adverts --- ##
        <div class="frag_col">
            % for (title, cb_list) in d['sponsored'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_list.sponsored_list(cb_list, title)}
            % endfor
            
            % for (title, cb_list) in d['featured'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_list.content_list(cb_list, title)}
            % endfor
        </div>
    </div>

</%def>

##------------------------------------------------------------------------------
## Advert
##------------------------------------------------------------------------------
<%def name="advert(content, href=None, icon=None, config_key=None, color=None)">
    % if config_key and config_key in self.advert_list:
    <div class="advert">
	##% if icon:
	##    <a class="icon16 i_${icon} icon"></a>
	##% endif
	% if color:
            <div class="box" style="background-color: ${color};">
        % else:
            <div class="box">
        % endif
	    ## Display content with href if supplied
	    % if href:
		<a href="${href}"><span class="content">${content}</span></a>
	    % else:
		<span class="content">${content}</span>
	    % endif
	    ## Display advert disable link
	    ${advert_disable_link(config_key)}
	    ## <a class="icon16 i_close"></a>
	</div>
    </div>
    % endif
</%def>
    
##------------------------------------------------------------------------------
## Advert disable link
##------------------------------------------------------------------------------

## Used for setting user settings to not display this chunk again
<%def name="advert_disable_link(config_key)">
    ${h.form(h.args_to_tuple(controller='settings', id=c.logged_in_user.username, action='update', format='redirect'), method='PUT', json_form_complete_actions="current_element.parent().parent().toggle(500, function(){current_element.parent().parent().remove();});")}
        ##${_("Don't show me this again")}
        ##<input type='checkbox' name='${config_key}' value='True' onclick="var form = $(this).closest('form'); form.submit(); form.parent().toggle(500, function(){form.parent().remove();})" />
        ##<input class='hide_if_js' type='submit' name='submit' value='hide'/>
        <input type='hidden' name='${config_key}' value='True'/>
        <input class='hide_advert_submit' type='submit' name='submit' value='hide'/>
    </form>
</%def>