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
		<!--
        <form id="form_search" action="${url('contents')}" method="GET"
              onsubmit="cb_frag($(this), '/contents.frag?' + $('#form_search').serialize(), 'frag_col_1'); return false;">
			<% args, kwargs = c.web_params_to_kwargs %>
            <fieldset style="border: 1px solid black; padding: 4px;">
                <legend>${_("Basic Search")}</legend>
                <input type="search" style="width: 100%;" name="term" placeholder="Search terms" value="${kwargs.get('term')}"/>
                <br/><input type="submit" style="width: 100%;" value="Search" class="button"/>
            </fieldset>
		</form>

        <p>&nbsp;
		-->
		
		<form id="form_search" action="${url('contents')}" method="GET"
              onsubmit="unplacehold('#form_search'); cb_frag($(this), '/contents.frag?' + $('#form_search').serialize(), 'frag_col_1'); return false;">
            <!--<fieldset style="border: 1px solid black; padding: 4px;">-->
            <fieldset>
                <!--<legend>${_("Advanced search")}</legend>-->

				<p><label>Search for</label><br>
				<select name="list" style="width: 100%;">
                % for list, type, name in contents_list_titles:
                    <% checked = 'selected' if (kwargs.get('list') == list) else '' %>
                    <option value="${list}" ${checked}>${name}</option>
                % endfor
				</select>

				<p><label>Talking about</label><br>
                <input type="search" style="width: 100%;" name="term" placeholder="Enter key words" value="${kwargs.get('term')}"/>

                <p><label>Near to</label>
                ${loc.location_picker(width='213px', height="213px")}

                <p>&nbsp;<br>
				<input type="submit" style="width: 100%;" value="Search" class="button"/>
            </fieldset>
        </form>
    </div>
</%def>
