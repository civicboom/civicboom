<%inherit file="/frag/common/frag.mako"/>
<%! import datetime %>

<%namespace name="frag_lists"      file="/frag/common/frag_lists.mako"     />
<%namespace name="flag"            file="/frag/content_actions/flag.mako"  />
<%namespace name="share"           file="/frag/common/share.mako"          />
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="member_includes" file="/html/web/common/member.mako"     />
<%namespace name="media_includes"  file="/html/web/media/show.mako"        />

## for deprication
<%namespace name="loc"             file="/html/web/common/location.mako"     />

<%!
    rss_url = True
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="custom_share()">
    <a href="#" onclick="${share.janrain_social_call_content(self.content, 'new_'+(self.content['type'] if not self.content['parent'] else 'response')) | n }; return false;" class="icon16 i_share"><span>Janrain</span></a> 
</%def>

<%def name="init_vars()">
    <%
        self.content   = d['content']
        self.id        = self.content['id']
        self.actions   = d.get('actions', [])
        
        #force = _('_draft') # This var is unused?
        
        # Title
        if self.content['type'] == 'draft':
            self.attr.title     = _('_Draft') + ' ' + _('_'+self.content['target_type'])
        else:
            self.attr.title     = _('_'+self.content['type']).capitalize()
        self.attr.icon_type = self.content['type']
        
        self.attr.frag_data_css_class = 'frag_content'
        
        # Agregation dict
        if self.content['private'] == False and self.content['type'] != 'draft':
            self.attr.share_kwargs = {
                'url'           : h.url('content', id=self.id, qualified=True) ,
                'title'         : self.content.get('title') ,
                'summary'       : self.content.get('content_short') ,
                'image'         : self.content.get('thumbnail_url') ,
                'published'     : self.content.get('publish_date') ,
                'updated'       : self.content.get('update_date') ,
                'author'        : self.content.get('creator', dict()).get('name') ,
                'custom_share'  : custom_share,
            }
        
        # Help Frag
        self.attr.help_frag = self.content['type']
        if self.attr.help_frag == 'draft':
            self.attr.help_frag = 'create_'+self.content['target_type']
        
        # Manipulate Action List
        # - remove actions in exclude_actions kwarg
        if self.kwargs.get('exclude_actions'):
            self.actions = list(set(self.actions) - set(self.kwargs.get('exclude_actions', '').split(',')))
        
        self.attr.auto_georss_link = True
        
        # GregM: Removed popups as we have the janrain share popup now :D
        #if c.logged_in_persona and c.logged_in_persona.username == self.content['creator']['username'] and self.content['type']=='assignment' and not c.logged_in_user.config['help_popup_created_assignment']:
        #    self.attr.popup_url = url(controller='misc', action='help', id='created_assignment', format='frag')
    %>
</%def>


