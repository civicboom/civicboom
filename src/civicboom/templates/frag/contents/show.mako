<%inherit file="/frag/common/frag.mako"/>

<%namespace name="frag_lists"      file="/frag/common/frag_lists.mako"   />
<%namespace name="flag"            file="/frag/content_actions/flag.mako"/>
<%namespace name="share"           file="/frag/common/share.mako"        />
<%namespace name="popup"           file="/web/common/popup_base.mako"    />
<%namespace name="member_includes" file="/web/common/member.mako"        />


## for deprication
<%namespace name="loc"              file="/web/common/location.mako"     />


##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.content   = d['content']
        self.id        = self.content['id']
        self.actions   = d['actions']
        
        self.attr.title     = self.content['type'].capitalize()
        self.attr.icon_type = self.content['type']
        
        self.attr.frag_data_css_class = 'frag_content'
        
        if self.content['private'] == False:
            self.attr.share_kwargs = {
                'url'      : self.attr.html_url ,
                'title'    : self.content.get('title') ,
                'summary'  : self.content.get('content_short') ,
                'image'    : self.content.get('thumbnail_url') ,
                'published': self.content.get('publish_date') ,
                'updated'  : self.content.get('update_date') ,
                'author'   : self.content.get('creator', dict()).get('name') ,
            }
        
        self.attr.auto_georss_link = True
    %>
</%def>


##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">

    <div class="frag_left_col">
        <div class="frag_col">
        ${content_details()}
        ${content_media()}
        ${content_map()}
        ${content_comments()}
        ## To maintain compatability the form to flag offensive content is included (hidden) at the bottom of content and viewed by JQuery model plugin
        <%def name="flag_form()">
            ${flag.flag_form(self.id)}
        </%def>
        ${popup.popup_static(_('Flag content'), flag_form, 'flag_content')}
        </div>
    </div>
    <div class="frag_right_col">
        <div class="frag_col">
        
        <h2>${_("Content by")}</h2>
        ${member_includes.avatar(self.content['creator'], show_name=True, show_follow_button=True, class_="large")}
        ##${frag_lists.member_list(content['creator'], _("Creator"))}
        
        % if self.content['parent']:
            ${frag_lists.content_list(self.content['parent'], _("Parent content"), creator=True)}
        % endif
        
        ${frag_lists.content_list(
            d['responses'],
            _("Responses"),
            href=h.args_to_tuple('contents', response_to=self.id),
            creator=True
        )}
        
        % if 'accepted_status' in d:
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status'] if m['status']=='accepted'],
                _("Accepted by"),
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status'] if m['status']=='invited'],
                _("Invited"),
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status'] if m['status']=='withdrawn'],
                _("Withdrawn"),
            )}
        % endif
        
        </div>
    </div>

</%def>


##------------------------------------------------------------------------------
## Content Details
##------------------------------------------------------------------------------
<%def name="content_details()">
    <% content = self.content %>

    ##----Title----
    <h1>${content['title']}</h1>

    <div class="details">
        
        ##----Details----
        % if hasattr(content,'views'):
        <p>${_("views: %d") % content['views']}</p>
        % endif
        
        
        <ul class="status">
            % if 'approval' in content and content['approval']=='approved':
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
<%def name="content_media()">
    <%
        content = self.content
    %>
    <%
        media_width  = config['media.display.video.width' ]
        media_height = config['media.display.video.height']
    %>

    <ul class="media">
    % for media in content['attachments']:
        <li>
        % if media['type'] == "image":
            <a href="${media['original_url']}"><img src="${media['media_url']}" alt="${media['caption']}" style="max-width: ${media_width}px; max-height: ${media_height}px;"/></a>
        % elif media['type'] == "audio":
            <object type="application/x-shockwave-flash" data="/flash/player_flv_maxi.swf" width="${media_width}" height="30">
                <param name="movie" value="/flash/player_flv_maxi.swf" />
                <param name="allowFullScreen" value="true" />
                <param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;showvolume=1&amp;showplayer=always&amp;showloading=always" />
            </object>
        % elif media['type'] == "video":
            <object type="application/x-shockwave-flash" data="/flash/player_flv_maxi.swf" width="${media_width}" height="${media_height}">
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

</%def>

##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="content_map()">
    <% content = self.content %>
    % if content.get('location'):
        <%
        lat = content['location'].split(' ')[0]
        lon = content['location'].split(' ')[1]
        %>
        <p>
        ${loc.minimap(
            name=h.uniqueish_id("map", content['id']),
            width="100%", height="200px",
            lat = lat,
            lon = lon,
            feeds = [
                dict(pin='yellow',  url='/contents.rss?location=%s,%s' % (lon,lat)      ),
                dict(pin='red',     url='/contents.rss?id=%s'          % content['id']  ),
            ]
        )}
        </p>
    % endif
</%def>


##------------------------------------------------------------------------------
## Comments
##------------------------------------------------------------------------------
<%def name="content_comments()">
<%
    content  = self.content
    comments = d['comments']
