
<%namespace name="member_includes" file="member.mako"  />

##------------------------------------------------------------------------------
## Content List (with thumbnails)
##------------------------------------------------------------------------------

<%def name="content_list(results, mode='normal', show_actions=False, max_images=None, class_='content_list')">
    <table class="${class_}">
    % for content in results[:max_images]:
        ##% if not h.isCurrentContent(content):
        % if mode=="normal":
            ${content_item_row(content, show_actions=show_actions)}
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



<%def name="content_item_row(content, show_actions=False)">
    <tr>
        ##---------------------------
        ## Thumbnail
        ##---------------------------
        <td class="thumbnail">
            <div class="clipper">
                <a href="${h.url('content', id=content['id'])}">
                    ${content_thumbnail_icons(content)}
                    <img class="img" src="${content['thumbnail_url']}" alt="${content['title']}"/>
                </a>
            </div>
        </td>
        
        ##---------------------------
        ## Title and Content preview + details
        ##---------------------------        
        <td>
            <a href="${h.url('content', id=content['id'])}">
                <p class="content_title">${content['title']}</p>
                <p class="content_details">
                    ${content['creation_date']}
                    ##.strftime('%b %d, %Y %H:%M %Z')}
                </p>
                <p class="content_preview">${content['content_short']}</p>
                ##${h.truncate(  , length=120, indicator='...', whole_word=True)}
            </a>
        </td>
        
        <td>
            ##---------------------------
            ## Creator
            ##---------------------------
            % if 'creator' in content:
            ${member_includes.avatar(content['creator'], show_name=True, class_="content_creator_thumbnail")}
            % endif
            
            ##---------------------------
            ## Other details
            ##---------------------------
            
            ## WARNING!!!! This is performing a full query to get all responses and comments, these should be replaced with derived fields
            ## Ticket raised
            <br>${ungettext("%s response", "%s responses", content['num_responses']) % content['num_responses']}
            <br>${ungettext("%s comment" , "%s comments" , content['num_comments' ]) % content['num_comments' ]}
        </td>
        
        ##---------------------------
        ## Action Buttons
        ##---------------------------
        % if show_actions:
        <td>
            % if content['edit_lock']:
              <span class="icon32 i_locked">edit locked</span>
            % else:
              <a class="button_small button_small_style_2" href="${h.url('edit_content', id=content['id'])}">
                ${_("Edit")}
              </a>
			  ${h.secure_link(
				href=url('content', id=content['id'], format="redirect"),
                method="DELETE",
				value=_("Delete"),
				link_class="button_small button_small_style_2",
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
        <td class="thumbnail small">
            <div class="clipper">
                <a href="${h.url('content', id=content['id'])}">
                    ${content_thumbnail_icons(content)}
                    <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img"/>
                </a>
            </div>
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
            ${member_includes.avatar(content['creator'], show_name=False, class_="content_creator_thumbnail")}
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


##------------------------------------------------------------------------------
## Content Thumbnail Icons
##------------------------------------------------------------------------------

<%def name="content_thumbnail_icons(content)">
    <div class="icons">
        % if content['private']:
            ${h.icon('private')}
        % endif
        % if content['edit_lock']:
            ${h.icon('edit_lock')}
        % endif
        % if content.get('approval'):
            ${h.icon(content['approval'])}
        % endif
    </div>
</%def>
