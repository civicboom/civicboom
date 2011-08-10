<%inherit file="/frag/common/frag.mako"/>
<%! import datetime %>

<%namespace name="frag_list"    file="/frag/common/frag_lists.mako" />
<%namespace name="components"   file="/html/web/common/components.mako"  />

##------------------------------------------------------------------------------
## Vars
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.advert_list = [] # List of advert/info box to display (empty by default, populated below)
        self.attr.title = _('Featured Content')
    %>
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

    <%
        list_names = dict(
            sponsored_responded     = _('Most responses'),
            sponsored_assignment    = _('Top _assignment'),
            
            top_viewed_assignments  = _('Top _assignments'),
            most_responses          = _('What people are getting involved in'),
            near_me                 = _('Near me'),
            recent_assignments      = _('Recent _assignments'),
            recent                  = _('Just happened!'),
            
            new_members             = _('Latest Members'),
            new_groups              = _('Latest Hubs'),
        )
    %>
    
    <span style="clear: both; display: block;"></span>
    <div class="frag_top_row">
        <div class="frag_col">
            ## Featured content title
            <div class="frag_list">
                <h1>${_("Featured content")}</h1>
            </div>
            
            <%doc>
            ## AllanC - this was remmed because it was taking up to much space. We wanted to show new users and hubs and needed space.
            % for (title, cb_list) in d['sponsored'].iteritems():
                <% title = list_names.get(title, title) %>
                ${frag_list.sponsored_list(cb_list, title, creator=1)}
            % endfor
            
            <table width="100%" style="margin-top: 1em;"><tr>
            % for (title, cb_list) in d['members'].iteritems():
                <% title = list_names.get(title, title) %>
                <td style="vertical-align: top;">${frag_list.member_list(cb_list, title)}</td>
            % endfor
            </tr></table>
            </%doc>

            <%def name="featured_list(title)">
                <%
                    cb_list = d['featured'][title]
                    title   = list_names.get(title,title)
                %>
                ${frag_list.content_list(cb_list, title, creator=1)}
            </%def>
            
            ${featured_list('recent'            )}
            
            
            <div style="clear:both; margin-top   : 1.4em;"></div>
            <div style="float:left;  width:48%;">${frag_list.member_list(d['members']['new_members'], list_names.get('new_members'))}</div>
            <div style="float:right; width:48%;">${frag_list.member_list(d['members']['new_groups' ], list_names.get('new_groups' ))}</div>
            <div style="clear:both; margin-bottom: 0em;"></div>
            
            ${featured_list('recent_assignments')}
            ${featured_list('most_responses'    )}
            
        </div>
        <div style="padding: 0.15em"></div>
    </div>

</%def>
