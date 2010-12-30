<%inherit file="/frag/common/frag.mako"/>

<%!
    share_url        = False
    rss_url          = False
    auto_georss_link = False
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%        
        self.attr.title     = _('Edit')
        self.attr.icon_type = 'edit'
        
        self.attr.frag_data_css_class = 'frag_content_edit'
    %>
</%def>


##------------------------------------------------------------------------------
## Edit Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    edit frag
</%def>