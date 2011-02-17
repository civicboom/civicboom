<%inherit file="/frag/common/frag.mako"/>
<%! import datetime %>

<%namespace name="frag_lists"      file="/frag/common/frag_lists.mako"   />
<%namespace name="flag"            file="/frag/content_actions/flag.mako"/>
<%namespace name="share"           file="/frag/common/share.mako"        />
<%namespace name="popup"           file="/html/web/common/popup_base.mako"    />
<%namespace name="member_includes" file="/html/web/common/member.mako"        />


## for deprication
<%namespace name="loc"             file="/html/web/common/location.mako"     />

<%!
    rss_url = True
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.content   = d['content']
        self.id        = self.content['id']
        self.actions   = d['actions']
        
        self.attr.title     = _('_'+self.content['type']).capitalize()
        self.attr.icon_type = self.content['type']
        
        # AllanC - rather than duplicating the formating information multiple times - use the subroutene h.api_datestr_to_datetime and time ago
        #self.creation_date = datetime.datetime.strptime(self.content['creation_date'].split('.')[0], "%Y-%m-%d %H:%M:%S") if self.content.get('creation_date') else nothing
        #self.update_date = datetime.datetime.strptime(self.content['update_date'].split('.')[0], "%Y-%m-%d %H:%M:%S") if self.content.get('update_date') else nothing
        #self.publish_date = datetime.datetime.strptime(self.content['publish_date'].split('.')[0], "%Y-%m-%d %H:%M:%S") if self.content.get('publish_date') else nothing
        #self.due_date = datetime.datetime.strptime(self.content['due_date'].split('.')[0], "%Y-%m-%d %H:%M:%S") if self.content.get('due_date') else nothing
        #self.event_date = datetime.datetime.strptime(self.content['event_date'].split('.')[0], "%Y-%m-%d %H:%M:%S") if self.content.get('event_date') else nothing
        
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
        
        self.attr.help_frag = self.content['type']
        if self.attr.help_frag == 'draft':
            self.attr.help_frag = 'create_'+self.content['target_type']
        
        self.attr.auto_georss_link = True
    %>
</%def>


##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">

    <div class="frag_left_col">
        <div class="frag_col">
        ${content_title()}
        ${content_media()}
        ${content_content()}
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
        <div style="clear:left;" class="frag_list">
          <h2><span class="icon icon_${self.content['creator']['type']}"><span>${self.content['creator']['type']}</span><div style="display:inline-block;padding-left:19px; width: 100%">Created&nbsp;by</div></span></h2>
          <div class="frag_list_contents">
            <div class="content" style="padding-bottom: 11px;">
              <div>
                <span style="float:left; padding-right: 3px;">${member_includes.avatar(self.content['creator'], show_name=True, show_follow_button=True, class_="large")}</span>
              ##${frag_lists.member_list(content['creator'], _("Creator"))}
                <div>
                  <span style="font-weight: bold;">${self.content['creator']['name']}</span><br />
                  Type: ${self.content['creator']['type'].capitalize()}<br />
                  ## Member Info Here
                  ##% if self.member['website'] != '':
                  ##  Website: ${self.member['join_date']}<br />
                  ##% endif
                  ##Joined: ${self.member['join_date']}<br />
                </div>
              </div>
            </div>
          </div>
        </div>
        ##<h2>${_("Content by")}</h2>
        ${content_details_foot()}
        ${content_details()}
        ${content_license()}
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
                [m for m in d['accepted_status']['items'] if m['status']=='accepted'],
                _("Accepted by"),
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='invited'],
                _("Invited"),
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='withdrawn'],
                _("Withdrawn"),
            )}
        % endif
        
        </div>
    </div>

</%def>

##------------------------------------------------------------------------------
## Content Title
##------------------------------------------------------------------------------

<%def name="content_title()">
    ##----Title----
    <h1>${self.content['title']}</h1>
</%def>

