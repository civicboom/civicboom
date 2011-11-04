<%inherit file="/frag/common/frag.mako"/>

<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="loc"             file="/html/web/common/location.mako"   />
<%namespace name="member_includes" file="/html/web/common/member.mako"     />

<%!
    from webhelpers.html import HTML, literal
    share_url        = False
    rss_url          = False
    auto_georss_link = False
    
    frag_data_css_class = 'frag_content_edit' #content_form
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.content = d['content']
        self.id      = d['content']['id']
        self.actions = d.get('actions', [])
        
        self.type          = self.content['type']
        self.selected_type = self.type
        if self.type == 'draft':
            self.selected_type = self.content.get('target_type')
        
        self.attr.title     = _('Edit ') + _('_'+self.selected_type)
        self.attr.icon_type = 'edit'
        
        if self.selected_type == 'assignment':
            self.attr.help_frag = 'create_assignment'
        if self.selected_type == 'article':
            self.attr.help_frag = 'create_article'
        if self.selected_type == 'article' and self.content.get('parent'):
            self.attr.help_frag = 'create_response'
        
        ##if has_role_required('editor', c.logged_in_persona_role) # AllanC - humm .. is this needed? ['actions'] has a 'publish' thing in it?
    %>
</%def>

##------------------------------------------------------------------------------
## Edit Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_col fill">
        <div class="frag_list fill">
        ## Should be here but changes size of text editor
        ##<div class="frag_list_contents">
        <h1>
            % if self.content.get('parent'):
                ${_("You are responding to: %s") % self.content['parent']['title']}
            % elif self.selected_type == 'assignment':
                ${_("Ask for stories")}
            % elif self.selected_type == 'article':
                ${_("Post a story")}
            % endif
        </h1>

        ${h.form(
            h.args_to_tuple('content', id=self.id, format="redirect"),
            id           = 'edit_%s' % self.id,
            name         = "content",
            method       = 'PUT',
            multipart    = True,
            data         = dict(
                json_complete = "[ ['update', null, '%s'], ['update', ['%s','%s'] ] ]" %
                (url('content', id=self.id, format='frag', prompt_aggregate='True' if prompt_aggregate else ''),
                    url('content', id=self.id),
                    url('content', id=self.content['parent']['id']) if self.content.get('parent') else ''
                ),
            ),
            class_      = 'auto_save' if self.content['type'] == 'draft' else ''
        )}
            ${invalid_messages()}
            ## accordion can be set to fill parent, but we don't want /filled/, we want a little
            ## margin at top and bottom for title and buttons
            <div style="position: absolute; top: 2.5em; bottom: 5.5em; left: 1em; right: 1em;">
            <div id="accordion-${self.id}">
                <h3>Article Text</h3>
                <div>${base_content()}</div>
                <h3>Attach Media</h3>
                <div>${media()}</div>
                <h3>Set Location</h3>
                <div>${location()}</div>
                <h3>Advanced</h3>
                <div>
                    <table>
                    <tr><td></td></tr>
                    % if not self.content.get('parent'):
                        ${privacy()}
                    % endif
                    ${license()}
                    ${content_extra_fields()}
                    </table>
                </div>
            </div>
            </div>
            ${submit_buttons()}
        ${h.end_form()}
        <script>
        $(function() {
            $("#accordion-${self.id}").accordion({fillSpace: true, autoHeight: false});
        });
        </script>
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Actions
##------------------------------------------------------------------------------

<%def name="actions_specific()">
    ## AllanC - for now just use buttons at bottom
    ##<a href='' class="icon16 i_save"    onclick="$('#edit_${self.id} input.submit_draft').click(); return false;" title="${_('Save')}"            ><span>${_('Save')}            </span></a>
    ##<a href='' class="icon16 i_preview" onclick="$('#edit_${self.id} input.submit_draft').click(); return false;" title="${_('Save and Preview')}"><span>${_('Save and Preview')}</span></a>
    
    ##cb_frag_load($(this), '${h.url('content', id=self.id, format='frag')}');
</%def>

