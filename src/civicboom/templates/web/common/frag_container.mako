<%inherit file="/web/common/html_base.mako"/>

<%!
    import types
    frag_container_css_class = '' # to be overridden
%>


<%def name="body()">

    ## How To Use: Overriding body methods should be blank - they should set self.attr.frags
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

<%def name="frag_containers(frags='')">
    <%
        if not isinstance(frags, list):
            frags = [frags]
    %>
    <div id='frag_containers'><!--
        <% frag_counter = '' %>
        % for frag in frags:
            --><div id="frag_${frag_counter}" class="frag_container ${self.attr.frag_container_css_class}">
                % if isinstance(frag, types.FunctionType):
                    ${frag()}
                % elif frag:
                    ${frag}
                % endif
            </div><!--    
            <% frag_counter += '_' %>
        % endfor
        -->
    </div>
</%def>

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