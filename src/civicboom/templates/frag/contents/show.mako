<%namespace name="frag_list" file="/frag/common/frag_lists.mako"/>
<%namespace name="share"     file="/frag/common/share.mako"     />

## for deprication
<%namespace name="loc"              file="/web/common/location.mako"     />
<%namespace name="member_includes"  file="/web/common/member.mako"       />
<%namespace name="content_includes" file="/web/common/content_list.mako" />



##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
${frag_content(d)}
</%def>

##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="frag_content(d)">
    <% content = d['content'] %>
    
    <div class="action_bar">
        ${action_bar(d['actions'])}
    </div>
    <div class="action_bar_content">
        ${action_bar_content(d['actions'])}
    </div>
    
    <div class="frag_data frag_content">
        <div class="frag_left_col">
            <div class="frag_col">
            ${content_details( content)}
            ${content_media(   content)}
            ${content_map(     content)}
            ${content_comments(d['comments'])}
            </div>
        </div>
        <div class="frag_right_col">
            <div class="frag_col">
            ${creator(  content)}
            ${parent(   content)}
            ${responses(d['responses'])}
            </div>
        </div>
    </div>
</%def>


##------------------------------------------------------------------------------
## Content Details
##------------------------------------------------------------------------------
<%def name="content_details(content)">

    ##----Title----
    <h1>${content['title']}</h1>

    <div class="details">
        
        ##----Details----
        % if hasattr(content,'views'):
        <p>${_("views: %d") % content['views']}</p>
        % endif
        
        
        <ul class="status">
            % if 'response_type' in content and content['response_type']=='approved':
            <li><div class="icon_large icon_approved_large" title="approved content"></div>${_("approved content")}</li>
            % endif
        </ul>
    </div>

    ##----Content----
    <div class="content_text">
      ${h.literal(h.scan_for_embedable_view_and_autolink(content['content']))}
    </div>

</%def>

##------------------------------------------------------------------------------
## Media
##------------------------------------------------------------------------------
<%def name="content_media(content)">

    <ul class="media">
    % for media in content['attachments']:
        <li>
        % if media['type'] == "image":
            <a href="${media['original_url']}"><img src="${media['media_url']}" alt="${media['caption']}"/></a>
        % elif media['type'] == "audio":
            <object type="application/x-shockwave-flash" data="/flash/player_flv_maxi.swf" width="320" height="30">
                <param name="movie" value="/flash/player_flv_maxi.swf" />
                <param name="allowFullScreen" value="true" />
                <param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;showvolume=1&amp;showplayer=always&amp;showloading=always" />
            </object>
        % elif media['type'] == "video":
            <object type="application/x-shockwave-flash" data="/flash/player_flv_maxi.swf" width="320" height="240">
                <param name="movie" value="/flash/player_flv_maxi.swf" />
                <param name="allowFullScreen" value="true" />
                <param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;startimage=${media['thumbnail_url']}&amp;showvolume=1&amp;showfullscreen=1" />
            </object>
        % else:
            ${_("unrecognised media type: %s") % media['type']}
        % endif
        </li>
    % endfor
    </ul>


    ## To maintain compatability the form to flag offensive content is included (hidden) at the bottom of content and viewed by JQuery model plugin
    ${flag_form()}

</%def>

##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="content_map(content)">
    % if content.get('location'):
        <%
        lat = content['location'].split(' ')[0]
        lon = content['location'].split(' ')[1]
        %>
        <p>
        ${loc.minimap(
            width="100%", height="200px",
            lat = lat,
            lon = lon,
            feeds = [
                dict(pin='yellow',  url='/contents.rss?location='+lon+','+lat   ),
                dict(pin='red',     url='/contents.rss?id='+content['id']  )
            ]
        )}
        </p>
    % endif
</%def>


##------------------------------------------------------------------------------
## Comments
##------------------------------------------------------------------------------
<%def name="content_comments(comments)">
<div class="comments">
    <h2>${_("Comments")}</h2>

    <table>
        <tr style="display: none;"><th>${_('Member')}</th><th>${_('Comment')}</th></tr>
        % for comment in comments:
        <tr>
            <td class="comment_avatar">
                ${member_includes.avatar(comment['creator'])}
            </td>
            <td class="comment">
                <p class="comment_by"     >${comment['creator']['name'] or comment['creator']['username']}</p>
                
                <p class="comment_content">${comment['content']}</p>
                
                ##<b style="float: right;">
                ##	${comment['creator']['name']}
                    ##${relation(comment['creator'], c.logged_in_persona, d['content']['creator'], 'text')} --
                ##	${str(comment['creation_date'])[0:19]}
                ##</b>
            </td>
        </tr>
        % endfor
        <tr>
            <td class="comment_avatar">
                % if c.logged_in_persona:
                ${member_includes.avatar(c.logged_in_persona.to_dict())}
                %endif
            </td>
            <td class="comment">
                ${h.form(url('contents', format='redirect'))}
                    <input type="hidden" name="parent_id" value="${d['content']['id']}">
                    <input type="hidden" name="title" value="Re: ${d['content']['title']}">
                    <input type="hidden" name="type" value="comment">
                    <textarea name="content" class="comment_textarea"></textarea>
                    <br><!--<input type="submit" name="submit_preview" value="Preview">-->
                    <input type="submit" name="submit_response" value="${_('Comment')}">
                ${h.end_form()}
            </td>
        </tr>
    </table>
