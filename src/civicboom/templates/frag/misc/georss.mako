<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/html/web/common/location.mako" />

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.attr.title     = _('Map')
        self.attr.icon_type = 'map'
        
        self.attr.frag_data_css_class = 'frag_map'
        
        self.attr.share_url = '' #url.current() #format='html'
    %>
</%def>


##------------------------------------------------------------------------------
## Map Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_col fill">
        <%
        try:
            location = [float(n) for n in request.params.get("location").split(",")]
            if len(location) != 3:
                raise ValueError("location needs 3 parts")
        except:
            location = [-1.0, 53.0, 5.0]
        %>
        
        ${loc.minimap(
            width="100%", height="100%",
            lon = location[0],
            lat = location[1],
            zoom = location[2],
            feeds = [
                dict(pin='red', url=request.params.get('feed', '/search/content.rss'), focus=True)
            ],
            controls = True
        )}
    </div>
</%def>