%>
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
            <td>
                ${popup.link(h.args_to_tuple('content_action', action='flag', id=comment['id']), title=_('Flag as offensive/spam') , class_='icon icon_flag')}
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
                ${h.form(h.args_to_tuple('contents', format='redirect'), json_form_complete_actions="cb_frag_reload(current_element);" )}
                    ##% url("content",id=d['content']['id'])
                    ## AllanC: RAAAAAAAAAAAAR!!! cb_frag_reload($(this)); does not work, because $(this) for forms is not a jQuery object?! so we cant use .parents() etc .. WTF!!!
                    ##         so to get round this I just submit a string to the reload ... not happy!
                    ##         workaround - turns up higher up $(this) works ... so I put it in a variable called current_element that is accessible
                    <input type="hidden" name="parent_id" value="${d['content']['id']}">
                    <input type="hidden" name="title" value="Re: ${d['content']['title']}">
                    <input type="hidden" name="type" value="comment">
                    <textarea name="content" class="comment_textarea"></textarea>
                    <br><!--<input type="submit" name="submit_preview" value="Preview">-->
                    <input type="submit" name="submit_response" value="${_('Comment')}">
                ${h.end_form()}
            </td>
            <td>
                ##padding col for flag actions
            </td>
        </tr>
    </table>
    
</div>
</%def>





##------------------------------------------------------------------------------
## Actions
##------------------------------------------------------------------------------

<%doc>
        ${share.share(
            url         = url('content', id=d['content']['id'], host=app_globals.site_host, protocol='http'),
            title       = d['content']['title'] ,
        )}
        
        
    ## Parent Content Owner Actions
    ## TODO needs to be some check to see if user is an organisation and has paid for the power to do this
    ##% if content.actions:
    ##    <a href="" class="button_small button_small_style_2">
    ##        Email Resorces
    ##    </a>
</%doc>
    
<%def name="actions_specific()">

    ## --- Respond -------------------------------------------------------------

    % if self.content['type'] != 'draft':
        ${h.secure_link(
            h.args_to_tuple('new_content', parent_id=self.id) ,
            value           = _("Respond") ,
            value_formatted = h.literal("<span class='icon icon_respond'></span>%s") % _('Respond') ,
            json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , 
        )}
        ## AllanC the cb_frag creates a new fragment, data is the return fron the JSON call to the 'new_content' method
        ##        it has to be done in javascript as a string as this is handled by the client side when the request complete successfully.
        <span class="separtor"></span>
    % endif
    
    ## --- Accept / Withdraw ---------------------------------------------------
    
    % if 'accept' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='accept'  , format='redirect', id=self.id) ,
            value           = _('Accept') ,
            value_formatted = h.literal("<span class='icon icon_accept'></span>%s") % _('Accept') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        ##${h.secure_link(h.args_to_tuple('content_action', action='accept'  , format='redirect', id=id), value=_('Accept'),  css_class="icon icon_accept")}
        <span class="separtor"></span>
    % endif
    
    % if 'withdraw' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='withdraw', format='redirect', id=self.id) ,
            value           = _('Withdraw') ,
            value_formatted = h.literal("<span class='icon icon_withdraw'></span>%s") % _('Withdraw'),
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        <span class="separtor"></span>
    % endif
    
    ## --- Boom ----------------------------------------------------------------
    
    % if 'boom' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='boom', format='redirect', id=self.id) ,
            value           = _('Boom') ,
            value_formatted = h.literal("<span class='icon icon_boom'></span>%s") % _('Boom') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        <span class="separtor"></span>
    % endif
    
    ## --- Approve/Viewed/Dissacocite ------------------------------------------
    
    % if 'approve' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='approve', format='redirect', id=self.id),
            value           = _('Approve & Lock'),
            value_formatted = h.literal("<span class='icon icon_approve'></span>%s") % _('Approve & Lock'),
            title           = _("Approve and lock this content so no further editing is possible"),
            confirm_text    = _('Once approved this article will be locked and no further changes can be made'),
            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    % if 'seen' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='seen'   , format='redirect', id=self.id),
            value           = _('Viewed') ,
            value_formatted = h.literal("<span class='icon icon_seen'></span>%s") % _('Viewed'),
            title           = _("Mark this content as viewed") ,
            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    % if 'dissasociate' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='disasociate', format='redirect', id=self.id),
            value           = _('Disasociate') ,
            value_formatted = h.literal("<span class='icon icon_dissasociate'></span>%s") % _('Disasociate'),
            title           = _("Dissacociate your content from this response") ,
            confirm_text    = _('This content with no longer be associated with your content, are you sure?') ,
            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
</%def>        

    
<%def name="actions_common()">
    
    % if 'edit' in self.actions:
        <a href="${h.url('edit_content', id=self.id)}"
           onclick="cb_frag_load($(this), '${h.url('edit_content', id=self.id, format='frag')}'); return false;"
        ><span class="icon icon_edit"></span>${_("Edit")}</a>
        <span class="separtor"></span>
        
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect'),
            method = "DELETE",
            value           = _("Delete"),
            value_formatted = h.literal("<span class='icon icon_delete'></span>%s") % _('Delete'),
            confirm_text    = _("Are your sure you want to delete this content?"),
            json_form_complete_actions = "cb_frag_remove(current_element);" ,
        )}
        <span class="separtor"></span>
    % endif

    % if 'aggregate' in self.actions:
        ##<a href='' class="icon icon_boom"><span>Aggregate</span></a>
        ${share.janrain_social(self.content, 'janrain', class_='icon icon_share')}
    % endif
    
    % if 'flag' in self.actions:
        <a href='' onclick="$('#flag_content').modal(); return false;" title='${_("Flag inappropriate content")}' class="icon icon_flag"><span>Flag</span></a>
    % endif
    
    % if self.content.get('location'):
        ${parent.georss_link()}
    % endif

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
          <img src="/images/licenses/${d['content']['license']['id']}.png" alt="${d['content']['license']['name']}" />
        </a>
  

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
