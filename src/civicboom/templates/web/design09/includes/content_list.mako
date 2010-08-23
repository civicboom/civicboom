
<%namespace name="member_includes" file="member.mako"  />

##------------------------------------------------------------------------------
## Content List (with thumbnails)
##------------------------------------------------------------------------------

<%def name="content_list(results, mode='normal', actions=False, max_images=None)">
    <table>
    % for content in results[:max_images]:
        ##% if not h.isCurrentContent(content):
        ${content_item_row(content, mode=mode, actions=actions)}
        ##% endif
    % endfor
    </table>
    % if max_images != None:
        ${content_list_text(resultss[max_images:])}
    % endif
</%def>



<%def name="content_item_row(content, mode='normal', actions=False)">
    <tr class="content_item_row">
        ##---------------------------
        ## Thumbnail Col
        ##---------------------------
        <td>
            ## Content Link
            ##---------------------------
            <a href="${h.url(controller='content',action='view',id=content.id)}">
            
            ## Thumbnail Status Overlay
            ##---------------------------
            % if mode=='normal':
                <%
                    overlay = None
                    if content.__type__=='syndicate' or content.__type__=='pending':
                        overlay = content.__type__
                    if content.status == 'locked':
                        overlay = 'approved'
                %>
                % if overlay:
                  <span class="thumbnail_overlay thumbnail_overlay_${overlay}">&nbsp;</span>
                % endif

            % endif
            ## Thumbnail image
            ##---------------------------
            <img src="${content.thumbnail_url}" alt="${content.title}" class="content_thumbnail"/>
          </a>
        </td>
        
        ##---------------------------
        ## Title and Content preview + details
        ##---------------------------        
        <td>
            <a href="${h.url(controller='content',action='view',id=content.id)}">
                <p class="content_title">${content.title}</p>
                <p class="content_details">
                    ${content.creation_date.strftime('%b %d, %Y %H:%M %Z')}
                </p>
                <p class="content_preview">${h.truncate(content.content, length=120, indicator='...', whole_word=True)}</p>
            </a>
        </td>
        
        <td>
            ##---------------------------
            ## Creator
            ##---------------------------
            ${member_includes.avatar(content.creator, show_name=True, class_="content_creator_thumbnail")}
            
            ##---------------------------
            ## Other details
            ##---------------------------
            
            ## WARNING!!!! This is performing a full query to get all responses and comments, these should be replaced with derived fields
            ## Ticket raised
            <br>${ungettext("%d response", "%d responses", len(content.responses)) % len(content.responses)}
            <br>${ungettext("%d comment" , "%d comments" , len(content.comments )) % len(content.comments )}
        </td>
        
        ##---------------------------
        ## Action Buttons
        ##---------------------------
        % if actions:
        <td>
            % if content.status == "locked":
              <span class="icon_large icon_locked">Approved and locked</span>
            % else:
              <a class="button_small button_small_style_2" href="${h.url(controller='content',action='edit',id=content.id)}">
                Edit
              </a>
              <a class="button_small button_small_style_2" href="${h.url(controller='content',action='delete',id=content.id)}"
                 onclick="confirm_before_link(this,'${_("Are your sure you want to delete this content?")}'); return false;">
                Delete
              </a>
            %endif
        </td>
        % endif
        
    </tr>
</%def>



##------------------------------------------------------------------------------
## Content List Text
##------------------------------------------------------------------------------

<%def name="content_list_text(results)">
    <ul>
        % for content in results:
        <li>${content_item(content)}</li>
        % endfor
    </ul>
</%def>
<%def name="content_item_li(content)">
<a href="${url(controller='content', action='view', id=content.id)}">${content.title}</a>
</%def>