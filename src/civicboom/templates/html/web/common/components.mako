<%!
    from webhelpers.html import HTML, literal
%>

<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

<%def name="tabs(tab_id, titles, tab_contents, *args, **kwargs)">
    ## JQuery ui tabs - http://jqueryui.com/demos/tabs/
    <div class="event_load jqui_tabs" id="${tab_id}">
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
</%def>

##------------------------------------------------------------------------------
## Guidance (formerly advert)
##------------------------------------------------------------------------------
<%def name="guidance(contents, ad_class=None, int=None, heading=None, config_key=None, disable_link=1)">
    % if config_key: ## and config_key in self.advert_list:
    <div class="guidance">
        ## Display advert disable link
        % if disable_link:
            ${guidance_disable_link(config_key)}
        % endif
        ## <a class="icon16 i_close"></a>
        ## Display content with href if supplied
    	% if heading:
    	    <h1>${heading}</h1>
    	% endif
    	% if int:
    	    <p class="int">${int}.</p>
    	% endif
    	% for item in contents:
    	   <div style="padding: 3px;"></div>
            <%
                content_html = ''
                if item.get('title'):
                    content_html += HTML.p(item['title'], class_="guidance_title")
                if item.get('content_text'):
                    content_html += HTML.p(item['content_text'], class_="guidance_content")
                if item.get('content_list'):
                    content_list = ''
                    for li in item['content_list']:
                        content_list += HTML.li('- ' + li)
                    content_html += HTML.ul(content_list)
                # if item.get('prompt'):
                #     content_html += HTML.br() + HTML.i(_('Click here!'))
                _content_html = HTML.p(content_html, class_="content "+item.get('guidance_class', ''))
            %>
            % if item.get('secure_href'):
                ${h.secure_link(item['secure_href'], item['title'], value_formatted = _content_html)}
            % elif item.get('popup_href'):
                ${popup.link(item['popup_href'], title=item.get('title'))}
            % else:
        	    % if item.get('href'):
                    <a href="${item['href']}">
        	    % endif
        		${content_html | n}
        	    % if item.get('href'):
                    </a>
        	    % endif
            % endif
    	% endfor

        <div class="separator" style="clear: both;"></div>
    </div>
    % endif
</%def>

##------------------------------------------------------------------------------
## Advert disable link
##------------------------------------------------------------------------------

## Used for setting user settings to not display this chunk again
<%def name="guidance_disable_link(config_key)">
    <div class="mo-help">
	${h.form(h.args_to_tuple(controller='settings', id=c.logged_in_user.username, action='update', format='redirect'), method='PUT', json_form_complete_actions="current_element.parent().parent().toggle(500, function(){current_element.parent().parent().remove();});")}
	    ##${_("Don't show me this again")}
	    ##<input type='checkbox' name='${config_key}' value='True' onclick="var form = $(this).closest('form'); form.submit(); form.parent().toggle(500, function(){form.parent().remove();})" />
	    ##<input class='hide_if_js' type='submit' name='submit' value='hide'/>
	    <input type='hidden' name='${config_key}' value='True'/>
	    <input class='hide_guidance_submit hide_if_nojs' src="/styles/common/icons/close_16.png" type='image' src="/styles/common/icons/close_16.png" name='submit' value='hide'/>
	    <div class="mo-help-l">
		${_("Click here to permanently hide this")}
	    </div>
	</form>
    </div>
</%def>
