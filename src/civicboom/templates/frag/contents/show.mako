<%inherit file="/frag/common/frag.mako"/>
<%!
    import datetime
    from webhelpers.html import HTML, literal
%>

<%namespace name="frag_lists"      file="/frag/common/frag_lists.mako"     />
<%namespace name="flag"            file="/frag/content_actions/flag.mako"  />
<%namespace name="share"           file="/frag/common/share.mako"          />
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="member_includes" file="/html/web/common/member.mako"     />
<%namespace name="media_includes"  file="/html/web/media/show.mako"        />
<%namespace name="components"       file="/html/web/common/components.mako" />
<%namespace name="edit"             file="edit.mako" />

## for deprication
<%namespace name="loc"             file="/html/web/common/location.mako"     />

<%!
    rss_url = True
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="custom_share()">
    <a href="#" ${share.janrain_social_call_content(self.content, 'existing' if c.logged_in_persona and c.logged_in_persona.username == self.content['creator']['username'] else 'other' , self.content['type'] if not self.content['parent'] else 'response')} class="icon16 i_share link_janrain"><span>Janrain</span></a> 
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
        
        def custom_share_line():
            popup.link(
                h.args_to_tuple(controller='misc', action='get_link_embed',type='content', id=self.id),
                title = _('Link or embed this content'),
                text  = h.literal("<span class='icon16 i_widget'></span>%s") % _('Link or embed'),
            )
        
        # Agregation dict
        if self.content['private'] == False and self.content['type'] != 'draft':
            self.attr.share_kwargs = {
                'url'               : h.url('content', id=self.id, qualified=True) ,
                'title'             : self.content.get('title') ,
                'summary'           : self.content.get('content_short') ,
                'image'             : self.content.get('thumbnail_url') ,
                'published'         : self.content.get('publish_date') ,
                'updated'           : self.content.get('update_date') ,
                'author'            : self.content.get('creator', dict()).get('name') ,
                'custom_share'      : custom_share,
                'custom_share_line' : custom_share_line,
            }
        
        # Help Frag
        self.attr.help_frag = self.content['type']
        if self.attr.help_frag == 'draft':
            self.attr.help_frag = 'create_'+self.content['target_type']
        
        # Manipulate Action List
        # - remove actions in exclude_actions kwarg
        if self.kwargs.get('exclude_actions'):
            if self.kwargs.get('exclude_actions') == 'all':
                self.actions = []
            else:
                self.actions = list(set(self.actions) - set(self.kwargs.get('exclude_actions', '').split(',')))
        
        self.attr.auto_georss_link = True
        
        # GregM: Removed popups as we have the janrain share popup now :D
        #if c.logged_in_persona and c.logged_in_persona.username == self.content['creator']['username'] and self.content['type']=='assignment' and not c.logged_in_user.config['help_popup_created_assignment']:
        #    self.attr.popup_url = url(controller='misc', action='help', id='created_assignment', format='frag')
        
        self.popup_link_class = "get-involved-popup-" + str(self.content['id'])
        self.popup_class      = "get-involved-" + str(self.content['id'])
    %>
</%def>

<%def name="invite_members_request()"> 
    <span class="mo-help">
        ${h.frag_link(value='', title='Invite Members', class_='icon16 i_plus_blue', href_tuple=h.args_to_tuple(controller='invite', action='index', id=self.id, invite='assignment'))}
        <div class="mo-help-l mo-help-b">
            ${_('Invite other members to participate in this request')}
        </div> 
    </span>
</%def>

