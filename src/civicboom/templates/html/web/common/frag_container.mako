<%inherit file="/html/web/common/html_base.mako"/>

##------------------------------------------------------------------------------
## Global
##------------------------------------------------------------------------------

<%!
    import types
    #frag_container_css_class = '' # to be overridden
    
    # Each frag can take 2 cols or 1 col
    # 1 col = 250px, 2 cols = 500px
    # this can be overridden by inherheriting templates to customise the size
    frag_col_sizes = []
    frag_col_classes = []
    
%>

<%def name="html_class_additions()">frag_containers</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">

    ## How To Use: Overriding body methods should be blank - they should set self.attr.frags
    ##             the overriding body method can have content, just dont set self.attr.frags
    <%
        frags_assigned_before = None
        if hasattr(self.attr, 'frags'):
            frags_assigned_before = True
    %>
    
    ${next.body()}

    % if frags_assigned_before==None and hasattr(self.attr, 'frags'):
        ${frag_containers(self.attr.frags)}
    % endif

</%def>


##------------------------------------------------------------------------------
## Frag Containers
##------------------------------------------------------------------------------

<%def name="frag_containers(frags='')">
    <%
        if not isinstance(frags, list):
            frags = [frags]
            
        def get_col_size(col_num, default=2):
            try:
                return self.attr.frag_col_sizes[col_num]
            except:
                return default
            
        def get_col_class(col_num, default=''):
            try:
                return (' ' + self.attr.frag_classes[col_num]) if self.attr.frag_classes[col_num] else default
            except:
                return default
    %>
    <div id='frag_containers'><!--
        <% frag_counter = 0 %>
        % for frag in frags:
            <% frag_col_class = get_col_size(frag_counter, 2) %>
            <% frag_col_classes = get_col_class(frag_counter) %>
            --><div id="frag__${frag_counter}" class="frag_container frag_col_${frag_col_class}${frag_col_classes}">
                % if isinstance(frag, types.FunctionType):
                    ${frag()}
                % elif frag:
                    ${frag}
                % endif
            </div><!--    
            <% frag_counter += 1 %>
        % endfor
        -->
    </div>
</%def>


##------------------------------------------------------------------------------
## Old
##------------------------------------------------------------------------------

<%doc>
            ## AllanC - Methods 1 and 2 have the same outcome
            
            ## Method 1: Use SSI to get the fragment
            ##<% frag_url = url('content', id=1, format='frag') %>
            ##${h.frag_div("frag_", frag_url, class_="frag_container")}
            
            ## Method 2: Create the div manually and render from the template

            ## Disscussion
            ## Method 1 relys on a second call to the server, most of the time this will be cached, but it is still a second call
            ## Method 2 The query and formatting to a dictionary have already happened and are avalable, so we can just give them to the template
            
            ## Development notes (marked for removal)
            ##<div id="frag_1" class="frag_container" style="border: 1px dashed red;">
                ##<p>hello all</p>
                ##<a href="${url("content", id=1, format='frag')}" onclick="cb_frag($(this)); return false;">Link of AJAX</a>
            ##</div>

</%doc>