##------------------------------------------------------------------------------
## Content Details
##------------------------------------------------------------------------------
<%def name="content_details()">
    <% content = self.content %>

    <div class="details">
        
        <%def name="detail(field_name)">
            % if content.get(field_name):
            <p>${field_name}: ${content[field_name]}</p>
            % endif
        </%def>
        <%def name="format_date_if(title, date_input, fuzzy=True)">
          % if date_input:
            <tr>
              <td><span class="icon icon_date" title="${title}"><span>&nbsp;</span></span></td>
              <td>${title}</td>
              % if fuzzy:
                <td colspan="4">${h.time_ago(date_input)}</td>
              % else:
                <td colspan="4">${datetime.datetime.strftime(h.api_datestr_to_datetime(date_input), '%d/%m/%Y')}</td>
              % endif
            </tr>
          % endif
        </%def>
        <%def name="iconify(field_name, title, icon_classes)">
          % if content.get(field_name):
            <span class="${icon_classes}" title="${title}"><span>${title}</span></span>
          % endif
        </%def>
        <style type="text/css">
          table.content tr td { padding-right: 3px; }
          table.content tr td.x { padding-left: 3px; }
        </style>
        <table class="content">
          <tr>
            <td><span class="icon icon_boom"><span>Boom</span></span></td>
            <td>Booms</td>
            <td>${content['boom_count'] if 'boom_count' in content else '0'}</td>
            <td class="x"><span class="icon icon_seen"><span>Views</span></span></td>
            <td>Views</td>
            <td>${content['views'] if 'views' in content else '0'}</td>
          </tr>
        </table>
        <div class="padded">${rating()}</div>
        <div class="iconholder padded">
          ${iconify('private', 'Private Content', 'icon icon_private')}
          ${iconify('closed', 'Closed', 'icon icon_closed')}
          % if content.get('approval')=='approved':
            <div class="icon icon_approved" title="approved"><span>Approved</span></div>${_("Approved")}
          % endif
          <span style="float: right;">${iconify('edit_lock', 'Locked for editing', 'icon icon_edit_lock')}</span>
        </div>
    </div>


</%def>


##------------------------------------------------------------------------------
## Content Details Footer
##------------------------------------------------------------------------------
<%def name="content_details_foot()">
    <% content = self.content %>
    <div class="details">
      <%def name="detail(field_name)">
          % if content.get(field_name):
          <p>${field_name}: ${content[field_name]}</p>
          % endif
      </%def>
        <%def name="format_date_if(title, date_input, fuzzy=True, trclass=None)">
          % if date_input:
            <tr${' class=%s' % trclass if trclass else ''}>
              <td><span class="icon icon_date"><span>&nbsp;</span></span></td>
              <td>${title}</td>
              % if fuzzy:
                <td>${_('%s ago') % h.time_ago(date_input)}</td>
              % else:
                <td>${datetime.datetime.strftime(h.api_datestr_to_datetime(date_input), '%d/%m/%Y')}</td>
              % endif
            </tr>
          % endif
        </%def>
      <%def name="iconify(field_name, title, icon_classes)">
        % if content.get(field_name):
          <span class="${icon_classes}"><span>${title}</span></span>
        % endif
      </%def>
      <style type="text/css">
        table.content tr td { padding-right: 3px; }
        table.content tr td.x { padding-left: 3px; }
      </style>
      <table class="content">
##        ${format_date_if('Created'  , content.get('creation_date'))}</p>
        ${format_date_if('Published', content.get('publish_date' ))}</p>
        % if content.get('publish_date') != content.get('update_date'):
          ${format_date_if('Updated'  , content.get('update_date'  ))}</p>
        % endif
        ${format_date_if('Event Date', content.get('event_date'), False, 'bold')}
        ${format_date_if('Due By'    , content.get('due_date'), False, 'bold'  )}
      </table>
    </div>


</%def>


##------------------------------------------------------------------------------
## Content
##------------------------------------------------------------------------------

