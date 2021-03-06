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
        self.attr.frag_data_css_class = 'frag_ignore_url'
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
                ${frag_list.content_list(cb_list, title, creator=True, show_count=False)}
            </%def>
            
            ${featured_list('recent'            )}
        </div>
            
            <div class="frag_col frag_left_col">
                ${frag_list.member_list(d['members']['new_members'], list_names.get('new_members'), show_count=False)}
            </div>
            
            <div class="frag_col frag_right_col">
                ${frag_list.member_list(d['members']['new_groups' ], list_names.get('new_groups' ), show_count=False)}
            </div>

        <div class="frag_col">
            <div style="clear:both;"></div>
            
            ${featured_list('recent_assignments')}
            
            ${featured_list('most_responses'    )}
        </div>
    </div>

</%def>