##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
	% if c.logged_in_persona and c.logged_in_persona.username == self.content['creator']['username'] and request.params.get('prompt_aggregate')=='True':
	<script>
		${share.janrain_social_call_content(self.content, 'new_'+(self.content['type'] if not self.content['parent'] else 'response')) | n }
	</script>
	% endif
    ## --- redesign --- ##
    <div class="frag_top_row">
	<div class="frag_col">
	    <div class="content_box">
		${content_title()}
		${content_media()}
		${content_content()}
		${content_map()}
		${content_action_buttons()}
		## ${content_why_resond()}
		${content_comments()}
		## To maintain compatability the form to flag offensive content is included (hidden) at the bottom of content and viewed by JQuery model plugin
		<%def name="flag_form()">
		    ${flag.flag_form(self.id)}
		</%def>
		${popup.popup_static(_('Flag content'), flag_form, 'flag_content')}
		${content_details_foot()}
		${content_details()}
		<span style="display: block; clear: both;"></span>
	    </div>
	</div>
    </div>
	
    <div class="frag_left_col">
        <div class="frag_col">
	    ${frag_lists.content_list(
		d['responses'],
		_("Responses"),
		href=h.args_to_tuple('contents', response_to=self.id),
		creator=True
	    )}
        </div>
    </div>
    
    <div class="frag_right_col">
      <div class="frag_col">
        <%doc><div style="clear:left;" class="frag_list">
          <h2>Set&nbsp;by</h2>
          <div class="frag_list_contents">
            <div class="content">
              <div>
                <span style="float:left; padding-right: 3px;">${member_includes.avatar(self.content['creator'], show_name=True, show_follow_button=True, class_="large")}</span>
              ##${frag_lists.member_list(content['creator'], _("Creator"))}
                <div>
                  <span style="font-weight: bold;">${self.content['creator']['name']}</span><br />
                  Type: ${_('_'+self.content['creator']['type'].capitalize())}<br />
                  ## Member Info Here
                  ##% if self.member['website'] != '':
                  ##  Website: ${self.member['join_date']}<br />
                  ##% endif
                  ##Joined: ${self.member['join_date']}<br />
                </div>
				<div style="clear: both; height: 5px;"></div>
              </div>
            </div>
          </div>
	</div></%doc>
        % if self.attr.share_kwargs:
            ${share.AddThisFragList(**self.attr.share_kwargs)}
        % endif
        
        ##<h2>${_("Content by")}</h2>
        
        % if self.content['parent']:
            ${frag_lists.content_list(self.content['parent'], _("Parent content"), creator=True)}
        % endif
        
        % if 'accepted_status' in d:
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='accepted'],
                _("Accepted by"),
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='invited'],
                _("Invited"),
                hide_if_empty = not 'invite_to_assignment' in self.actions, # Always show this list if invite is avalable
                actions = h.frag_link(value='', title='Invite Members', class_='icon16 i_invite', href_tuple=h.args_to_tuple(controller='invite', action='index', id=self.id, invite='assignment')) if 'invite_to_assignment' in self.actions else None ,
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='withdrawn'],
                _("Withdrawn"),
            )}
        % endif
        ${content_license()}
        </div>
    </div>

</%def>

##------------------------------------------------------------------------------
## Content Title
##------------------------------------------------------------------------------

<%def name="content_title()">
    ##----Title----
    <h1>${self.content['title']}</h1>
    <div style="clear: both;"></div>
    <div class="creator_avatar">
	% if c.logged_in_user:
	${member_includes.avatar(self.content['creator'])}
	%endif
    </div>
    <div class="content_creator">By: ${self.content['creator']['name']}</div>
    ## ${map_icon()}
    <div style="clear: both; padding-bottom: 10px;"></div>
</%def>

##------------------------------------------------------------------------------
## Media icons
##------------------------------------------------------------------------------
<%def name="map_icon()">
    <% content = self.content %>
    % if content.get('location'):
	##<a href="" class="map_popup">
	    <div class="media_icon">
		<img src="/images/misc/contenticons/map.png" />
	    </div>
	##</a>
	##<script>
	##    $('.map_popup').click(function() {
	##	$('#map-popup').modal({ onShow: function (dialog) {}});
	##	return false;
	##    });
	##</script>
	##${popup.popup_static('map', content_map, 'map-popup')}
    % endif
</%def>

##------------------------------------------------------------------------------
## Content Details
##------------------------------------------------------------------------------
<%def name="content_details()">
    <% content = self.content %>

    <div class="details" style="float: right;">
        
        <%def name="detail(field_name)">
            % if content.get(field_name):
            <p>${field_name}: ${content[field_name]}</p>
            % endif
        </%def>
        <%def name="format_date_if(title, date_input, fuzzy=True)">
          % if date_input:
            <tr>
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
            <td>Booms</td>
            <td>${content['boom_count'] if 'boom_count' in content else '0'}</td>
	    <td><span class="separator"></span></td>
            <td>Views</td>
            <td>${content['views'] if 'views' in content else '0'}</td>
          </tr>
        </table>
        <div class="padded">${rating()}</div>
        <div class="iconholder padded">
          ${iconify('private', 'Private Content', 'icon16 i_private')}
          ${iconify('closed', 'Closed', 'icon16 i_closed')}
          % if content.get('approval')=='approved':
            <div class="icon16 i_approved" title="approved"><span>Approved</span></div>${_("Approved")}
          % endif
          <span style="float: right;">${iconify('edit_lock', 'Locked for editing', 'icon16 i_edit_lock')}</span>
        </div>
    </div>
</%def>


