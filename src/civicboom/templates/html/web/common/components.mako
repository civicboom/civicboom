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
<%def name="advert(contents, ad_class=None, int=None, heading=None, config_key=None)">
    % if config_key: ## and config_key in self.advert_list:
    <div class="advert">
        ## Display advert disable link
        ${advert_disable_link(config_key)}
        ## <a class="icon16 i_close"></a>
        ## Display content with href if supplied
	<% pad = 0 %>
	% if heading:
	    <h1>${heading}</h1>
	% endif
	% if int:
	    <p class="int">${int}.</p>
	% endif
	% for item in contents:
	    % if pad:
		<div style="padding: 1em;"></div>
	    % endif
	    % if item.get('href'):
		<a href="${item['href']}">
	    % endif
	    % if item.get('advert_class'):
		<div class="content ${item['advert_class']}">
	    % else:
		<div class="content">
	    % endif
		% if item.get('title'):
		    <p class="advert_title">${item['title']}</p>
		% endif
		% if item.get('content_text'):
		    <p class="advert_content">${item['content_text']}</p>
		% endif
		% if item.get('content_list'):
		    <ul>
			% for li in item['content_list']:
			    <li>- ${li}</li>
			% endfor
		    </ul>
		% endif
		% if item.get('prompt'):
		    ## <br /><i>Click here!</i>
		% endif
	    </div>
	    % if item.get('href'):
		</a>
	    % endif
	    <% pad = 1 %>
	% endfor

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
	${h.form(h.args_to_tuple(controller='settings', id=c.logged_in_user.username, action='update', format='redirect'), method='PUT', json_form_complete_actions="current_element.parent().parent().toggle(500, function(){current_element.parent().parent().remove();});")}
	    ##${_("Don't show me this again")}
	    ##<input type='checkbox' name='${config_key}' value='True' onclick="var form = $(this).closest('form'); form.submit(); form.parent().toggle(500, function(){form.parent().remove();})" />
	    ##<input class='hide_if_js' type='submit' name='submit' value='hide'/>
	    <input type='hidden' name='${config_key}' value='True'/>
	    <input class='hide_advert_submit' src="/styles/common/icons/close_16.png" type='image' src="/styles/common/icons/close_16.png" name='submit' value='hide'/>
	    <div class="mo-help-l">
		Click here to permanently hide this
	    </div>
	</form>
    </div>
</%def>