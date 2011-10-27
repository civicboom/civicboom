<%inherit file="/html/mobile/common/mobile_base.mako"/>


<%namespace name="member_includes"       file="/html/mobile/common/member.mako"  />
<%namespace name="content_list_includes" file="/html/mobile/contents/index.mako" />
<%namespace name="content_edit_includes" file="/html/mobile/contents/edit.mako"  />

<%def name="title()">${d['content']['title']}</%def>


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
    
    
    ## Content Text ------------------------------------------------------------
    
    <div data-role="page" data-theme="b" id="content-main-${id}" class="content_page">
        
        ${self.swipe_event('#content-main-%s' % id, '#content-info-%s' % id, 'left')}
        
        ${self.header(link_next="#content-info-%s" % id)}
        
        <div data-role="content">
            <div class="content_title">
                <h1>${title}</h1>
            </div>
            
            ## Media thumbnails ------------------------------------------------
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
            
            ## Content ---------------------------------------------------------
            <div class="content_text">
                ${h.literal(h.scan_for_embedable_view_and_autolink(content['content']))}
            </div>
            
            ## Actions ---------------------------------------------------------
            % if "respond" in actions:
                ## AllanC - TODO - require a way of detecting platform type and launching app if required - or at least prompting user to install or use generic
                
                ${h.secure_form(h.url('new_content', parent_id=id), data_ajax=False)}
                <input type="submit" value="${_('Respond')}">
                ${h.end_form()}
            % endif
            
            % if "edit" in actions:
                ## AllanC - TODO - require a way of detecting platform type and launching app if required - or at least prompting user to install or use generic
                <a data-role="button" href="${h.url('edit_content', id=id)}">${_('Edit')}</a>
            % endif
            
            % if "publish" in actions:
                <a data-role="button" href="#confirm_publish" data-rel="dialog" data-transition="fade">${_('Publish')}</a>
            % endif
            
            % if "delete" in actions:
                <a data-role="button" href="#confirm_delete" data-rel="dialog" data-transition="fade">${_('Delete')}</a>
            % endif

        </div>
        
        ${self.footer()}
    </div>
    
    
    ## Details & responses -----------------------------------------------------
    
    <div data-role="page" data-theme="b" id="content-info-${id}" class="content_page">
        
        ${self.swipe_event('#content-info-%s' % id, '#content-main-%s' % id, 'right')}
        
        ${self.header(link_back="#content-main-%s" % id)}
        
        <div data-role="content">
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
        </div>
        
        ${self.footer()}
    </div>
    

    ## Media -------------------------------------------------------------------

    % if len(media):
    <div data-role="page" data-theme="b" id="content-media-${id}" class="content_page">
        
        ${self.swipe_event('#content-media-%s' % id, '#content-main-%s' % id, 'right')}

        ${self.header(link_back="#content-main-%s" % id)}

        <div data-role="content">
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
        </div>
        
        ${self.footer()}
    </div>
    % endif
    

    ${content_edit_includes.confirm_dialogs(content)}
    
</%def>