</div>
</%def>


##------------------------------------------------------------------------------
## Creator
##------------------------------------------------------------------------------
<%def name="creator(content)">
    <h2>${_("Content by")}</h2>
    ${member_includes.avatar(content['creator'], show_name=True, show_follow_button=True, class_="large")}
</%def>

##------------------------------------------------------------------------------
## Parent
##------------------------------------------------------------------------------
<%def name="parent(content)">
    % if content['parent']:
    <h2>${_("Parent content")}</h2>
    ${content_includes.content_list([content['parent']], mode="mini", class_="content_list_mini")}
    % endif
</%def>

##------------------------------------------------------------------------------
## Responses
##------------------------------------------------------------------------------
<%def name="responses(responses)">
    <h2>${_("Responses")}</h2>
    ${content_includes.content_list(responses, mode="mini", class_="content_list_mini")}
</%def>
    
##------------------------------------------------------------------------------
## Accepted by
##------------------------------------------------------------------------------
<%def name="accepted_by()">
    % if 'accepted_status' in d:
        <h2>${_("Assignment")}</h2>
        % if 'accepted' in d['content']:
            <h3>${_("accepted by: %d") % len(d['accepted_status']['accepted'])}</h3>
            ${member_includes.member_list(d['accepted_status']['accepted'] , show_avatar=True, class_="avatar_thumbnail_list")}
        % endif
        
        % if 'invited' in d['content']:
            <h3>${_("awaiting reply: %d") % len(d['accepted_status']['invited'])}</h3>
            ${member_includes.member_list(d['accepted_status']['invited']  , show_avatar=True, class_="avatar_thumbnail_list")}
        % endif
        
        % if 'withdrawn' in d['content']:
            <h3>${_("withdrawn members: %d") % len(d['content']['withdrawn'])}</h3>
            ${member_includes.member_list(d['accepted_status']['withdrawn'], show_avatar=True, class_="avatar_thumbnail_list")}
        % endif
    % endif
</%def>

##------------------------------------------------------------------------------
## Action Bar
##------------------------------------------------------------------------------
<%def name="action_bar(actions)">

    <% id = d['content']['id'] %>

    <div class="type_actions">
        <% type = d['content']['type'] %>
        <span class="icon icon_${type}"></span><span class="title">${type.capitalize()}</span>
    </div>
    
    <div class="common_actions">
        <a href='' onclick="$('#flag_content').modal(); return false;" title='${_("Flag inappropriate content")}' class="icon icon_flag"><span>Flag</span></a>

        ${share.share(
            url         = url('content', id=d['content']['id'], host=app_globals.site_host, protocol='http'),
            title       = d['content']['title'] ,
        )}
        
        <a href='${url('formatted_content', id=id, format='rss')}'  title='RSS'   class="icon icon_rss"  ><span>RSS  </span></a>
        <a href='' onclick="cb_frag_remove($(this)); return false;" title='Close' class="icon icon_close"><span>Close</span></a>
    </div>



</%def>
    
<%def name="action_bar_content(actions)">
    <% id = d['content']['id'] %>
	<ul>
        <li>
            ${h.secure_link(url('new_content', parent_id=id), value=_("Respond to this"))}
        </li>
        
        ## Content Owner Actions
        % if 'edit' in actions:
            <li><a href="${h.url('edit_content', id=id)}" class="">${_("Edit")}</a></li>
            <li>${h.secure_link(url('content', id=id, format='redirect'), method="DELETE", value=_("Delete"), css_class="button_small button_small_style_2", confirm_text=_("Are your sure you want to delete this content?") )}</li>
        % endif
        
        ## Assignment Accept and Withdraw
        % if 'accept' in actions:
            <li>${h.secure_link(h.args_to_tuple('content_action', action='accept'  , format='redirect', id=id), _('Accept')  , css_class="")}</li>
        % endif
        % if 'withdraw' in d['actions']:
            <li>${h.secure_link(h.args_to_tuple('content_action', action='withdraw', format='redirect', id=id), _('Withdraw'), css_class="")}</li>
        % endif
        
        % if 'boom' in actions:
            <li>${h.secure_link(h.args_to_tuple('content_action', action='boom'    , format='redirect', id=id), _('Boom')    , css_class="")}</li>
        % endif
        
        ## Parent Content Owner Actions
        ## TODO needs to be some check to see if user is an organisation and has paid for the power to do this
        ##% if content.actions:
        ##    <a href="" class="button_small button_small_style_2">
        ##        Email Resorces
        ##    </a>
        
        % if 'approve' in actions:
            <li class="approve"     >${h.secure_link(h.args_to_tuple('content_action', action='approve'    , format='redirect', id=id), _('Approve & Lock'), title=_("Approve and lock this content so no further editing is possible"), css_class="button_small button_small_style_2", confirm_text=_('Once approved this article will be locked and no further changes can be made') )}</li>
        % endif
        % if 'seen' in actions:
            <li class="seen"        >${h.secure_link(h.args_to_tuple('content_action', action='seen'       , format='redirect', id=id), _('Seen, like it')   , title=_("Seen it, like it"),                                              css_class="button_small button_small_style_2" )}</li>
        % endif
        % if 'dissasociate' in actions:
            <li class="dissasociate">${h.secure_link(h.args_to_tuple('content_action', action='disasociate', format='redirect', id=id), _('Disasociate')   , title=_("Dissacociate your content from this response"),                    css_class="button_small button_small_style_2", confirm_text=_('This content with no longer be associated with your content, are you sure?')   )}</li>
        % endif
    </ul>
    