##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    % if c.logged_in_persona and c.logged_in_persona.username == self.content['creator']['username'] and request.params.get('prompt_aggregate')=='True':
        <div class="link_janrain event_load" ${share.janrain_social_data_content(self.content, 'new', self.content['type'] if not self.content['parent'] else 'response')}></div>
    % endif
    ## --- redesign --- ##
    <div class="frag_top_row">
    <div class="frag_col">        
        % if self.content.get('parent'):
            ${frag_lists.content_list(self.content['parent'], _("This is a response to..."), creator=True)}
            ${response_guide()}
        % endif
        
        <div class="frag_list">
                <div class="frag_list_contents">
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
                    <div class="separator" style="padding: 10px;"></div>
                    % if self.attr.share_kwargs:
                        ${share.AddThisLine(**self.attr.share_kwargs)}
                    % endif
                    ${content_license()}
                    <div class="separator"></div>
                </div>
        </div>
    </div>
    </div>
    
    <div class="frag_col">
    ${frag_lists.content_list(
        d['responses'],
        _("Responses"),
        href=h.args_to_tuple('contents', response_to=self.id),
        creator=True
    )}
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
      <%doc>
        % if self.attr.share_kwargs:
            ${share.AddThisFragList(**self.attr.share_kwargs)}
        % endif
        </%doc>
        
        ##<h2>${_("Content by")}</h2>
        
        % if 'accepted_status' in d:
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='accepted'],
                _("Accepted by"),
            )}
            ${frag_lists.member_list_thumbnails(
                [m for m in d['accepted_status']['items'] if m['status']=='invited'],
                _("Invited"),
                hide_if_empty = not 'invite_to_assignment' in self.actions, # Always show this list if invite is avalable
                actions = invite_members_request if 'invite_to_assignment' in self.actions else None ,
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
    <table class="content_title_table">
        <tr>
            <td class="content_title">
                <h1>${self.content['title']}</h1>
            </td>
            <td rowspan="2" class="actions">
                ${content_title_actions()}
            </td>
        </tr>
        <tr>    
            <td class="creator_avatar">
                ${member_includes.avatar(self.content['creator'], class_="thumbnail_small")}
                ${_("By: ")} ${member_includes.member_link(self.content['creator'], rel='author')}
            </td>
        </tr>
        % if self.content.get('approval') == 'approved' and self.content.get('parent'):
        <tr>
            <td>
                <span class="icon32 i_approved"></span>${_("Approved by ")} ${member_includes.member_link(self.content['parent']['creator'])}
            </td>
        </tr>
        % endif
    </table>
</%def>

<%def name="content_title_actions()">
    % if 'edit' in self.actions:
        <a class="link_update_frag" href="${h.url('edit_content', id=self.id)}"
           data-frag="${h.url('edit_content', id=self.id, format='frag')}"
        ><span class="icon16 i_edit"></span>${_("Edit")}</a>
        <div class="separator"></div>
    % endif
    
    % if 'delete' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect'),
            method          = "delete",
            value           = _('Delete'),
            value_formatted ='<span class="icon16 i_delete"></span>%s' % _('Delete'),
            link_data       = dict(
                confirm = _("Are you sure you want to delete this posting?"),
                confirm_yes = _("Yes. Delete"),
                confirm_no = _("No. Take me back!"),
            ),
        )}
        <div class="separator"></div>
    % endif
    
    % if 'boom' in self.actions:
        <span class="mo-help">
            ${h.secure_link(
                h.args_to_tuple('content_action', action='boom', format='redirect', id=self.id) ,
                value           = _('Boom') ,
                value_formatted = h.literal("<span class='icon16 i_boom'></span>&nbsp;%s") % _('Boom') ,
                force_profile   = True,
            )}
            <div class="mo-help-l mo-help-b">
                ${_('Booming this content will recommend it to your followers and the rest of the community.')}
            </div>
        </span>
        <div class="separator"></div>
    % endif

    % if 'unboom' in self.actions:
        <span class="mo-help">
            ${h.secure_link(
                h.args_to_tuple('content_action', action='unboom', format='redirect', id=self.id) ,
                value           = _('Unboom') ,
                value_formatted = h.literal("<span class='icon16 i_boom'></span>&nbsp;%s") % _('Unboom') ,
                force_profile   = True,
            )}
            <div class="mo-help-l mo-help-b">
                ${_('UnBooming this content will remove it from your list of boomed content.')}
            </div>
        </span>
        <div class="separator"></div>
    % endif
    
    % if 'flag' in self.actions:
        <a href='' onclick="$('#flag_content').modal(); return false;" title='${_("Flag inappropriate content")}'><span class="icon16 i_flag"></span>&nbsp;Flag</a>
        <div class="separator"></div>
    % endif
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
    ##    $('#map-popup').modal({ onShow: function (dialog) {}});
    ##    return false;
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
        <table class="content">
          <tr>
            <td>${_("Booms")}</td>
            <td>${content['boom_count'] if 'boom_count' in content else '0'}</td>
        <td><span class="separator"></span></td>
            <td>${_("Views")}</td>
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
      <table class="content">
##        ${format_date_if('Created'  , content.get('creation_date'))}</p>
        ${format_date_if(_('Published'), content.get('publish_date' ))}</p>
        % if content.get('publish_date') != content.get('update_date'):
          ${format_date_if(_('Updated')  , content.get('update_date'  ))}</p>
        % endif
        ${format_date_if(_('Event Date'), content.get('event_date'), False, 'bold')}
        ${format_date_if(_('Due By')    , content.get('due_date'), False, 'bold'  )}
        % if content.get('tags'):
            <tr${' class=%s' % trclass if trclass else ''}>
                <td>${_('Tags')}</td>
                <td>${", ".join(content['tags'][:])}</td>
            </tr>
        % endif
      </table>
    </div>
