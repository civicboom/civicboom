<%inherit file="/frag/common/frag.mako"/>
<%! import datetime %>

<%namespace name="frag_lists"      file="/frag/common/frag_lists.mako"     />

##------------------------------------------------------------------------------
## Vars
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.attr.title = _('Featured Content')
    %>
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

    <%
        list_names = dict(
            sponsored_assignment    = _('Top _request'),
            sponsored_responded     = _('Most responded'),
            
            top_viewed_assignments  = _('Top _requests'),
            most_responses          = _('What people are getting involved in'),
            near_me                 = _('Near me'),
            recent_assignments      = _('Recent _requests'),
            recent                  = _('Just happened'),
        )
    %>

    <div class="frag_left_col">
        <div class="frag_col">
            % for (title, cb_list) in d['sponsored'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_lists.sponsored_list(cb_list, title)}
            % endfor
            % for (title, cb_list) in d['featured'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_lists.content_list(cb_list, title)}
            % endfor
        </div>
    </div>

    <div class="frag_right_col">
        <div class="frag_col">
            <p>Contribute via your mobile</p>
        </div>
    </div>

</%def>