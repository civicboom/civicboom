<%inherit file="/html/mobile/common/mobile_base.mako"/>


<%namespace name="member_includes"       file="/html/mobile/common/member.mako" />
<%namespace name="content_list_includes" file="/html/mobile/contents/index.mako" />

<%def name="title()"  >${d['content']['title']}</%def>


<%def name="body()">
    <%
        content   = d['content']
        id        = content['id']
        title     = content['title']
        creator   = content['creator']
        media     = content['attachments']
        responses = d['responses']
        actions   = d.get('actions', [])
    %>
    
    <%self:page>
        <%def name="page_attr()">id="content-main-${id}" class="content_page"</%def>
        ${self.swipe_event('#content-main-%s' % id, '#content-info-%s' % id, 'left')}
        <%def name="page_header()">
            ${self.header(link_next="#content-info-%s" % id)}
        </%def>
        <%def name="page_content()">
            <div class="content_title">
                <h1>${title}</h1>
            </div>
            
            ##----Media----
            <div class="top_media media_list">
                <%
                    count = len(media)
                    thumb = content.get('thumbnail_url', None)
                %>
                % if thumb and count > 1:
                    <a href="#content-media-${id}" alt="Content thumbnail">
                        <img src="${thumb}" />
                        <p>See all ${count} media items</p>
                    </a>
                % elif thumb and count:
                    <a href="${media[0]['original_url']}" alt="Content thumbnail"><img src="${thumb}"/></a>
                % endif
            </div>
            
            ##----Content----
            <div class="content_text">
                ${h.literal(h.scan_for_embedable_view_and_autolink(content['content']))}
            </div>
            
            ## content actions
            % if config['development_mode']:
                % if "respond" in actions:
                    ${h.secure_link(
                        h.args_to_tuple('new_content', parent_id=id),
                        value     = h.literal("<button>respond</button>"),
                        rel = "external"
                    )}
                % endif
                
                % if "edit" in actions:
                % endif
                
                % if "delete" in actions:
                    <a href="#confirm_delete" data-rel="dialog" data-transition="fade"><button>delete</button></a>
                % endif
            % endif
        </%def>
    </%self:page>
    
    <%self:page>
        <%def name="page_attr()">id="content-info-${id}" class="content_page"</%def>
        ${self.swipe_event('#content-info-%s' % id, '#content-main-%s' % id, 'right')}
        <%def name="page_header()">
            ${self.header(link_back="#content-main-%s" % id)}
        </%def>
        <%def name="page_content()">
            <div class="content_details">
                ## Creator info
                <ul data-role="listview" data-inset="true">
                    <li data-role="list-divider" role="heading">Creator</li>
                    ${member_includes.member_details_short(creator, li_only=1)}
                </ul>
                
                ## Parent
                <ul data-role="listview" data-inset="true">
                    ${content_list_includes.parent_content(content)}
                </ul>
                
                ## Content info
                <ul data-role="listview" data-inset="true">
                    <li data-role="list-divider" role="heading">${content['type'].capitalize()} information</li>
                    % if content.get('publish_date'):
                        <li><h3>Published:</h3> ${content.get('publish_date')}</li>
                    % endif
                    % if content.get('tags'):
                        <li><h3>Tags:</h3> ${", ".join(content['tags'])}</li>
                    % endif
                    % if content.get('views'):
                        <li><h3>Views:</h3> ${content['views']}</li>
                    % endif
                    % if content.get('boom_count'):
                        <li><h3>Booms:</h3> ${content['boom_count']}</li>
                    % endif
                </ul>
                
                ## Responses
                <ul data-role="listview" data-inset="true">
                    ${content_list_includes.list_contents(responses, "Responses")}
                </ul>
            </div>
        </%def>
    </%self:page>
    

    % if len(media):
    <%self:page>
        <%def name="page_attr()">id="content-media-${id}" class="content_page"</%def>
        ${self.swipe_event('#content-media-%s' % id, '#content-main-%s' % id, 'right')}
        <%def name="page_header()">
            ${self.header(link_back="#content-main-%s" % id)}
        </%def>
        <%def name="page_content()">
            <div class="media_list">
                % for item in media:
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
        </%def>
    </%self:page>
    % endif
    

    <div data-role="page" id="confirm_delete">
        <div data-role="header">
            <h1>Delete posting?</h1>
        </div>
        <div data-role="content">
            ##${parent.flash_message()}
            <h3>${_("Are you sure you want to delete")} "${title}"${_("? The posting will be permanently deleted from _site_name.")}</h3>
            ${h.secure_link(
                h.args_to_tuple('content', id=id, format='redirect'),
                method = "DELETE",
                value           = _("Delete"),
                value_formatted = h.literal("<button data-theme='a'>Yes, delete!</button>"),
                json_form_complete_actions = "",
            )}
            <a href="#" data-rel="back" data-direction="reverse"><button>No, take me back!</button></a>
        </div>
    </div>
</%def>



