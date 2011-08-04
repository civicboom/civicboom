<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes" file="/html/mobile/common/lists.mako" />

## page structure defs
<%def name="body()">
    <%
        self.content = d['content']
        self.id = self.content['id']
        self.title = self.content['title']
        self.creator = self.content['creator']
        self.media = self.content['attachments']
        self.responses = d['responses']
    %>
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="content-main-${self.id}" class="content_page">
        <div data-role="header" data-position="inline">
            <h1>${self.title}</h1>
            <a href="#content-info-${self.id}" alt="more" class="ui-btn-right" data-role="button" data-icon="arrow-r" data-iconpos="right">More</a>
        </div>
        ${content_main()}
    </div>
    
    <div data-role="page" data-title="${page_title()} - info" data-theme="b" id="content-info-${self.content['id']}" class="content_page">
        <div data-role="header" data-position="inline">
            <a href="#content-main-${self.id}" data-role="button" data-icon="arrow-l" data-direction="reverse">Back</a>
            <h1>${self.title} - info</h1>
        </div>
        ${content_info()}
    </div>
    
    <div data-role="page" data-title="${page_title()} - media" data-theme="b" id="content-media-${self.content['id']}" class="content_page">
        <div data-role="header" data-position="inline">
            <a href="#content-main-${self.id}" data-role="button" data-icon="arrow-l" data-direction="reverse">Back</a>
            <h1>${self.title} - media</h1>
        </div>
        ${content_media()}
    </div>
</%def>

<%def name="page_title()">
    ${_("_site_name Mobile - %s") % d['content']['title']}
</%def>

<%def name="content_main()">
    <div data-role="content">
        ##----Media----
        <div class="top_media">
            <%
                count = len(self.media)
                thumb = None
                for item in self.media:
                    thumb = item['thumbnail_url'] if item['type'] in ["image", "video"] else None
                thumb = "/images/misc/shareicons/audio_icon.png" if not thumb else None
            %>
            % if count > 1:
                <a href="#content-media-${self.id}" alt="more"><img src="${thumb}" /></a>
            % elif count:
                <a href="${self.media[0]['original_url']}"><img src="${thumb}" /></a>
            % endif
        </div>
        
        ##----Content----
        <div class="content_text">
            ${h.literal(h.scan_for_embedable_view_and_autolink(self.content['content']))}
        </div>
        
        ##----Details----
        % if hasattr(self.content,'views'):
            <p>views: ${self.content['views']}</p>
        % endif
    </div>
</%def>

<%def name="content_info()">
    <div data-role="content">
        <div class="content_details">
                ## Creator info
                <ul data-role="listview" data-inset="true">
                    <li data-role="list-divider" role="heading">Creator</li>
                    ${member_includes.member_details_short(self.creator, li_only=1)}
                </ul>
                
                ## Parent
                <ul data-role="listview" data-inset="true">
                    ${list_includes.parent_content(self.content)}
                </ul>

                ## Content info
                <ul data-role="listview" data-inset="true">
                    <li data-role="list-divider" role="heading">${self.content['type'].capitalize()} information</li>
                    <li><h3>Published:</h3> ${self.content['publish_date']}</li>
                    <li><h3>Views:</h3> ${self.content['views']}</li>
                    <li><h3>Booms:</h3> ${self.content['boom_count']}</li>
                </ul>
                
                ## Responses
                <ul data-role="listview" data-inset="true">
                    ${list_includes.list_contents(self.responses, "Responses")}
                </ul>
            </ul>
        </div>
    </div>
</%def>

<%def name="content_media()">
    % if len(self.media):
        <div data-role="content">
            <div class="media_list">
                % for item in self.media:
                    <div class="media_item">
                        <a href="${item['original_url']}">
                            % if item['type'] == "audio":
                                <img src="/images/misc/shareicons/audio_icon.png" />
                            % else:
                                <img src="${item['thumbnail_url']}" />
                            % endif
                        </a>
                        <p class="media_item_data">
                            % if item['caption']:
                                ${item['caption']}
                            % endif
                            <br />
                            % if item['credit']:
                                Credited to ${item['credit']}
                            % endif
                        </p>
                    </div>
                % endfor
            </div>
        </div>
    % endif
</%def>
