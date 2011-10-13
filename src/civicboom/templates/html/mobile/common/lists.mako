<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="body()">
    <div data-role="page" data-theme="b" id="${next.list_id()} class="${next.list_class()}">
        
        ## Content -------------------------------------------------------------
        <div data-role="content">
            ${next.list_content()}
        </div>
        
        ## Footer --------------------------------------------------------------
        <div data-role="footer" data-position="fixed" data-fullscreen="true">
            <%
                import copy
                
                args, kwargs = c.web_params_to_kwargs
                kwargs = copy.copy(kwargs)
                if 'format' in kwargs:
                    del kwargs['format']
                list   = d['list']
                offset = list['offset']
                limit  = list['limit']
                count  = list['count']
                items  = len(list['items'])
            %>
            % if offset > 0 or offset + items < count:
                <div data-role="navbar" class="ui-navbar">
                    <ul>
                    % if offset > 0:
                        <li>
                            <% kwargs['offset'] = offset - limit %>
                            <a href="${h.url('current', format='html', **kwargs)}" class="prev" data-direction="reverse">${_("Previous")}</a>
                        </li>
                    % endif
                    % if offset + items < count:
                        <li>
                            <% kwargs['offset'] = offset + limit %>
                            <a href="${h.url('current', format='html', **kwargs)}" class="next">${_("Next")}</a>
                        </li>
                    % endif
                    </ul>
                </div>
            % endif
        </div>
        
    </div>
</%def>





<%def name="search_form()">
    <div data-role="collapsible" data-collapsed="true" class="search_form">
        <h3>Search</h3>
        <p>
            <form action="${url(controller='misc', action='search_redirector')}" data-ajax="false">
                <input type="search" name="term" placeholder="${_("Find _assignments, _articles and _members")}">
                <select name="type" data-theme="b">
                    <option value="All">All content</option>
                    <option value="${_("_Assignments")}">${_("_Assignments")}</option>
                    <option value="${_("_Articles")}">${_("_Articles")}</option>
                    <option value="${_("_Users / _Groups")}">${_("_Users / _Groups")}</option>
                </select>
                <input type="submit" value="${_("Search")}">
            </form>
        </p>
    </div>
</%def>


##--------------------------------------------------------------------------------------------------------------------------------------------------



##------------------------------------------------------------------------------
## Generate li elements for a list
##------------------------------------------------------------------------------
<%def name="generate_list(list, render_item_func, title=None, more=True)">

    % if render_item_func and list.get('count') and list['count']:
        <ul data-role="listview" data-inset="true" data-split-icon="delete" data-split-theme="d">
            % if title:
                <li data-role="list-divider" role="heading">
                    ${title.capitalize()} <span class="ui-li-count">${list['count']}</span>
                </li>
            % endif
            % for item in list['items']:
                ${render_item_func(item)}
            % endfor
            % if more and list.get('count') > list.get('limit'):
                <li>
                    <a href="${more_link(list)}">
                        % if title:
                            ${_('See all %s %s' % (list.get('count'), title.lower()))}
                        % else:
                            ${_('more')}
                        % endif
                    </a>
                </li>
            % endif
        </ul>
    % endif
    
    <%def name="more_link(list)">
        <%
            href = None
            count = list.get('count')
            limit = list.get('limit')
        
            if not href and isinstance(list, dict) and list.get('kwargs'):
                href_args   = [list.get('type')] 
                href_kwargs = list.get('kwargs')
            
            if href_args or href_kwargs:
                href_kwargs['private'] = True
                href      = h.url(*href_args, **href_kwargs)
        %>
        ${href}
    </%def>
</%def>