</%def>

##------------------------------------------------------------------------------
## Content
##------------------------------------------------------------------------------

<%def name="content_content()">
    <div class="content_text">
      ${h.literal(h.scan_for_embedable_view_and_autolink(self.content['content'], protocol=h.current_protocol()))}
      ##size=(config['media.display.video.width'], config['media.display.video.height'])
    </div>
</%def>

##------------------------------------------------------------------------------
## Content Response button when content has parent (GregM)
##------------------------------------------------------------------------------
<%def name="respond_has_parent()">
    <%def name="li_story(title, content_dict)">
        <li>
            <h3>${title}:</h3>
            <p><b>${content_dict.get('title')}</b></p>
            <p>
                <div class="creator_avatar fl">
                   ${member_includes.avatar(content_dict['creator'])}
                </div>
                <div class="content_creator">${_("By: %s") % content_dict['creator']['name']}</div>
            </p>
            <div style="padding: 0.5em 0 1em 0;">
                ${h.secure_link(
                    h.args_to_tuple('new_content', parent_id=content_dict['id']) ,
                    link_class = 'button',
                    value     = _("Respond with your _content") ,
                    form_data = dict(
                        json_complete = "[['create', null, '%s']]" % h.url('content', id='{json_id}', format='frag'),
                    ),
    
                )}
            </div>
        </li>
    </%def>
    <div style="">
        <h2 class="hide_if_js">${_("Respond with your _content")}</h2>
        <h1 class="hide_if_nojs">${_("Great you want to share your _content...")}</h1>
        <p style="padding-bottom: 1em;">${_("Would you like to respond to:")}</p>
        <ul>
            ${li_story(_('The original request'), self.content.get('root_parent'))}
            ${li_story(_('This _article'), self.content)}
        </ul>
    </div>
    <div class="cb"></div>
    <div class="hide_if_nojs" style="padding-bottom: 6em;"></div>
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
        
            <%
                (confirm_title, confirm_message) = edit.module.publish_labels(self.content.get('target_type'), self.content, _)
#                (confirm_title, confirm_message) = (_(confirm_title), _(confirm_message))
            %>
            ${h.secure_link(
                h.args_to_tuple('content', id=self.id, format='redirect', submit_publish='publish'),
                method          = "put",
                value           = _('Post'),
                link_class      = 'button',
                parent_id       = self.content['parent']['id'] if self.content.get('parent') else None,
                link_data       = dict(
                    confirm         = confirm_message,
                    confirm_title   = confirm_title,
                    confirm_yes     = _('Yes. Post.'),
                    confirm_no      = _('No. Take me back.'),
                    confirm_avatar  = 'true',
                ),
                form_data       = dict(
                    json_complete   = "[ ['update', null, '%s'], ['update',['%s', '/profile'], null, null] ]" % (h.url('content', id=self.id, format='frag', prompt_aggregate='True'), h.url('content', id=self.id))
                ),

)}
        % endif
      
        ## --- Respond -----------------------------------------------------------
        % if 'respond' in self.actions:
            % if self.content.get('parent'):
                ${h.secure_link(
                    h.args_to_tuple('new_content', parent_id=self.id) ,
                    link_class  = 'button' ,
                    value       = _("Respond with your _content") ,
                    form_data   = dict(
                        json_complete = "[['create', null, '%s']]" % h.url('edit_content', id='{json_id}', format='frag'),
                    ) ,
                    link_data   = dict(
                        confirm = _("Would you like to respond to:"),
                        confirm_title = _("Great you want to share your _content..."),
                        confirm_secure_options = [
                            dict(
                                title=_('The original request'),
                                content='<p><b>%s</b></p><p><div class="creator_avatar fl"><div class="thumbnail"><img src="%s" alt="%s" class="img" onerror="this.onerror=null;this.src=\'/images/default/avatar_user.png\'" /></div></div><div class="content_creator">%s: %s</div></p>' % (self.content['root_parent']['title'], self.content['root_parent']['creator']['avatar_url'], self.content['root_parent']['creator']['username'], _('By'), self.content['root_parent']['creator']['name']),
                                json=h.url('new_content', parent_id=self.content['root_parent']['id'], format='json')
                            ) ,
                            dict(
                                title=_('This _content'),
                                content='<p><b>%s</b></p><p><div class="creator_avatar fl"><div class="thumbnail"><img src="%s" alt="%s" class="img" onerror="this.onerror=null;this.src=\'/images/default/avatar_user.png\'" /></div></div><div class="content_creator">%s: %s</div></p>' % (self.content['title'], self.content['creator']['avatar_url'], self.content['creator']['username'], _('By'), self.content['creator']['name']),
                                json=h.url('new_content', parent_id=self.id, format='json'))
                        ]
                    ) ,
                )}