<%def name="actions_common()">
    % if self.id:
        <a class="link_update_frag"
            href="${h.url('content', id=self.id)}"
            data-frag="${h.url('content', id=self.id, format='frag')}"
            data-confirm="Are you sure you wish to discard changes?"
            data-confirm-yes="Yes. Discard"
            data-confirm-no="No. Take me back">
            <span class="icon16 i_close_edit"></span>Discard Changes and view
        </a>
        
        % if 'delete' in self.actions:
            ${h.secure_link(
                h.args_to_tuple('content', id=self.id, format='redirect'),
                method          = "DELETE",
                value           = _('Delete'),
                value_formatted ='<span class="icon16 i_delete"></span>%s' % _('Delete'),
                link_data       = dict(
                    confirm = _("Are you sure you want to delete this posting?"),
                    confirm_yes = _("Yes. Delete"),
                    confirm_no = _("No. Take me back!"),
                ),
            )}
        % endif
    % endif
</%def>

##------------------------------------------------------------------------------
## Display Utils
##------------------------------------------------------------------------------
<%def name="tooltip(text)">
    <span class="tooltip tooltip_icon"><span>${_(text)}</span></span>
</%def>

<%def name="form_instruction(text)">
    <p class="instuctions">${_(text)}</p>
</%def>

