<%inherit file="/frag/common/frag.mako"/>

<%!
    title               = 'Help'
    icon_type           = 'help'
    
    share_kwargs        = None
    
    frag_url            = False
    html_url            = False
    rss_url             = False
    ##auto_georss_link    = False

    frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
    
    ##frag_data_css_class = 'bridge'
%>

<%def name="body()">
    <div class="frag_col">
    ${next.body()}
    </div>
</%def>