</%def>


##------------------------------------------------------------------------------
## Flag Form
##------------------------------------------------------------------------------

<%def name="flag_form()">
    <div id="flag_content" class="hideable">
      <p class="form_instructions">${_('Flag this _content as inappropriate')}</p>
      ${h.form(url(controller='content_actions', action='flag', id=d['content']['id'], format='redirect'))}
          <select name="type">
              <% from civicboom.model.content import FlaggedContent %>
              % for type in [type for type in FlaggedContent._flag_type.enums if type!="automated"]:
              <option value="${type}">${_(type.capitalize())}</option>
              % endfor
          </select>
          <p class="form_instructions">${_('Comment (optional)')}</p>
          <textarea name="comment" style="width:90%; height:3em;"></textarea>
          <input type="submit" name="flagit" value="Flag it" class=""/>
          ##<a class="simplemodal-close">${_("Cancel")}</a>
      ${h.end_form()}
    </div>
</%def>


##------------------------------------------------------------------------------
## Other Actions (to be refined)
##------------------------------------------------------------------------------

<%def name="other_actions()">
    ##-----Share Article Links--------

    ##<% from civicboom.model.content import UserVisibleContent %>
    ##% if issubclass(content_obj.__class__, UserVisibleContent):
    % if (d['content']['type'] == 'article' or d['content']['type'] == 'assignment') and config['online']:
    <h2>${_("Share this")}</h2>
        ${share_links()}
    % endif
  

    ##-------- Licence----------
    <h2>${_("Licence")}</h2>
        <a href="${d['content']['license']['url']}" target="_blank" title="${d['content']['license']['name']}">
          <img src="/images/licenses/${d['content']['license']['code']}.png" alt="${d['content']['license']['name']}" />
        </a>
  
    ##-----Copyright/Inapropriate?-------
    <h2>${_("Content issues?")}</h2>
      <a href="" class="button_small button_small_style_1" onclick="swap('flag_content'); return false;">${_("Inappropriate Content?")}</a>
    
      <div id="flag_content" class="hideable">
        <p class="form_instructions">${_('Flag this _content as inappropriate')}</p>
        ${h.form(url(controller='content_actions', action='flag', id=d['content']['id'], format='redirect'))}
            <select name="type">
                <% from civicboom.model.content import FlaggedContent %>
                % for type in [type for type in FlaggedContent._flag_type.enums if type!="automated"]:
                <option value="${type}">${_(type.capitalize())}</option>
                % endfor
            </select>
            <p class="form_instructions">${_('Comment (optional)')}</p>
            <textarea name="comment" style="width:90%; height:3em;"></textarea>
            <input type="submit" name="flagit" value="Flag it" class="button_small button_small_style_tiny "/>
            <span class="button_small button_small_style_tiny " onclick="swap('flag_content'); return false;">${_("Cancel")}</span>
        ${h.end_form()}
      </div>
</%def>



<%def name="rating()">
    % if 'rating' in d['content']:
        <li>
<%
def selif(r, n):
	if round(r) == n:
		return " selected"
	else:
		return ""
r = (d['content']['rating'] * 5)
%>
		<form id="rating" action="${url('content_action', action='rate', id=d['content']['id'], format='redirect')}" method="POST">
			<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
			<select name="rating" style="width: 120px">
				<option value="0">Unrated</option>
				<option value="1"${selif(r, 1)}>Very poor</option>
				<option value="2"${selif(r, 2)}>Not that bad</option>
				<option value="3"${selif(r, 3)}>Average</option>
				<option value="4"${selif(r, 4)}>Good</option>
				<option value="5"${selif(r, 5)}>Perfect</option>
			</select>
			<input type="submit" value="Rate!">
		</form>
		<script>
		$(function() {
			$("#rating").children().not("select").hide();
			$("#rating").stars({
				inputType: "select",
				callback: function(ui, type, value) {
					## $("#rating").submit();
					$.ajax({
						url: "${url(controller='content_actions', action='rate', id=d['content']['id'], format='json')}",
						type: "POST",
						data: {
							"_authentication_token": "${h.authentication_token()}",
							"rating": value
						},
						dataType: "json",
						success: function(data) {flash_message(data);},
						error: function(XMLHttpRequest, textStatus, errorThrown) {flash_message(textStatus);}
					});
				}
			});
		});
		</script>
        </li>
    % endif

</%def>
