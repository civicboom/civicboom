<%inherit file="/frag/common/frag.mako"/>

<%!
    title               = 'Help'
    icon_type           = 'help'
    
    share_kwargs        = None
    
    frag_url            = False
    html_url            = False
    rss_url             = False
    ##auto_georss_link    = False

%>

<%def name="body()">
    <div class="frag_col help_frag">
    ${next.body()}
    </div>
</%def>
