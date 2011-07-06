<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />

## page structure defs
<%def name="body()">
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="content-${d['content']['id']}" class="content_page">
        ${header()}
        ${content()}
    </div>
</%def>

<%def name="page_title()">
    ${_("_site_name Mobile - " + d['content']['title'])}
</%def>

<%def name="header()">
    <div data-role="header" data-position="inline">
        <h1>${d['content']['title']}</h1>
    </div>
</%def>

<%def name="content()">
    <div data-role="content">
        ${creator()}
    
        ##----Content----
        <div class="content_text">
            ${h.literal(h.scan_for_embedable_view_and_autolink(d['content']['content']))}
        </div>
        
        ##----Media----
        % for media in d['content']['attachments']:
            % if media['type'] == "image":
                <a href="${media['original_url']}"><img src="${media['media_url']}" alt="${media['caption']}"/></a>
            % endif
        % endfor
        
        ##----Details----
        % if hasattr(d['content'],'views'):
            <p>views: ${d['content']['views']}</p>
        % endif
    </div>
</%def>

<%def name="creator()">
    ${member_includes.member_details_short(d['content']['creator'])}
</%def>