##                <div class="hide_if_nojs">
##                    <a href="" onclick="$(this).parents('.hide_if_nojs').siblings('.hide_if_js').find('#popup_share').modal({appendTo: $(this).parents('table')}); return false;" class="button">${_("Respond with your _content")}</a>
##                </div>
##                <div class="hide_if_js">
##                    ${popup.popup_static(_('Respond with your _content'), respond_has_parent, 'popup_share')}
##                </div>
            % else:
                ${h.secure_link(
                    h.args_to_tuple('new_content', parent_id=self.id) ,
                    link_class = 'button',
                    value     = _("Respond with your _content") ,
                    form_data = dict(
                        json_complete = "[['create', null, '%s']]" % h.url('edit_content', id='{json_id}', format='frag'),
                    ),
                )}
            ## AllanC the cb_frag creates a new fragment, data is the return fron the JSON call to the 'new_content' method
            ##        it has to be done in javascript as a string as this is handled by the client side when the request complete successfully.
            % endif
        % endif
<%doc>

## GregM: These need updating to new frag links!!!
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
##            <a href="" class="${self.popup_link_class}">${_("Why should you get involved?")}</a>
##            <script>
##            $(".${self.popup_link_class}").click(function() {
##                $("#${self.popup_class}").modal({ onShow: function (dialog) {}});
##                return false;
##            });
##            </script>
##            ${popup.popup_static(_('Why get involved?'), get_involved, self.popup_class)}
            <a
                href="#"
                class="link_dummy"
                data-confirm-title="${_('Why get involved?')}"
                data-confirm="${_("By sharing your _content with <b>%s</b> as video, images or audio, you can:") % self.content['creator']['name'] | n}<ol><li>${_("Get published")}</li><li>${_("Get recognition")}</li><li>${_("Make the news!")}</li></ol>" data-confirm-title="Why should you get involved?"
                data-confirm-yes="OK, let's go!"
            >Why should you get involved?</a>

        </div></td>
        </tr>
    </table>
    </div>
</%def>

##------------------------------------------------------------------------------
## License
##------------------------------------------------------------------------------