<%def name="invalid_messages()">
    <%doc>
        AllanC
        I was debating putting invalid fields net to each of the fields themselfs but decided to just list all errors in one place for now
        This form potentially needs reworking if we are going to have embedable forms in the future (feature #335)
    </%doc>

    ## testing
    ##<% d['invalid'] = dict(test='testing is the way to go', test2='testing is the way to go', test3='testing is the way to go') %>
    
    % if 'invalid' in d:
        <div class="invalid error">
        <p>${_('Invalid')}</p>
        % for key, value in d['invalid'].iteritems():
            <p><span>${key}</span>: ${value}</p>
        % endfor
        </div>
    % endif
</%def>

##------------------------------------------------------------------------------
## Base Form Text Content
##------------------------------------------------------------------------------
<%def name="base_content()">
    <table>
        <tr><td>
        </td></tr>
        <tr><td>
            <label for="title_${self.id}">${_('Add your story title')}</label>
            <input id="title_${self.id}" name="title" type="text" class="edit_input auto_save" value="${self.content['title']}" placeholder="${_('Enter a story title')}"/>
        </td></tr>
        <tr><td>
		<%
		area_id = h.uniqueish_id("content")
		%>
		<label for="${area_id}">${_("Add more detail and supporting links, etc")}</label>
		<textarea class="editor edit_input auto_save" name="content" id="${area_id}">${self.content['content']}</textarea>
        </td></tr>
        <tr><td>
            <label for="tags_${self.content['id']}">${_("Tags")}</label>
            <span>(${_('separated by commas')})</span>
            <%
            tags = []
            separator = config['setting.content.tag_string_separator']
            if   isinstance(self.content['tags'], list):
                tags = self.content['tags']
            elif isinstance(self.content['tags'], basestring):
                tags = self.content['tags'].split(separator)
                
            tags_string = u""
            for tag in tags:
                tags_string += tag + separator
            %>
            <input class="edit_input" name="tags_string" type="text" value="${tags_string}" id="tags_${self.content['id']}"/>
        </td></tr>
    </table>
</%def>


##------------------------------------------------------------------------------
## Media Upload and Editor
##------------------------------------------------------------------------------

<%def name="media()">
        <ul class="media_files">
            <li class="media_file" style="display: none;" id="mediatemplate">
              <div class="file_type_overlay icon"></div>
              <a href="#"><!--
                --><img id="media_thumbnail" class="media_preview" src="/images/media_placeholder.gif" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/><!--
              --></a>
              <div class="media_fields">
                  <span id="media_status" style="display: none">(status)</span>
                  <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="text" disabled="true" value=""   /><input type="submit" name="file_remove" value="Remove" class="file_remove icon16 i_delete"/></p>
                  <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text"                 value=""/></p>
                  <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text"                 value="" /></p>
              </div>
            </li>
            <!-- List existing media -->
            % for media in self.content['attachments']:
                <% id = media['id'] %>
                <li class="media_file ${'event_load' if app_globals.memcache.get(str("media_processing_"+media['hash'])) else ''}" data-json_url="${h.url('medium', id=media['hash'], format='json')}" data-id="${id}" data-hash="${media['hash']}" id="media_attachment_${id}">
                    <div class="file_type_overlay icon16 i_${media['type']}"></div>
                    <a href="${media['original_url']}">
                        <img id="media_thumbnail_${id}" class="media_preview" src="${media['thumbnail_url']}?0" alt="${media['caption']}" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/>
                    </a>
                    <span class="status" id="media_status_${id}" style="display: none">(status)</span>
                    
                    <div class="media_fields">
                        <p><label for="media_file_${id}"   >${_("File")}       </label><input id="media_file_${id}"    name="media_file_${id}"    type="text" disabled="true" value="${media['name']}"   /><input type="submit" name="file_remove_${id}" value="Remove" class="file_remove icon16 i_delete"/></p>
                        <p><label for="media_caption_${id}">${_("Caption")}    </label><input id="media_caption_${id}" name="media_caption_${id}" type="text"                 value="${media['caption']}"/></p>
                        <p><label for="media_credit_${id}" >${_("Credited to")}</label><input id="media_credit_${id}"  name="media_credit_${id}"  type="text"                 value="${media['credit']}" /></p>
                    </div>
                </li>
            % endfor
            <!-- End list existing media -->
            
            <!-- Add media -->
            <!-- Add media javascript - visible to JS enabled borwsers -->
            <li class="hide_if_nojs">
				<input id="file_upload" class="file_upload_uploadify" data-content_id="${self.id}" data-member_id="${c.logged_in_persona.id}" data-key="${c.logged_in_persona.get_action_key("attach to %d" % self.id)}" name="file_upload" type="file" />
            </li>
            
            <!-- Add media non javascript version - hidden if JS enabled -->
            <li class="hide_if_js">
                <div class="media_preview">
                    <div class="media_preview_none">${_("Select a file to upload")}</div>
                </div>
            <div class="media_fields">
                <p>
                    <label for="media_file"   >${_("File")}       </label>
                    <input id="media_file"    name="media_file"    type="file" class="field_file"/>
                    <input type="submit" name="submit_draft" value="${_("Upload")}" class="file_upload"/>
                </p>
                <p>
                    <label for="media_caption">${_("Caption")}    </label>
                    <input id="media_caption" name="media_caption" type="text" />
                    ${tooltip(_("extra_info"))}
                </p>
                <p>
                    <label for="media_credit" >${_("Credited to")}</label>
                    <input id="media_credit"  name="media_credit"  type="text" />
                    ${tooltip(_("extra_info"))}
                </p>
            </div>              
        </li>
        <!-- End Add media -->

        <a href="#" class="link_popup_next_element">Click here to record using your webcam / microphone</a>
        <div class="popup_element" style="display: none;">
        ${media_recorder()}
        </div>
##        ${popup.popup_static('Webcam Recorder', media_recorder, '', html_class="recorder-${self.id}")}
    </ul>
</%def>

##------------------------------------------------------------------------------
## Flash Media Recorder
##------------------------------------------------------------------------------

<%def name="media_recorder()">
    <p>${_('(Please note this is in beta, please use the feedback link at the bottom of the page if you experience any problems.)')}</p>
	<div class="media_recorder event_load" data-content_id="${self.id}" data-member_id="${c.logged_in_persona.id}" data-key="${c.logged_in_persona.get_action_key("attach to %d" % self.id)}" style="left:0px;width:360px;height:371px;">
</%def>

##------------------------------------------------------------------------------
## Content Extras
##------------------------------------------------------------------------------
<%def name="content_extra_fields()">
    <%doc>
        AllanC - Some content types have extra fields
                 Currently only assignment have extra fields
    </%doc>


    % if self.selected_type == 'assignment':
        <%
            due_date                      = str(self.content.get('due_date'  )                    or self.content.get('extra_fields',{}).get('due_date'  ) or '')[:16]
            event_date                    = str(self.content.get('event_date')                    or self.content.get('extra_fields',{}).get('event_date') or '')[:16]
            auto_publish_trigger_datetime = str(self.content.get('auto_publish_trigger_datetime')                                                          or '')[:16]
        %>
        <tr><td>
        <label for="due_date">${_("Due Date")}</label>
        <br><input class="detail" type="datetime" name="due_date"   value="${due_date}" />
        </td></tr>
        
        ##<span class="padded"><label for="event_date">${_("Event Date")}</label></span>
        ##<input class="detail" type="datetime" name="event_date" value="${event_date}">
        
        ## http://trentrichardson.com/examples/timepicker/
        % if self.content['type']=='draft' and c.logged_in_persona.has_account_required('plus'):
            <tr><td>
                <label for="auto_publish_trigger_datetime">${_("Automatically publish on")}</label>
                <br><input class="detail" type="datetime" name="auto_publish_trigger_datetime" value="${auto_publish_trigger_datetime}" />
            </td></tr>
        % endif
        
        <%doc>
        <p>${_("Response License:")}
        <table>
        <% from civicboom.lib.database.get_cached import get_licenses %>
        % for license in get_licenses():
            <tr>
            <%
                license_selected = ''
                if type == "assigment" and 'default_response_license' in self.content and license.id == self.content['default_response_license_id']:
                    license_selected = h.literal('checked="checked"')
            %>
            <td><input id="licence_${license.id}" type="radio" name="default_response_license_id" value="${license.id" ${license_selected} /></td>
            <td><a href="${license.url}" target="_blank" title="${_(license.name)}"><img src="/images/licenses/${license.id}.png" alt="${_(license.name)}"/></a></td>
            <td><label for="licence_${license.id}">${license.description}</label></td>
            </tr>
            ##${popup(_(license.description))}
        % endfor
        </table>
        </%doc>
    % endif
</%def>


##------------------------------------------------------------------------------
## Location
##------------------------------------------------------------------------------
<%def name="location()">
    <div style="padding-top: 1em; padding-bottom: 1em">
        ${loc.location_picker(field_name='location', always_show_map=True, width="100%", height="300px")}
    </div>
</%def>


##------------------------------------------------------------------------------
## License
##------------------------------------------------------------------------------
<%def name="license()">
<%doc>
    % if self.content['type'] == 'draft':
    <% from civicboom.lib.database.get_cached import get_licenses %>
    <!-- Licence -->
    <fieldset>
        <legend class="toggle_section"><span class="icon16 i_plus"></span>${_("Licence")}</legend>
        <div class="hideable">

            <span style="padding-top: 3px;">
              ${form_instruction(_("What is licensing explanation"))}
            </span>
			<table style="display: inline-block; padding-top: 3px;">
            % for license in get_licenses():
				<tr>
                <%
                  license_selected = ''
                  if 'license_id' in self.content and license.id == self.content['license_id']:
                      license_selected = h.literal('checked="checked"')
                %>
                <td><input id="licence_${license.id}" type="radio" name="licence" value="${license.id}" ${license_selected} /></td>
				<td><a href="${license.url}" target="_blank" title="${_(license.name)}"><img src="/images/licenses/${license.id}.png" alt="${_(license.name)}"/></a></td>
                <td><label for="licence_${license.id}">${license.description}</label></td>
				</tr>
                ##${popup(_(license.description))}
            % endfor
			</table>
              <div class="padded">This content will be published under the Creative Commons Attributed licence</div>
              <div class="padded">
                <a href="http://creativecommons.org/licenses/by/3.0/" target="_blank" title="Creative Commons Attribution"><img src="/images/licenses/CC-BY.png" alt="Creative Commons Attribution"/></a>
              </div>
        </div>
    </fieldset>
    % endif
</%doc>
    <tr><td>
        <label>License</label>
        <br>${_("This _content will be published under:")}
        <br><a href="http://creativecommons.org/licenses/by/3.0/" target="_blank" title="Creative Commons Attribution">Creative Commons Attributed License <img src="/images/licenses/CC-BY.png"/></a>
        ${what_now_link()}
    </td></tr>
</%def>


##------------------------------------------------------------------------------
## Privacy
##------------------------------------------------------------------------------

<%def name="privacy()">
	<%def name="selected(private, text='selected')">
		%if private == self.content.get('private'):
			${text}="${text}"
		%endif
	</%def>
	<tr class="${'' if c.logged_in_persona.has_account_required('plus') else 'setting-disabled'}">
        <td>
            <label>${_("Want to tell the world, or just a select few?")}</label>
            <br>${_("You can choose to make your content either <b>public</b> for anyone to see or <b>private</b> to you, your trusted followers and anyone you invite to respond to your request.")|n}
            
            % if not c.logged_in_persona.has_account_required('plus'):
                <div class="upgrade">
                    ${_('This requires a plus account. Please <a href="%s">upgrade</a> if you want access to this feature.') % (h.url(controller='about', action='upgrade_plans')) | n }
                </div>
            % endif
            
            <div class="padded">
                <div class="jqui-radios">
                    <input ${selected("False", "checked")} type="radio" id="private-false" name="private" value="False" /><label for="private-false">${_("Public")}</label>
                    <input ${selected("True", "checked")} type="radio" id="private-true" name="private" value="True" /><label for="private-true">${_("Private")}</label>
                </div>
                <script type="text/javascript">
                $(function() {
                    $('.jqui-radios').buttonset().removeClass('.jqui-radios');
                })
                </script>
            </div>
        </td>
    </tr>
</%def>


##------------------------------------------------------------------------------
## Submit button - form post buttons have special behaviour template
##------------------------------------------------------------------------------

## AllanC - note the class selectors are used by jQuery to simulate clicks
<%def name="submit_button(name, title_text=None, show_content_frag_on_submit_complete=False, prompt_aggregate=False, mo_text=None, mo_class='mo-help-r', onclick_js='')">
    <%
        button_id = "submit_%s_%s" % (name, self.id)
        if not title_text:
            title_text = _(name)
    %>

    % if mo_text:
        <span class="mo-help">
        <div class="${mo_class}">
            <h2>${title_text}</h2>
            <p>${_(mo_text)}</p>
        </div>
    % endif
            <input
                type    = "submit"
                id      = "${button_id}"
                name    = "submit_${name}"
                class   = "submit_${name} button"
                value   = "${title_text}"

            />
    % if mo_text:
        </span>
    % endif
</%def>



##------------------------------------------------------------------------------
## Submit buttons
##------------------------------------------------------------------------------
<%def name="submit_buttons()">
    <div style="font-size: 130%; text-align: center; padding: 1em; position: absolute; bottom: 0px; left: 0px; right: 0px;" class="buttons">
        ## Preview + Publish
        % if self.content['type'] == "draft":
            <span style="float: left; margin-left: 2em;">
                <span class="mo-help">
                    <div class="mo-help-r">
                        <h2>${_('Save draft')}</h2>
                        <p>${_("This _assignment will be saved to your profile for further editing prior to posting.")}</p>
                    </div>
                    <input class="button" type="submit" name="submit_draft" value="${_('Save draft')}" data-json-complete="[]" />
                </span>
            </span>
            <span class="mo-help">
                <div class="mo-help-r">
                    <h2>${_("Preview draft")}</h2>
                    <p>${_("See how it will look once it's been posted.")}</p>
                </div>
                <input class="button" type="submit" name="submit_preview" value="${_('Preview draft')}" data-json-complete="[['update', null, '${h.url('content', id=self.id, format='frag')}']]" />
            </span>
            ##${submit_button('preview', _("Preview draft"), show_content_frag_on_submit_complete=True, mo_text=_("See how it will look once it's been posted.") )}
            % if 'publish' in self.actions:
                <%
                    tooltip = "Ask the world!"
                    if self.selected_type == "article":
                        tooltip = "Tell the world!"
                %>
                <span style="float: right; margin-right: 2em;">
                    ##${submit_button('publish', _("Post"), show_content_frag_on_submit_complete=True, prompt_aggregate=True, mo_text=_(tooltip), mo_class="mo-help-l", onclick_js="$(this).parents('.buttons').children('.what-now-pop').modal({appendTo: $(this).parents('form')}); return false;" )}
                    <span class="mo-help">
                        <div class="mo-help-l">
                            <h2>${_("Post")}</h2>
                            <p>${_(tooltip)}</p>
                        </div>
                        <%
                            if self.selected_type == "assignment":
                                confirm_title = _("Once you post this request, it will appear:")
                                confirm_message = "<ol>" +\
                                    "<li>" + _("On your _Widget for your community to respond to") +"</li>" +\
                                    "<li>" + _("In all your _site_name followers' notification streams") +"</li>" +\
                                    "<li>" + _("On the _site_name request stream") +"</li>" +\
                                    "</ol>"
                            elif self.selected_type == "article":
                                if self.content.get("parent"):
                                    confirm_title = _("Once you share this story, it will:")
                                    confirm_message = "<ol>" +\
                                        "<li>" + (_("Be sent directly to %s") % self.content['parent'].get('creator', dict()).get('name')) + "</li>" +\
                                        "<li>" + _("Be listed as a response against the request") + "</li>" +\
                                        "<li>" + _("Appear in your followers' notification streams") + "</li>" +\
                                        "</ol>"
                                else:
                                    confirm_title = _("Once you post this story:")
                                    confirm_message = "<ol>" +\
                                        "<li>" + _("It will appear in your followers' notification streams.") + "</li>" +\
                                        "<li>" + _("You will also be able to share it on Facebook, LinkedIn and Twitter once you post.") + "</li>" +\
                                        "</ol>"
                        %>
                        <input type="submit" name="submit_publish" value="Post" class="button"
                            data-confirm="${confirm_message}"
                            data-confirm-title="${confirm_title}"
                            data-confirm-yes="${_('Yes. Post.')}"
                            data-confirm-no="${_('No. Take me back.')}"
                            data-confirm-avatar="true"
##                                                  update, this frag, with this content's view frag (prompt to aggregate.                     update, all frags with this content, and your profile
                            data-json-complete="[ ['update', null, '${h.url('content', id=self.id, format='frag', prompt_aggregate='True')}'], ['update',['${h.url('content', id=self.id)}', '/profile'], null, null] ]"
                        />
                    </span>
                </span>
            % endif
            
        ## Update
        % else:
            % if 'update' in self.actions:
            <input class="button" type="submit" name="submit_publish" value="${_('Update')}"
##                                      update, this frag, with this content's view frag.                update, all frags with this content
                data-json-complete="[ ['update', null, '${h.url('content', id=self.id, format='frag')}'], ['update','${h.url('content', id=self.id)}'] ]"
            >
            
            
            ##${submit_button('publish', _("Update") , show_content_frag_on_submit_complete=True )}
            % endif
            <a class="button link_update_frag"
                href="${h.url('content', id=self.id)}"
                data-frag="${h.url('content', id=self.id, format='frag')}"
                % if 'update' in self.actions:
                    data-confirm="Are you sure you wish to discard changes?"
                    data-confirm-title="${_('Discard changes and view')}"
                    data-confirm-yes="Yes. Discard"
                    data-confirm-no="No. Take me back"
                % endif
            >
                ${_("View Content")}
            </a>
        % endif
    </div>
</%def>

##------------------------------------------------------------------------------
## What happens now?
##------------------------------------------------------------------------------
## This is the popup for post confirmation

<%def name="what_now_link()">
</%def>

<%def name="what_now_popup()">
    <div class="information">
        <p>${member_includes.avatar(c.logged_in_persona)} <span style="font-size:250%; vertical-align: middle;">${c.logged_in_persona}</span></p>
        % if self.selected_type == "assignment":
        	<div class="popup-title">
        	    ${_("Once you post this request, it will appear:")}
        	</div>
        	<div class="popup-message">
        	    <ol>
                    <li>${_("On your _Widget for your community to respond to")}</li>
                    <li>${_("In all your _site_name followers' notification streams")}</li>
                    <li>${_("On the _site_name request stream")}</li>
        	    </ol>
        	</div>
        % elif self.selected_type == "article":
            % if self.content.get('parent'):
                <div class="popup-title">
                    ${_("Once you share this story, it will:")}
                </div>"
                <div class="popup-message">
                    <ol>
                        <li>${_("Be sent directly to")} ${self.content.get('parent',dict()).get('creator', dict()).get('name')}</li>
                        <li>${_("Be listed as a response against the request")}</li>
                        <li>${_("Appear in your followers' notification streams")}</li>
                    </ol>
                </div>
            % else:
                <div class="popup-title">
                    ${_("Once you post this story:")}
                </div>
                <div class="popup-message">
                    <ol>
                        <li>${_("It will appear in your followers' notification streams.")}</li>
                        <li>${_("You will also be able to share it on Facebook, LinkedIn and Twitter once you post.")}</li>
                    </ol>
                </div>
            % endif
        % endif
        <div style="font-size: 130%; text-align: center;">
            % if self.content['type'] == "draft":
                % if 'publish' in self.actions:
                <span >${submit_button('publish', _("Yes I want to Post!"), show_content_frag_on_submit_complete=True, prompt_aggregate=True)}</span>
                % endif
            % else:
                % if 'update' in self.actions:
                ${submit_button('publish', _("Update") , show_content_frag_on_submit_complete=True )}
                % endif
            % endif
        </div>
    </div>
</%def>
