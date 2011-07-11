<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />

## page structure defs
<%def name="body()">
    <%
        self.content = d['content']
        self.id = self.content['id']
        self.title = self.content['title']
    %>
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="content-main-${self.id}" class="content_page">
        <div data-role="header" data-position="inline">
            <h1>${self.title}</h1>
            <a href="#content-info-${self.id}" alt="more" class="ui-btn-right" data-role="button" data-icon="arrow-r" data-iconpos="right">More</a>
        </div>
        ${content_main(self.content)}
    </div>
    
    <div data-role="page" data-title="${page_title()} - info" data-theme="b" id="content-info-${self.content['id']}" class="content_page">
        <div data-role="header" data-position="inline">
            <a href="#content-main-${self.id}" data-role="button" data-icon="arrow-l" data-direction="reverse">Back</a>
            <h1>${self.title} - info</h1>
        </div>
        ${content_info(d)}
    </div>
</%def>

<%def name="page_title()">
    ${_("_site_name Mobile - %s") % d['content']['title']}
</%def>

<%def name="content_main(content)">
    % if content:
        <div data-role="content">
            ##----Media----
            <div class="top_media">
                % for media in content['attachments']:
                    % if media['type'] == "image":
                        <img src="${media['media_url']}" alt="${media['caption']}" />
                    % endif
                % endfor
            </div>
            
            ##----Content----
            <div class="content_text">
                ${h.literal(h.scan_for_embedable_view_and_autolink(content['content']))}
            </div>
            
            ##----Details----
            % if hasattr(content,'views'):
                <p>views: ${content['views']}</p>
            % endif
        </div>
    % endif
</%def>

<%def name="content_info(data)">
    % if data:
    <%
        content = data['content']
        creator = content['creator']
    %>
        <div data-role="content">
            <div class="content_details">
                <ul data-role="listview">
                    ${member_includes.member_details_short(creator, li_only=1)}
                </ul>
            </div>
        </div>
    % endif
</%def>
