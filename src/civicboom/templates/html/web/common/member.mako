<%def name="kwargs_attrs(**kwargs)">
    % for key, value in kwargs.iteritems():
${key}="${value}" 
    % endfor
</%def>

##------------------------------------------------------------------------------
## Member Autocomplete - used? where?
##------------------------------------------------------------------------------

<%def name="autocomplete_member(field_name='member', size='250px')">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
<script>autocomplete_member("${field_name}_name", "${field_name}_comp", "${field_name}");</script>
</%def>

##------------------------------------------------------------------------------
## Member Link
##------------------------------------------------------------------------------
<%def name="member_link(member, js_link_to_frag=True, new_window=False, class_='', qualified=False, **kwargs)">
<%
    if js_link_to_frag:
        class_ = class_ + ' link_new_frag'
        
    if new_window:
        new_window = 'target="_blank"'
    else:
        new_window = ''
%>
<a href="${h.url('member', id=member['username'], qualified=qualified)}" data-frag="${h.url('member', id=member['username'], format='frag')}" title="${member['name']}" class="${class_}" ${new_window} ${kwargs_attrs(**kwargs)}>${member['name']}</a>
</%def>

##------------------------------------------------------------------------------
## Member Avatar - display a member as text/image + link to profile + follow actions
##------------------------------------------------------------------------------

<%def name="avatar(member, class_='', js_link_to_frag=True, new_window=False, img_class='', as_link=True, qualified=False, **kwargs)">
    % if member:
    <%
        # AllanC - WOOOOOW!!! This is REALLY ineffiencet for passing multiple member objects that are not dicts already
        #          Can this be profiled and checked as to how often this occours?
        if hasattr(member,'to_dict'):
            member = member.to_dict()
            

        if js_link_to_frag:
            js_link_to_frag = h.literal(""" onclick="cb_frag($(this), '%s'); return false;" """ % h.url('member', id=member['username'], format='frag'))
        else:
            js_link_to_frag = ''
            
        if new_window:
            new_window = 'target="_blank"'
        else:
            new_window = ''

    %>\
    <%def name="member_link()"><a class="link_new_frag" href="${h.url('member', id=member['username'], qualified=qualified)}" title="${member['name']}" data-frag="${h.url('member', id=member['username'], format='frag')}"></%def>
    ##<a href="${h.url('member', id=member['username'])}" title="${member['name']}" ${js_link_to_frag} ${new_window}></%def>
    ##% if include_name == 'prefix':
    ##  nothing
    ##% endif
    <div class="thumbnail ${class_} event_load">
	% if as_link:
		${member_link()}
	% endif
              <img src="${member['avatar_url']}" alt="${member['username']}" class="img ${img_class}" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
	% if as_link:
		</a>
	% endif
    </div>
    % endif
</%def>

##------------------------------------------------------------------------------
## Member List
##------------------------------------------------------------------------------

<%def name="member_list(members, show_avatar=False, show_name=False, class_=None)">
    <ul class="${class_}">
    % for member in members:
        <li>${avatar(member, show_avatar=show_avatar, show_name=show_name)}</li>
    % endfor
    </ul>
</%def>
