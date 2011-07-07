<%def name="tabs(tab_id, titles, tab_contents, *args, **kwargs)">
    ## JQuery ui tabs - http://jqueryui.com/demos/tabs/
    <div id="${tab_id}">
        <ul>
            % for (title, i) in zip( titles , [i+1 for i in range(len(titles))]):
            <li><a href="#${tab_id}-${i}">${title}</a></li>
            % endfor
        </ul>
        % for (tab_content, i) in zip( tab_contents , [i+1 for i in range(len(tab_contents))]):
        <div id="${tab_id}-${i}">
            ${tab_content(*args, **kwargs)}
        </div>
        % endfor
    </div>
    <script>
        $(function() {
            $("#${tab_id}").tabs({
                create: function(event, ui) {
                    ##$.modal.update(); ## AllanC - failed attempt at trying to get the ***ing thing to resize
                }
            });
        });
	</script>
</%def>

##------------------------------------------------------------------------------
## Advert
##------------------------------------------------------------------------------
<%def name="advert(title, content, href=None, advert_class='', heading=None, int=None, config_key=None, background=None)">
    % if config_key: ## and config_key in self.advert_list:
    <div class="advert">
        ## Display advert disable link
        ${advert_disable_link(config_key)}
        ## <a class="icon16 i_close"></a>
        ## Display content with href if supplied

	% if heading:
	    <h1>${heading}</h1><div style="clear: both"></div>
	    <div style="clear: both;"></div>
	% endif
	% if int:
	    <span class="int">${int}.</span>
	% endif
	% if href:
	    <a href="${href}">
	% endif
	<div class="content ${advert_class}">
	    <p class="advert_title">${title}</p>
	    <p class="advert_content">${content}</p>
	</div>
	% if href:
	    </a>
	% endif

        <div class="separator" style="clear: both;"></div>
    </div>
    % endif
</%def>

##------------------------------------------------------------------------------
## Advert disable link
##------------------------------------------------------------------------------

## Used for setting user settings to not display this chunk again
<%def name="advert_disable_link(config_key)">
    <div class="mo-help">
	${h.form(h.args_to_tuple(controller='settings', id=c.logged_in_user.username, action='update', format='redirect'), method='PUT', json_form_complete_actions="current_element.parent().toggle(500, function(){current_element.parent().remove();});")}
	    ##${_("Don't show me this again")}
	    ##<input type='checkbox' name='${config_key}' value='True' onclick="var form = $(this).closest('form'); form.submit(); form.parent().toggle(500, function(){form.parent().remove();})" />
	    ##<input class='hide_if_js' type='submit' name='submit' value='hide'/>
	    <input type='hidden' name='${config_key}' value='True'/>
	    <input class='hide_advert_submit' src="/styles/common/icons/close_16.png" type='image' src="/styles/common/icons/close_16.png" name='submit' value='hide'/>
	    <div class="mo-help-l">
		Be aware, by closing this advert it will disappear from your profile <b>forever!</b>
	    </div>
	</form>
    </div>
</%def>