<%def name="content_license()">
    ## BIG DIRTY HACK, changes cc urls for time being
    % if 'license' in self.content:
    <%
        license = self.content['license']
        if license['id'][:3] == 'CC-':
            d['content']['license']['url'] = 'http://www.creativecommons.org/licenses/' + license['id'][3:].lower() + '/3.0/'
    %>
    
    <%doc>
    <div class="frag_list" style="margin-top:14px">
        <h2>License</h2>
        <div class="frag_list_contents">
            <a href="${license['url']}" target="_blank" rel="license" title="${license['description']}">
                <img src="/images/licenses/${license['id']}.png" alt="${license['name']}" />
            </a>
        </div>
    </div>
    </%doc>
    
    <div class="license">
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
        
        # AllanC - now done by media/show.mako
        #media_width  = config['media.display.video.width' ]
        #media_height = config['media.display.video.height']
    %>
    <div class="media_container">
        ## Load the content carousel to display previews of all content media
        <span class="carousel">
            ${media_includes.media_carousel(content['attachments'], content['id'])}
        </span>
    </div>
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
        dict(pin='gold',    url='/contents.rss?sort=distance&location=%s,%s&limit=10' % (lon,lat)     , focus=True ),
        dict(pin='red',     url='/contents.rss?id=%s'          % content['id']              ),
        ],
        #controls=True
    )}
    </p>
    <!--
    <div id="map_key">
        <img src="/images/map-icons/marker-red.png"> This Article
        <img src="/images/map-icons/marker-gold.png"> Near-by articles
    </div>
    -->
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
                ${_("Need more info on this %s? ") % _(('_'+self.content['type'] if not self.content['parent'] else 'response'))}<span class="show-comments show-new-comments">${_("Ask here...")}</span>
            % else:
                ${_("To comment on this content, please")} <a href="${url(controller='account', action='signin')}">${_("sign up or log in!")}</a>
            % endif
        </div>
        </td>
    </tr>
        <tr class="new-comment hide_if_js">
            <td class="comment_avatar">
                % if c.logged_in_user:
                ${member_includes.avatar(c.logged_in_user.to_dict())}
                %endif
            </td>
            <td class="comment">
                % if c.logged_in_persona:
                ${h.form(h.args_to_tuple('contents', type='comment', parent_id=content['id'], format='redirect'), form_data = dict( json_complete = "[['update']]" ) )}
                    ##% url("content",id=d['content']['id'])
                    ## AllanC: RAAAAAAAAAAAAR!!! cb_frag_reload($(this)); does not work, because $(this) for forms is not a jQuery object?! so we cant use .parents() etc .. WTF!!!
                    ##         so to get round this I just submit a string to the reload ... not happy!
                    ##         workaround - turns up higher up $(this) works ... so I put it in a variable called current_element that is accessible
                    ##<input type="hidden" name="parent_id" value="${d['content']['id']}">
                    <input type="hidden" name="title" value="Re: ${d['content']['title']}">
                    ##<input type="hidden" name="type" value="comment">
                    <textarea name="content" class="comment-ta limit_length event_load"></textarea><br />
                    <span class="limit_length_remaining" style="text-align: right; font-size: 120%;">${config['setting.content.max_comment_length']}</span><br />
                    ${_('Ask <b>%(name)s</b> for more information about this %(type)s. Note: your question and/or answers will be publicly visible.') % dict(name=content['creator']['name'], type=_(('_'+self.content['type'] if not self.content['parent'] else 'response'))) | n}
                    
                    ${_("Need more info on this %s? ") % _(('_'+self.content['type'] if not self.content['parent'] else 'response'))}
                    
                    ${_('If you want to respond with your _content please use the "Respond with your _content" button above.')}<br />
                    <!--<br><input type="submit" name="submit_preview" value="Preview">-->
                    <br /><input type="submit" class="button" name="submit_response" value="${_('Ask')}">
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
                ##    ${comment['creator']['name']}
                    ##${relation(comment['creator'], c.logged_in_persona, d['content']['creator'], 'text')} --
                    <i>${h.time_ago(comment['creation_date'])} ${_('ago')}</i>
                </p>
            </td>
            % if c.logged_in_persona:
            <td>
                ${popup.link(h.args_to_tuple('content_action', action='flag', id=comment['id']), title=_('Flag as') , class_='icon16 i_flag')}
                
                % if 'moderator' in self.actions:
                    ${h.secure_link(
                        h.args_to_tuple('content_action', action='disassociate', format='redirect', id=comment['id']),
                        value           = _('disassociate'),
                        value_formatted ='<span class="icon16 i_delete"></span>',
                        title           = _("Remove this comment by %s" % comment['creator']['name']) ,
                        link_data       = dict(
                            confirm = _("Are you sure you want to disassociate this comment?"),
                            confirm_yes = _("Yes. Remove it"),
                            confirm_no  = _("No.  Take me back!"),
                        ),
                    )}
                % endif
            </td>
            % endif
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

<%def name="content_actions_specific()">

    ## --- Pubish --------------------------------------------------------------

<%doc>
    % if 'publish' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect', submit_publish='publish') ,
            method = "put" ,
            value           = _('Publish') ,
            value_formatted = h.literal("<span class='icon16 i_publish'></span>&nbsp;%s") % _('Publish') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" , BROKEN, needs new style frag link
        )}
        <span class="separtor">&nbsp;</span>
    % endif


    ## --- Respond -------------------------------------------------------------

    % if 'respond' in self.actions: #self.content['type'] != 'draft'
        ${h.secure_link(
            h.args_to_tuple('new_content', parent_id=self.id) ,
            value           = _("Respond") ,
            value_formatted = h.literal("<span class='icon16 i_respond'></span>&nbsp;%s") % _('Respond') ,
            json_form_complete_actions = h.literal(""" cb_frag(current_element, '/contents/'+data.data.id+'/edit.frag'); """)  , BROKEN, needs new style frag link
        )}
        ## AllanC the cb_frag creates a new fragment, data is the return fron the JSON call to the 'new_content' method
        ##        it has to be done in javascript as a string as this is handled by the client side when the request complete successfully.
        <span class="separtor">&nbsp;</span>
    % endif
    
    ## --- Accept / Withdraw ---------------------------------------------------
    
    % if 'accept' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='accept'  , format='redirect', id=self.id) ,
            value           = _('_Respond later') ,
            value_formatted = h.literal("<span class='icon16 i_accept'></span>&nbsp;%s") % _('Accept') ,
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" , BROKEN, needs new style frag link
        )}
        ##${h.secure_link(h.args_to_tuple('content_action', action='accept'  , format='redirect', id=id), value=_('Accept'),  css_class="icon16 i_accept")}
        <span class="separtor">&nbsp;</span>
    % endif 
    
    % if 'withdraw' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='withdraw', format='redirect', id=self.id) ,
            value           = _('Withdraw') ,
            value_formatted = h.literal("<span class='icon16 i_withdraw'></span>&nbsp;%s") % _('Withdraw'),
            json_form_complete_actions = "cb_frag_reload(current_element); cb_frag_reload('profile');" ,
        )}
        <span class="separtor">&nbsp;</span>
    % endif