##------------------------------------------------------------------------------
## Content Details Footer
##------------------------------------------------------------------------------
<%def name="content_details_foot()">
    <% content = self.content %>
    <div class="details" style="float: left;">
      <%def name="detail(field_name)">
          % if content.get(field_name):
          <p>${field_name}: ${content[field_name]}</p>
          % endif
      </%def>
        <%def name="format_date_if(title, date_input, fuzzy=True, trclass=None)">
          % if date_input:
            <tr${' class=%s' % trclass if trclass else ''}>
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
      ${h.literal(h.scan_for_embedable_view_and_autolink(self.content['content'], protocol=h.current_protocol(), size=(config['media.display.video.width'], config['media.display.video.height'])))}
    </div>
</%def>


##------------------------------------------------------------------------------
## Content Action Buttons
##------------------------------------------------------------------------------
<%def name="content_action_buttons()">
    <div style="padding-top: 20px;" class="acceptrequest">
	<table>
	    <tr>
		<td class="tip"></td>
		<td>
		## --- Publish -----------------------------------------------------------
		% if 'publish' in self.actions:
		    ${h.secure_link(
			h.args_to_tuple('content', id=self.id, format='redirect', submit_publish='publish') ,
			method = "PUT" ,
			css_class = 'button',
			value           = _('Publish') ,
			json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
			
		    )}
		% endif
      
		## --- Respond -----------------------------------------------------------
		% if 'respond' in self.actions:
		    ${h.secure_link(
			h.args_to_tuple('new_content', parent_id=self.id) ,
			css_class = 'button',
			value           = _("Share your story") ,
			json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , 
		    )}
		    ## AllanC the cb_frag creates a new fragment, data is the return fron the JSON call to the 'new_content' method
		    ##        it has to be done in javascript as a string as this is handled by the client side when the request complete successfully.
		% endif
		
<%doc>
	      ## --- Accept ------------------------------------------------------------
		% if 'accept' in self.actions:
		    ${h.secure_link(
			h.args_to_tuple('content_action', action='accept'  , format='redirect', id=self.id) ,
			css_class = '',##'button',
			value           = _('_Respond later') ,
			json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
		    )}
		    ##${h.secure_link(h.args_to_tuple('content_action', action='accept'  , format='redirect', id=id), value=_('Accept'),  css_class="icon16 i_accept")}
		% endif
		
	      
		## --- Withdraw ----------------------------------------------------------
		% if 'withdraw' in self.actions:
		    ${h.secure_link(
			h.args_to_tuple('content_action', action='withdraw', format='redirect', id=self.id) ,
			css_class = '',##'button',
			value           = _('Withdraw') ,
			json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
		    )}
		% endif
</%doc>
		</td>
		<td class="tip"><div>
		    <a href="" class="get-involved-popup">Why should you get involved?</a>
		    <script>
			$('.get-involved-popup').click(function() {
			    $('#get-involved').modal({ onShow: function (dialog) {}});
			    return false;
			});
		    </script>
		    ${popup.popup_static('Why get involved?', get_involved, 'get-involved')}
		</div></td>
	    </tr>
	</table>
    </div>
</%def>

##------------------------------------------------------------------------------
## License
##------------------------------------------------------------------------------

<%def name="content_license()">
    % if 'license' in self.content:
    <% license = self.content['license'] %>
    <div class="padded license" style="margin-top:14px">
      <a href="${license['url']}" target="_blank" rel="license" title="${license['description']}">
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
        # AllanC - now done by media/show.mako
        #media_width  = config['media.display.video.width' ]
        #media_height = config['media.display.video.height']
    %>
    <div class="media_container">
    
    ## Load the content carousel to display previews of all content media
    <span class="carousel">${media_includes.media_carousel(content['attachments'])}</span>
    
    <%doc>
    <ul id="media_carousel_content_${content['id']}" class="media_carousel">
    % for media in content['attachments']:
        <li>
            ${media_includes.preview(media)}
            <p>
            % if media.get('caption'):
                <span class="caption">${media['caption']}</span>
            % endif
            % if media.get('credit'):
                <span class="credit">(${_('Credit to')}: ${media['credit']})</span>
            % endif
            </p>
        </li>
    % endfor
    </ul>
    </%doc>
    
    </div>
    
    <%doc>
    <script type="text/javascript">
        ## http://sorgalla.com/projects/jcarousel/
        
        function media_carousel_content_${content['id']}_initCallback(carousel) {
            // future control options go here
        };
        
        jQuery(document).ready(function() {
            jQuery('#media_carousel_content_${content['id']}').jcarousel({
                wrap   : 'last' ,
                scroll : 1 ,
                visible: 1 ,
                initCallback: media_carousel_content_${content['id']}_initCallback,
            });
        });
    </script>
    </%doc>
    
