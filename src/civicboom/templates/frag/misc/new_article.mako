<%inherit file="/frag/common/frag.mako"/>

<%def name="body()">
    <%
        organisations = {
            # request_id, display name
            '25': 'Kent Online',
            '100'  : 'Gradvine',
        }
    %>
    <div class="frag_col">
        <h1>Excellent, you want to post a story!</h1>
        <h2>Is this story...</h2>
        <h2>...in response to a request?</h2>
            <a href="${h.url(controller='misc', action='featured')}" class="button" onclick="cb_frag($(this), '${h.url(controller='misc', action='featured', format='frag')}'); return false;">Click Here</a>
        <h2>...for an organisation to look at?</h2>
            % for org in organisations:
                ${h.secure_link(
                    h.args_to_tuple('new_content', parent_id=org) ,
                    value           = _("Share your story with %s") % (organisations[org]) ,
                    value_formatted = h.literal("<span class='button'>%s</span>") % _('Share your story with %s') % (organisations[org]) ,
                    json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , 
                )}<br />
            % endfor
        <h2>...a new story you want to post?</h2>
            ${h.secure_link(h.url('new_content', target_type='article'   ), _("Click here") , css_class="button")}
    </div>
</%def>