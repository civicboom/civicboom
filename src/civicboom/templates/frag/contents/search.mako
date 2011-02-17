<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/html/web/common/location.mako"/>


<%!
    from civicboom.lib.constants import contents_list_titles
    rss_url = False
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.attr.title     = _('Search')
        self.attr.icon_type = 'search'
        
        self.attr.frag_data_css_class = 'frag_search'
    %>
</%def>


##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_col">
        <form id="form_search" action="${url('contents')}" method="GET"
              onsubmit="cb_frag($(this), '/contents.frag?' + $('#form_search').serialize(), 'frag_col_1'); return false;">
            <fieldset>
				<!--
                <legend>Search</legend>
                <br/>
				-->
                <% args, kwargs = c.web_params_to_kwargs %>
                <label for="term">Text</label><br />
                <input type="text" style="width: 210px" name="term" value="${kwargs.get('term')}"/>
                <br/>
                <label for="list">Type</label><br/>
                % for list, type, name in contents_list_titles:
                    <%
                        checked = ''
                        if kwargs.get('list') == list:
                            checked = 'checked'
                    %>
                    <input type="radio" name="list" value="${list}" ${checked}>${name}<br/>
                % endfor
                <br/>
                <label>Location</label><br />
                ${loc.location_picker(width='210px')}
                <br/>
                <input type="submit" value="Search" class="button"/>
            </fieldset>
        </form>
    </div>
</%def>
