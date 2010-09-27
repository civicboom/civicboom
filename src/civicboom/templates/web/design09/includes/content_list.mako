
<%namespace name="member_includes" file="member.mako"  />

##------------------------------------------------------------------------------
## Content List (with thumbnails)
##------------------------------------------------------------------------------

<%def name="content_list(results, mode='normal', actions=False, max_images=None, class_='content_list')">
    <table class="${class_}">
    % for content in results[:max_images]:
        ##% if not h.isCurrentContent(content):
        % if mode=="normal":
            ${content_item_row(content, actions=actions)}
        % elif mode=="mini":
            ${content_item_row_mini(content)}
        % endif
        ##% endif
    % endfor
    </table>
    % if max_images != None:
        ${content_list_text(resultss[max_images:])}
    % endif
</%def>



<%def name="content_item_row(content, actions=False)">
    <tr>
        ##---------------------------
        ## Thumbnail Col
        ##---------------------------
        <td class="content_thumbnail">
            ## Content Link
            ##---------------------------
            <a href="${h.url('content', id=content['id'])}">
            
            ## Thumbnail Status Overlay
            ##---------------------------
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
            
            ## Thumbnail image
            ##---------------------------
            <img src="${content['thumbnail_url']}" alt="${content['title']}"/>
          </a>
        </td>
        
        ##---------------------------
        ## Title and Content preview + details
        ##---------------------------        
        <td>
            <a href="${h.url('content', id=content['id'])}">
                <p class="content_title">${content['title']}</p>
                <p class="content_details">
                    ${content['creation_date'].strftime('%b %d, %Y %H:%M %Z')}
                </p>
                <p class="content_preview">content['content_short']</p>
                ##${h.truncate(  , length=120, indicator='...', whole_word=True)}
            </a>
        </td>
        
        <td>
            ##---------------------------
            ## Creator
            ##---------------------------
            ${member_includes.avatar(content['creator'], show_name=True, class_="content_creator_thumbnail")}
            
            ##---------------------------
            ## Other details
            ##---------------------------
            
            ## WARNING!!!! This is performing a full query to get all responses and comments, these should be replaced with derived fields
            ## Ticket raised
            <br>${ungettext("%d response", "%d responses", content['num_responses']) % content['num_responses']}
            <br>${ungettext("%d comment" , "%d comments" , content['num_comments' ]) % content['num_comments' ]}
        </td>
        
        ##---------------------------
        ## Action Buttons
        ##---------------------------
        % if actions:
        <td>
            % if content['status'] == "locked":
              <span class="icon_large icon_locked">Approved and locked</span>
            % else:
              <a class="button_small button_small_style_2" href="${h.url('edit_content', id=content['id'])}">
                ${_("Edit")}
              </a>
			  ${h.secure_link(
				href=url('content', id=content['id']), method="DELETE",
				value=_("Delete"),
				css_class="button_small button_small_style_2",
				confirm_text=_("Are your sure you want to delete this content?")
              )}
            %endif
        </td>
        % endif
        
    </tr>
</%def>


##------------------------------------------------------------------------------
## Content List Mini (with thumbnails)
##------------------------------------------------------------------------------
<%def name="content_item_row_mini(content, location=False)">
    <tr>
        <td class="content_thumbnail">
            <a href="${h.url('content', id=content['id'])}">
                <img src="${content['thumbnail_url']}" alt="${content['title']}" />
            </a>
        </td>
        <td>
            <a href="${h.url('content', id=content['id'])}">
                <p class="content_title">${content['title']}</p>
            </a>
        </td>
        % if location:
        <td>
            flag
        </td>
        % endif
        <td>
            rating <br/> comments
        </td>
        <td>
            ${member_includes.avatar(content['creator'], show_name=True, class_="content_creator_thumbnail")}
        </td>
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
<a href="${url('content', id=content['id'])}">${content['title']}</a>
</%def>