</%doc>
    
    ## --- Boom ----------------------------------------------------------------
    
    % if 'boom' in self.actions:
        <span class="mo-help">
            ${h.secure_link(
                h.args_to_tuple('content_action', action='boom', format='redirect', id=self.id),
                value           = _('Boom'),
                value_formatted = "<span class='icon16 i_boom'></span>&nbsp;%s" % _('Boom') ,
                force_profile   = True,
            )}
            <div class="mo-help-r mo-help-b">
                ${_('Booming this content will recommend it to your followers and the rest of the community.')}
            </div>
        </span>
    

        <span class="separtor">&nbsp;</span>
    % endif
    
    ## --- Approve/Viewed/Dissacocite ------------------------------------------
    
    % if 'approve' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='approve', format='redirect', id=self.id),
            value           = _('Approve & _Lock'),
            value_formatted = "<span class='icon16 i_approved'></span>&nbsp;%s" % _('Approve & _Lock'),
            link_data = dict(
                confirm = "<p>" +\
                    _("When something is _locked and approved it means that you can use this for your needs (including commercial). It could be for your website, a newspaper, your blog so long as you credit the creator. Once you've _locked and approved it, no further changes can be made to the original _article by the creator. You can still contact them for more information.") +\
                    "</p><p>" +\
                    _("You will get an email explaining this in greater detail. The email will also give you access to the original file (if video, image or audio) to download and edit as you see fit - meaning your email file space is kept free.") +\
                    "</p>",
                confirm_yes = _('Yes. Approve and _lock'),
                confirm_no  = _('No. Take me back'),
                confirm_title = _("Approve and _Lock"),
            ),
            title           = _("Approve and _lock this content so no further editing is possible"),
        )}
##        ${h.secure_link(
##            h.args_to_tuple('content_action', action='approve', format='redirect', id=self.id),
##            value           = _('Approve & _Lock'),
##            value_formatted = h.literal("<span class='icon16 i_approved'></span>&nbsp;%s") % _('Approve & _Lock'),
##            title           = _("Approve and _lock this content so no further editing is possible"),
##            confirm_text    = _('Click OK to approve this. Once approved, no further changes can be made by the creator, and further details will be sent to your inbox.'),
##            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id ,
##            modal_params = dict(
##                title   = _('_Lock and approve this'),
##                message = HTML.p(_("When something is _locked and approved it means that you can use this for your needs (including commercial). It could be for your website, a newspaper, your blog so long as you credit the creator. Once you've _locked and approved it, no further changes can be made to the original story by the creator. You can still contact them for more information.") + HTML.p("You will get an email explaining this in greater detail. The email will also give you access to the original file (if video, image or audio) to download and edit as you see fit - meaning your email file space is kept free.")),
##                buttons = dict(
##                    yes = _('Yes. _Lock and approve'),
##                    no  = _('No. Take me back'),
##                ),
##                icon_image = '/images/misc/contenticons/lock.png',
##            ),
##        )}
        <span class="separtor">&nbsp;</span>
    % endif
    
    ## Seen action removed 
    <%doc>% if 'seen' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='seen'   , format='redirect', id=self.id),
            value           = _('Viewed') ,
            value_formatted = h.literal("<span class='icon16 i_seen'></span>&nbsp;%s") % _('Mark viewed'),
            title           = _("Mark this content as viewed") ,
            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id , BROKEN, needs new style frag link
            modal_params = dict(
                title   = 'Mark this as viewed',
                message = HTML.p('Use this to tell the contributor that you have viewed this content, but are not going to Lock and Approve it.'),
                buttons = dict(
                    yes = 'Yes. Mark as Viewed',
                    no  = 'No. Take me back',
                ),
                icon_image = '/images/misc/contenticons/view.png',
            ),
        )}
        <span class="separtor">&nbsp;</span>
    % endif</%doc>
    % if 'dissasociate' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content_action', action='disassociate', format='redirect', id=self.id),
            value           = _('_Disassociate') ,
            value_formatted = "<span class='icon16 i_disassociate'></span>&nbsp;%s" % _('_Disassociate'),
            link_data = dict(
                confirm = _('If you think that this post is not appropriate for your brand or audience, but does not break any terms and conditions, you can _disassociate it from your request. This means the content still "exists" on Civicboom but is not attached in any way to your request and will not be visible as a listed response to your request.'),
                confirm_yes = _('Yes. _Disassociate'),
                confirm_no = _('No. Take me back'),
                confirm_title = _('_Disassociate'),
            ),
            title           = _("_Disassociate your content from this response") ,
        )}
