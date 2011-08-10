<%inherit file="/frag/common/frag_lists.mako"/>

<%!
    rss_url = True
%>


<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs
        creator = True
        if 'creator' in kwargs:
            creator = False
        list_title = 'List'
        if 'list' in kwargs:
            list_title = kwargs['list'].capitalize()
    %>
            
    ## Display first item in content list as 'sponsored'
    ## Temporary -> designed to be replaced by actual sponsored/partner content
    <div class="frag_list">
        <%doc>
        % if len(d['list']['items']):
            <div style="border: 1px solid #ddd;">${parent.sponsored_list(d['list']['items'][0], list_title, show_heading=False)}</div>
            <div style="clear: both; padding: 0.3em;"></div>
            ## Rest of content list
            ${parent.content_list(d['list']['items'][1:], list_title, show_heading=False, paginate=True, creator=creator)}</div>
        % endif
        </%doc>
        
        % if len(d['list']['items']):
            ${parent.content_list(d['list']['items'], list_title, show_heading=False, paginate=True, creator=creator, extra_info=True)}
        % endif
    </div>
</%def>