<%def name="content_content()">

    <div class="content_text">
      ${h.literal(h.scan_for_embedable_view_and_autolink(self.content['content']))}
    </div>
</%def>


##------------------------------------------------------------------------------
## License
##------------------------------------------------------------------------------

<%def name="content_license()">
    % if 'license' in self.content:
    <% license = self.content['license'] %>
    <div class="padded" style="margin-top:14px">
      <a href="${license['url']}" target="_blank" title="${license['description']}">
        <img src="/images/licenses/${license['id']}.png" alt="${license['name']}" />
      </a>
    </div>
    % endif
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
        <li class="paddedbottom">
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
        % if media.get('caption') or media.get('credit'):
          <br />
        % endif
        % if media.get('caption'):
          <span class="caption">${media['caption']}</span>
        % endif
        % if media.get('credit'):
          <span class="credit">(${_('Credit to')}: ${media['credit']})</span>
        % endif
        <br />
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
    comments = d['comments']['items']
%>
<div style="padding-top: 20px;" class="acceptrequest">
  % if 'publish' in self.actions:
      ${h.secure_link(
          h.args_to_tuple('content', id=self.id, format='redirect', submit_publish='publish') ,
          method = "PUT" ,
          css_class = 'button',
          value           = _('Publish') ,
          json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
          
      )}
      <span class="separtor"></span>
  % endif
  ## --- Respond -------------------------------------------------------------
  % if self.content['type'] != 'draft':
      ${h.secure_link(
          h.args_to_tuple('new_content', parent_id=self.id) ,
          css_class = 'button',
          value           = _("Respond") ,
          json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , 
      )}
      ## AllanC the cb_frag creates a new fragment, data is the return fron the JSON call to the 'new_content' method
      ##        it has to be done in javascript as a string as this is handled by the client side when the request complete successfully.
      <span class="separtor"></span>
  % endif
  % if 'accept' in self.actions:
      ${h.secure_link(
          h.args_to_tuple('content_action', action='accept'  , format='redirect', id=self.id) ,
          css_class = 'button',
          value           = _('Accept') ,
          json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
      )}
      ##${h.secure_link(h.args_to_tuple('content_action', action='accept'  , format='redirect', id=id), value=_('Accept'),  css_class="icon icon_accept")}
      <span class="separtor"></span>
  % endif
  
  % if 'withdraw' in self.actions:
      ${h.secure_link(
          h.args_to_tuple('content_action', action='withdraw', format='redirect', id=self.id) ,
          css_class = 'button',
          value           = _('Withdraw') ,
          json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
      )}
      <span class="separtor"></span>
  % endif
</div>
<div class="comments">
    <h2 style="padding-top: 20px; padding-bottom: 10px;">${_("Comments")}</h2>

    <table>
        <tr style="display: none;"><th>${_('Member')}</th><th>${_('Comment')}</th></tr>
        % for comment in comments:
        <tr>
            <td style="padding-bottom: 6px" class="comment_avatar">
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
                ${popup.link(h.args_to_tuple('content_action', action='flag', id=comment['id']), title=_('Flag as') , class_='icon icon_flag')}
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
                    <br /><input type="submit" name="submit_response" value="${_('Comment')}">
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

    ## --- Pubish --------------------------------------------------------------

    % if 'publish' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect', submit_publish='publish') ,
            method = "PUT" ,
            value           = _('Publish') ,
            value_formatted = h.literal("<span class='icon icon_publish'></span>%s") % _('Publish') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
            
        )}
        <span class="separtor"></span>
    % endif


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
            confirm_text    = _('Click OK to approve this. Once approved, no further changes can be made by the creator, and further details will be sent to your inbox.'),
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
            h.args_to_tuple('content_action', action='disassociate', format='redirect', id=self.id),
            value           = _('Disassociate') ,
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
            json_form_complete_actions = "cb_frag_reload('contents/%s'); cb_frag_remove(current_element);" % self.id,
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