##        ${h.secure_link(
##            h.args_to_tuple('content_action', action='disassociate', format='redirect', id=self.id),
##            value           = _('_Disassociate') ,
##            value_formatted = h.literal("<span class='icon16 i_disassociate'></span>&nbsp;%s") % _('_Disassociate'),
##            title           = _("_Disassociate your content from this response") ,
##            confirm_text    = _('This content with no longer be associated with your content, are you sure?') ,
##            json_form_complete_actions = "cb_frag_reload('contents/%s');" % self.id ,
##            modal_params = dict(
##                title   = _('_Disassociate this post from your request'),
##                message = HTML.p(_('If you think that this post is not appropriate for your brand or audience, but does not break any terms and conditions, you can _disassociate it from your request. This means the content still "exists" on Civicboom but is not attached in any way to your request and will not be visible as a listed response to your request.')),
##                buttons = dict(
##                    yes = _('Yes. _Disassociate'),
##                    no  = _('No. Take me back'),
##                ),
##                icon_image = '/images/misc/contenticons/disassociate.png',
##            ),
##        )}
        <span class="separtor">&nbsp;</span>
    % endif
    
</%def>

<%def name="modal_dialog(title, message, buttons, icon=None, icon_image=None)">
    <div class="information popup-modal" style="width: 35em;">
        % if icon:
            <div class="popup-icon fr"><div class="icon_32 i_${icon}"></div></div>
        % elif icon_image:
            <div class="popup-icon fr"><img src="/images/${icon_image}.png" /></div>
        % endif
        <div class="popup-title">
            ${title}
        </div>
        <div class="popup-message">
            ${message | n}
        </div>
        % if buttons:
            <div class="popup-buttons">
                % for button in buttons:
                    ${button | n}
                % endfor
                <div class="cb"></div>
            </div>
        % endif
    </div>
</%def>


<%def name="content_actions_common()">
    
    % if 'edit' in self.actions:
        <a class="link_update_frag" href="${h.url('edit_content', id=self.id)}"
               data-frag="${h.url('edit_content', id=self.id, format='frag')}"
            ><span class="icon16 i_edit"></span>${_("Edit")}</a>
        <span class="separtor">&nbsp;</span>
    % endif

    % if 'delete' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect'),
            method          = "delete",
            value           = _('Delete'),
            value_formatted ='<span class="icon16 i_delete"></span>%s' % _('Delete'),
            link_data       = dict(
                confirm = _("Are you sure you want to delete this posting?"),
                confirm_yes = _("Yes. Delete"),
                confirm_no = _("No. Take me back!"),
            ),
        )}
        <span class="separtor">&nbsp;</span>
    % endif


    % if 'aggregate' in self.actions:
        ##${share.janrain_social(self.content, 'janrain', class_='icon16 i_share')}
    % endif
    
    % if 'flag' in self.actions:
        <a href='' onclick="$('#flag_content').modal(); return false;" title='${_("Flag inappropriate content")}'><span class="icon16 i_flag"></span>&nbsp;${_("Flag")}</a>
       <span class="separtor">&nbsp;</span>
    % endif
    
    ##% if self.content.get('location'):
    ##    ${parent.georss_link()}
    ##% endif

</%def>

