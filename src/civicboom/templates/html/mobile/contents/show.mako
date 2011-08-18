<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

<%def name="page_title()">
    ${_(d['content']['title'])}
</%def>

## page structure defs
<%def name="body()">
    <%
        self.content = d['content']
        self.id = self.content['id']
        self.title = self.content['title']
        self.creator = self.content['creator']
        self.media = self.content['attachments']
        self.responses = d['responses']
        self.actions   = d.get('actions', [])
    %>
    <div data-role="page" data-theme="b" id="content-main-${self.id}" class="content_page">
        ${components.header(next_link="#content-info-"+str(self.id))}
        ${content_main()}
    </div>
    
    <div data-role="page" data-theme="b" id="content-info-${self.id}" class="content_page">
        ${components.header(back_link="#content-main-"+str(self.id))}
        ${content_info()}
    </div>
    
    <div data-role="page" data-theme="b" id="content-media-${self.id}" class="content_page">
        ${components.header(back_link="#content-main-"+str(self.id))}
        ${content_media()}
    </div>
</%def>

<%def name="content_main()">
    <div data-role="content">
        <div class="content_title">
            <h1>${self.title}</h1>
        </div>
        
        ##----Media----
        <div class="top_media media_list">
            <%
                count = len(self.media)
                thumb = self.content['thumbnail_url'] if self.content.get('thumbnail_url') else None
            %>
            % if thumb and count > 1:
                <a href="#content-media-${self.id}" alt="Content thumbnail">
                    <img src="${thumb}" />
                    <p>See all ${count} media items</p>
                </a>
            % elif thumb and count:
                <a href="${self.media[0]['original_url']}" alt="Content thumbnail"><img src="${thumb}"/></a>
            % endif
        </div>
        
        ##----Content----
        <div class="content_text">
            ${h.literal(h.scan_for_embedable_view_and_autolink(self.content['content']))}
        </div>
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
                    % if self.content.get('tags'):
                        <li><h3>Tags:</h3> ${", ".join(self.content['tags'])}</li>
                    % endif
                    % if self.content.get('views'):
                        <li><h3>Views:</h3> ${self.content['views']}</li>
                    % endif
                    % if self.content.get('boom_count'):
                        <li><h3>Booms:</h3> ${self.content['boom_count']}</li>
                    % endif
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