</%def>

##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="content_map()">
    <% content = self.content %>
    % if content.get('location'):
	<%
	lon = content['location'].split(' ')[0]
	lat = content['location'].split(' ')[1]
	%>
	<p>
	${loc.minimap(
	    name=h.uniqueish_id("map", content['id']),
	    width="100%", height="200px",
	    lat = lat,
	    lon = lon,
	    feeds = [
		dict(pin='gold',    url='/contents.rss?location=%s,%s' % (lon,lat)      ),
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

<div class="comments">

    <table>
        <tr style="display: none;">
			<th>${_('Member')}</th>
			<th>${_('Comment')}</th>
			<th>${_('Actions')}</th>
		</tr>
	<tr>
	    <td colspan="3">
		<div class="comments-option">
		    % if c.logged_in_user:
		    ${_("Need more info on this request? ")}<span class="show-comments">Ask here...</span>
		    % else:
		    To comment on this content, please <a href="${url(controller='account', action='signin')}">sign up or log in!</a>
		    % endif
		</div>
	    </td>
	    <script>
		$(function() {
			$('.new-comment').hide();
			//$('.new-comment').css("display", "table-row");
			$('.show-comments').click(function() {
				$('.new-comment').toggle();
				$('.comment-${self.id}').focus();
			});
		});
	    </script>
	</tr>
        <tr class="new-comment">
            <td class="comment_avatar">
                % if c.logged_in_user:
                ${member_includes.avatar(c.logged_in_user.to_dict())}
                %endif
            </td>
            <td class="comment">
                % if c.logged_in_persona:
                ${h.form(h.args_to_tuple('contents', type='comment', parent_id=content['id'], format='redirect'), json_form_complete_actions="cb_frag_reload(current_element);" )}
                    ##% url("content",id=d['content']['id'])
                    ## AllanC: RAAAAAAAAAAAAR!!! cb_frag_reload($(this)); does not work, because $(this) for forms is not a jQuery object?! so we cant use .parents() etc .. WTF!!!
                    ##         so to get round this I just submit a string to the reload ... not happy!
                    ##         workaround - turns up higher up $(this) works ... so I put it in a variable called current_element that is accessible
                    ##<input type="hidden" name="parent_id" value="${d['content']['id']}">
                    <input type="hidden" name="title" value="Re: ${d['content']['title']}">
                    ##<input type="hidden" name="type" value="comment">
                    <textarea name="content" class="comment-${self.id}"></textarea><br />
                    <span class="commentcount-${self.id}" style="text-align: right; font-size: 120%;">${config['setting.content.max_comment_length']}</span><br />
                    Ask <b>${content['creator']['name']}</b> for more information about this request. Note: your question and/or answers will be publically visible.
		    If you want to share your story please use the "share your story" button above.<br />
                    <!--<br><input type="submit" name="submit_preview" value="Preview">-->
                    <br /><input type="submit" class="button" name="submit_response" value="${_('Ask')}">
                    <script type="text/javascript">
                        $(function () {
                            $('.comment-${self.id}').limit(${config['setting.content.max_comment_length']}, '.commentcount-${self.id}');
                        });
                    </script>
                ${h.end_form()}
                % else:
                <p>${_('Please login to comment')}
                % endif
            </td>
            <td>
                ##padding col for flag actions
            </td>
        </tr>
        % for comment in comments:
        <tr>
            <td class="comment_avatar">
                ${member_includes.avatar(comment['creator'])}
            </td>
            <td class="comment">
                <p class="comment_by"     >${comment['creator']['name']}</p>
                
                <p class="comment_content">${comment['content']}</p>
                
                <p style="float: right;">
                ##	${comment['creator']['name']}
                    ##${relation(comment['creator'], c.logged_in_persona, d['content']['creator'], 'text')} --
                	<i>${h.time_ago(comment['creation_date'])} ${_('ago')}</i>
                </p>
            </td>
            <td>
                ${popup.link(h.args_to_tuple('content_action', action='flag', id=comment['id']), title=_('Flag as') , class_='icon16 i_flag')}
            </td>
        </tr>
        % endfor
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

<%doc>    % if 'publish' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect', submit_publish='publish') ,
            method = "PUT" ,
            value           = _('Publish') ,
            value_formatted = h.literal("<span class='icon16 i_publish'></span>%s") % _('Publish') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        <span class="separtor"></span>
    % endif


    ## --- Respond -------------------------------------------------------------

    % if 'respond' in self.actions: #self.content['type'] != 'draft'
        ${h.secure_link(
            h.args_to_tuple('new_content', parent_id=self.id) ,
            value           = _("Respond") ,
            value_formatted = h.literal("<span class='icon16 i_respond'></span>%s") % _('Respond') ,
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
            value           = _('_Respond later') ,
            value_formatted = h.literal("<span class='icon16 i_accept'></span>%s") % _('Accept') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        ##${h.secure_link(h.args_to_tuple('content_action', action='accept'  , format='redirect', id=id), value=_('Accept'),  css_class="icon16 i_accept")}
        <span class="separtor"></span>
    % endif 
    
    % if 'withdraw' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='withdraw', format='redirect', id=self.id) ,
            value           = _('Withdraw') ,
            value_formatted = h.literal("<span class='icon16 i_withdraw'></span>%s") % _('Withdraw'),
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        <span class="separtor"></span>
    % endif</%doc>
    
    ## --- Boom ----------------------------------------------------------------
    
    % if 'boom' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='boom', format='redirect', id=self.id) ,
            value           = _('Boom') ,
            value_formatted = h.literal("<span class='icon16 i_boom'></span>%s") % _('Boom') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        <span class="separtor"></span>
    % endif
    
    ## --- Approve/Viewed/Dissacocite ------------------------------------------
    
    % if 'approve' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='approve', format='redirect', id=self.id),
            value           = _('Approve & Lock'),
            value_formatted = h.literal("<span class='icon16 i_approve'></span>%s") % _('Approve & Lock'),
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
            value_formatted = h.literal("<span class='icon16 i_seen'></span>%s") % _('Viewed'),
            title           = _("Mark this content as viewed") ,
            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    % if 'dissasociate' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='disassociate', format='redirect', id=self.id),
            value           = _('Disassociate') ,
            value_formatted = h.literal("<span class='icon16 i_dissasociate'></span>%s") % _('Disassociate'),
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
        ><span class="icon16 i_edit"></span>${_("Edit")}</a>
        <span class="separtor"></span>
    % endif

    % if 'delete' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect'),
            method = "DELETE",
            value           = _("Delete"),
            value_formatted = h.literal("<span class='icon16 i_delete'></span>%s") % _('Delete'),
            confirm_text    = _("Are your sure you want to delete this content?"),
            json_form_complete_actions = "cb_frag_reload(cb_frag_previous(current_element)); cb_frag_remove(current_element);", ## 'contents/%s' % self.id,
        )}
        <span class="separtor"></span>
    % endif


    % if 'aggregate' in self.actions:
        ##${share.janrain_social(self.content, 'janrain', class_='icon16 i_share')}
    % endif
    
    % if 'flag' in self.actions:
        <a href='' onclick="$('#flag_content').modal(); return false;" title='${_("Flag inappropriate content")}'><span class="icon16 i_flag"></span>Flag</a>
        <span class="separtor"></span>
    % endif
    
    ##% if self.content.get('location'):
    ##    ${parent.georss_link()}
    ##% endif

</%def>

##------------------------------------------------------------------------------
## Get involved
##------------------------------------------------------------------------------
<%def name="get_involved()">
    <div class="information" style="width: 35em;">
	<div class="popup-title">
	    Why should you get involved?
	</div>
	<div class="popup-message">
	    By sharing your story with <b>${self.content['creator']['name']}</b> as video, images or audio, you can:
	    <ol>
		<li>Get published</li>
		<li>Get recognition</li>
		<li>Make the news!</li>
	    </ol>
	</div>
	<div class="popup-tag-line">
	    Don't just read it. Feed it.
	</div>
    </div>
    <div class="popup-icons">
	<img src="/images/misc/shareicons/video_icon.png" />
	<img src="/images/misc/shareicons/camera_icon.png" />
	<img src="/images/misc/shareicons/audio_icon.png" />
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