##------------------------------------------------------------------------------
## Get involved
##------------------------------------------------------------------------------
<%def name="get_involved()">
    <div class="wrapper">
        <div class="information">
            <div class="popup-title">
                ${_("Why should you get involved?")}
            </div>
            <div class="popup-message">
                ${_("By sharing your _content with <b>%s</b> as video, images or audio, you can:") % self.content['creator']['name'] | n}
                <ol>
                    <li>${_("Get published")}</li>
                    <li>${_("Get recognition")}</li>
                    <li>${_("Make the news!")}</li>
                </ol>
            </div>
            <div class="popup-tag-line">
                ${_("_tagline")}
            </div>
        </div>
        <div class="popup-icons">
            <img src="/images/misc/shareicons/video_icon.png" />
            <img src="/images/misc/shareicons/camera_icon.png" />
            <img src="/images/misc/shareicons/audio_icon.png" />
        </div>
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
    <%
        license_id = d['content']['license']['id']
        if license_id[:3] == 'CC-':
            d['content']['license']['url'] = 'http://www.creativecommons.org/licenses/' + license_id[3:].lower() + '/3.0/'
    %>
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
        <form class="content_rating event_load" action="${url('content_action', action='rate', id=d['content']['id'], format='redirect')}" method="post" data-json="${url(controller='content_actions', action='rate', id=d['content']['id'], format='json')}">
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
        </li>
    % endif

</%def>


##------------------------------------------------------------------------------
## Response guide (this is a huge mess forgive me ;____;)
##------------------------------------------------------------------------------
<%def name="response_guide()">
    ##% if c.logged_in_persona and self.content.get('parent').get('creator').get('username') == c.logged_in_persona.username:
    ## AllanC - this is undeeded as this processing is done at the model level
    % if 'approve' in self.actions or 'dissasociate' in self.actions:
        <div class="guidance">
        % if c.logged_in_persona.has_account_required('plus'):
        ## --- Response guide ---
        
           <h1>${_("What now? You can:")}</h1>
           <div class="content response_guide">
               <table><tr><td style="width: 48%;">
                   % if 'approve' in self.actions:
                        ${h.secure_link(
                            h.args_to_tuple('content_action', action='approve', format='redirect', id=self.id),
                            value           = _('Approve & _Lock'),
                            value_formatted = h.literal("<table class=\"approve\"><tr><td class=\"int\">1.</td><td><p class=\"guidance_title\">"+_("_Lock it!")+"</p><p class=\"guidance_text\">"+_("Want to publish or use this content? Click here!")+"</p></td></tr></table>"),
                            link_data = dict(
                                confirm = '<p>' +\
                                    _("When something is _locked and approved it means that you can use this for your needs (including commercial). It could be for your website, a newspaper, your blog so long as you credit the creator. Once you've _locked and approved it, no further changes can be made to the original _article by the creator. You can still contact them for more information.") +\
                                    '</p><p>' +\
                                    _('You will get an email explaining this in greater detail. The email will also give you access to the original file (if video, image or audio) to download and edit as you see fit - meaning your email file space is kept free.') +\
                                    '</p>',
                                confirm_yes = _('Yes. Approve and _lock'),
                                confirm_no  = _('No. Take me back'),
                                confirm_title = _("Approve and _Lock"),
                            ),
                            title           = _("Approve and _lock this content so no further editing is possible"),
                        )}
                    % endif
                </td>
                <td style="width: 4%;"></td>
                <td>
                    % if 'dissasociate' in self.actions:
                        ${h.secure_link(
                            h.args_to_tuple('content_action', action='disassociate', format='redirect', id=self.id),
                            value           = _('_Disassociate') ,
                            value_formatted = h.literal("<table class=\"disassociate\"><tr><td class=\"int\">2.</td><td class=\"guidance_title\">"+_("Not appropriate or off brand?")+"</td></tr><tr><td></td><td class=\"guidance_text\">"+_("Click here to remove this from your list of responses!")+"</td></tr></table>"),
                            link_data = dict(
                                confirm = _('If you think that this post is not appropriate for your brand or audience, but does not break any terms and conditions, you can _disassociate it from your request. This means the content still "exists" on Civicboom but is not attached in any way to your request and will not be visible as a listed response to your request.'),
                                confirm_yes = _('Yes. _Disassociate'),
                                confirm_no = _('No. Take me back'),
                                confirm_title = _('_Disassociate'),
                            ),
                            title           = _("_Disassociate your content from this response") ,
                        )}
                    % endif
               </td></tr>
               <tr><td style="font-size: 80%;">
                    ${_("Pst! Or you can do nothing")}
               </tr></td></table>
           </div>
        
        ## Else No 'plus account'
        % else:
            <h1>${_("Upgrade your account:")}</h1>
            <div class="content response_guide">
                <p>${_("You could have the ability to moderate this content.")} <a href="${h.url(controller='misc', action='about', id='upgrade_plans')}">${_("Upgrade Now")}</a></p>
            </div>
        % endif
           <div style="clear: both;"></div>
        </div>
    % endif
</%def>
