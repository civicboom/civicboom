<%inherit file="/frag/common/frag.mako"/>

<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="loc"             file="/html/web/common/location.mako"   />
<%namespace name="member_includes" file="/html/web/common/member.mako"     />

<%!    
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
    <div class="frag_col">
        <div class="frag_list">
        <h1>
            % if self.content.get('parent'):
                ${_("You are responding to: %s") % self.content['parent']['title']}
            % elif self.selected_type == 'assignment':
                Post a request
            % elif self.selected_type == 'article':
                Post a story
            % endif
        </h1>
        <div class="separator"></div>
        
        <!-- Toggle Section -->
        <script type="text/javascript">
            var icon_more = 'icon_plus';
            var icon_less = 'icon_down';
            function toggle_edit_section(jquery_element) {
                $(jquery_element).next().slideToggle();
                var icon = $(jquery_element).find('.icon');
                if (icon.hasClass('icon_plus')) {
                    icon.removeClass(icon_more);
                    icon.addClass(icon_less);
                }
                else if (icon.hasClass(icon_less)) {
                    icon.removeClass(icon_less);
                    icon.addClass(icon_more);
                }
            }
        </script>
        
        
        
        ## pre_onsubmit is needed to save the contents of the TinyMCE component back to the text area
        ##  reference - http://www.dreamincode.net/forums/topic/52581-textarea-value-not-updating/
        ${h.form(
            h.args_to_tuple('content', id=self.id, format="redirect"),
            id           = 'edit_%s' % self.id,
            name         = "content",
            method       = 'PUT',
            multipart    = True,
            pre_onsubmit = "tinyMCE.triggerSave(true,true);",
            json_form_complete_actions = "json_submit_complete_for_%(id)s();" % dict(id=self.id)
        )}
            ## AllanC - whenthe AJAX submit it complete it will call the function below
            ##          The onclick event of the actual submit buttons can set a variable to direct the fragment refresh
            <script type="text/javascript">
                submit_complete_${self.id}_url = null;
                function json_submit_complete_for_${self.id}() {
                    if (submit_complete_${self.id}_url) {
                        ##cb_frag_load($('#edit_${self.id}'), submit_complete_${self.id}_url); ## Why update just this frag, if we set the frag source then it will be reloaded along with the reload of other frags with this content id
                        cb_frag_set_source($('#edit_${self.id}'), submit_complete_${self.id}_url);
                        submit_complete_${self.id}_url = null;
                        % if self.content.get('parent'):
                        cb_frag_reload(['contents/${self.id}','contents/${self.content['parent']['id']}']);
                        % else:
                        cb_frag_reload('contents/${self.id}');
                        % endif
                    }
                }
            </script>
            ${invalid_messages()}
            ${base_content()}
            ${media()}
            % if self.selected_type == 'assignment':
                ${content_type()}
            % endif
            ${location()}
            % if not self.content.get('parent'):
                ${privacy()}
            % endif
            ${tags()}
            ${submit_buttons()}
            ${license()}
        ${h.end_form()}
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
        <a href="${h.url('content', id=self.id)}"
           title="${_('Discard Changes and view')}"
           onclick="if (confirm('${_('View _content without saving your changes?')}')) {cb_frag_load($(this), '${h.url('content', id=self.id, format='frag')}');} return false;"
        ><span class="icon16 i_close_edit"></span>${_("Discard Changes and view")}</a>
        
        <span class="separtor"></span>
        
        % if 'delete' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect'),
            method="DELETE" ,
            value=_('Delete') ,
            value_formatted = h.literal("<span class='icon16 i_delete'></span>%s") % _('Delete'),
            confirm_text=_("Are your sure you want to delete this content?") ,
            #json_form_complete_actions = "cb_frag_remove($(this));" ,
            json_form_complete_actions = "cb_frag_reload('%s', current_element); cb_frag_remove(current_element);" % url('content', id=self.id),
            modal_params = dict(
                title='Delete posting',
                message='Are you sure you want to delete this posting?',
                buttons=dict(
                    yes="Yes. Delete",
                    no="No. Take me back!",
                )
            ),
        )}
        <span class="separtor"></span>
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
    <fieldset>
        ##<legend>${_("Content")}</legend>
        ##${form_instruction(_("Got an opinion? want to ask a question?"))}
        
        ##<p>
            <label for="title_${self.id}">${_('Add your title')}</label>
            <input id="title_${self.id}" name="title" type="text" class="edit_input" value="${self.content['title']}" placeholder="${_('Enter a title')}"/><br />
            ##${popup(_("extra info"))}
        ##</p>
        <div class="separator"></div>
        ##${YUI.richtext(c.content.content, width='100%', height='300px')}
		<%
		area_id = h.uniqueish_id("content")
		%>
		<label for="${area_id}">Add more detail and supporting links, etc</label>
		<textarea class="editor edit_input" name="content" id="${area_id}">${self.content['content']}</textarea>
        <!-- http://tinymce.moxiecode.com/ -->
        
		<script type="text/javascript">
			$(function() {
                tinyMCE.init({
                    mode     : "exact" ,
                    elements : "${area_id}" ,
                    theme    : "advanced" ,
                    theme_advanced_buttons1 : "bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,link,unlink",
                    theme_advanced_buttons2 : "",
                    theme_advanced_buttons3 : "",
                    theme_advanced_toolbar_location : "top",
                    theme_advanced_toolbar_align    : "left",
                });
			});
            function ajaxSave() {
                var ed = tinyMCE.get('${area_id}');
                ed.setProgressState(1); // Show progress spinner
                $.ajax({
                    type    : 'POST',
                    dataType: 'json',
                    url     : "${url('content', id=self.id, format='json')}",
                    data    : {
                        "_method": 'PUT',
                        "content": ed.getContent(),
                        "mode"   : 'autosave',
                        "_authentication_token": '${h.authentication_token()}'
                    },
                    success: function(data) {
                        ed.setProgressState(0);
                        flash_message(data);
                    },
                    error: function (jqXHR, status, error) {
                        ed.setProgressState(0);
                        flash_message({status:'error', message:'${_('Error automatically saving your content')}'});
                    },
                });
            }
            % if self.content['type'] == "draft":
            if (typeof cb_frag_get_variable($("#${area_id}"), 'autoSaveDraftTimer') != "undefined")
                clearInterval(cb_frag_get_variable($("#${area_id}"), 'autoSaveDraftTimer'));
            cb_frag_set_variable($("#${area_id}"), 'autoSaveDraftTimer', setInterval('ajaxSave()', 60000));
            % endif
		</script>
        <div class="separator"></div>
        ## Owner
        <%doc>
        <p><label for="owner">${_("By")}</label>
        <select name="owner">
            <%
            owners = []
            owners.append(c.logged_in_persona)
            # TODO - unfinished
            # AllanC - this is really odd! activating the hasattr triggers a query (im cool with that, it's expected) but an INSERT query?! that then errors?
            #if hasattr(c.logged_in_persona,"groups"):
            #    pass
            #owners += c.logged_in_persona.groups
            %>
            % for owner in owners:
                <%
                owner_selected = ""
                if owner.id == c.content.creator_id:
                    owner_selected = h.literal('selected="selected"')
                %>
                <option value="${owner.id}" ${owner_selected}>${owner.username}</option>
            % endfor
        </select>
        ${popup(_("extra_info"))}
        </p>
        </%doc>

    </fieldset>
    <div class="separator"></div>
</%def>

##------------------------------------------------------------------------------
## Tags
##------------------------------------------------------------------------------
<%def name="tags()">
    <fieldset>
        <label for="tags_${self.id}">${_("Tags")}</label>
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
        <input class="detail edit_input" id="tags_${self.id}" name="tags_string" type="text" value="${tags_string}"/>
        <span>(${_('separated by commas')} ',')</span>
        ##${popup(_("extra_info"))}
    </fieldset>
    <div class="separator"></div><div class="separator"></div>
</%def>

##------------------------------------------------------------------------------
## Media Upload and Editor
##------------------------------------------------------------------------------

<%def name="media()">
    <fieldset>
        <label>
            % if self.selected_type == 'assignment':
                Add media to help build a better request!
            % elif self.selected_type == 'article':
                Add media to help build a better story!
            % endif
        </label>
        <legend onclick="toggle_edit_section($(this));" class="edit_input">
            <span class="icon16 i_plus"></span>
            <img src="/images/misc/contenticons/media_trio.png" alt="Media" />
        </legend>
        <div class="hideable">
        ##${form_instruction(_("Add any relevent pictures, videos, sounds, links to your content"))}
        <div class="separator"></div>
        <ul class="media_files">
            <li class="media_file" style="display: none;" id="mediatemplate">
              <div class="file_type_overlay icon"></div>
              <a href="#"><!--
                --><img id="media_thumbnail" class="media_preview" src="/images/media_placeholder.gif" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/><!--
              --></a>
              <div class="media_fields">
                  <span id="media_status" style="display: none">(status)</span>
                  <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="text" disabled="true" value=""   /><input type="submit" onclick="return removeMedia($(this))" name="file_remove" value="Remove" class="file_remove icon16 i_delete"/></p>
                  <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text"                 value=""/></p>
                  <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text"                 value="" /></p>
              </div>
            </li>
            <!-- List existing media -->
            % for media in self.content['attachments']:
                <% id = media['id'] %>
                <li class="media_file" id="media_attachment_${id}">
                    <div class="file_type_overlay icon16 i_${media['type']}"></div>
                    <a href="${media['original_url']}"><!--
                        --><img id="media_thumbnail_${id}" class="media_preview" src="${media['thumbnail_url']}?0" alt="${media['caption']}" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/><!--
                    --></a>
					% if app_globals.memcache.get(str("media_processing_"+media['hash'])):
						<!-- Media still undergoing proceccesing -->
						## Clients without javascript could have the current status hard in the HTML text
						## TODO
						
						## Clients with    javascript can have live updates from the media controller
						<script type="text/javascript">
							updateMedia($('#media_attachment_${id}'), ${id}, ${media['hash']});
						</script>
						<!-- End media still undergoing proceccesing -->
					% endif
                    <span id="media_status_${id}" style="display: none">(status)</span>
                    
                    <div class="media_fields">
                        <p><label for="media_file_${id}"   >${_("File")}       </label><input id="media_file_${id}"    name="media_file_${id}"    type="text" disabled="true" value="${media['name']}"   /><input type="submit" onclick="return removeMedia($(this))" name="file_remove_${id}" value="Remove" class="file_remove icon16 i_delete"/></p>
                        <p><label for="media_caption_${id}">${_("Caption")}    </label><input id="media_caption_${id}" name="media_caption_${id}" type="text"                 value="${media['caption']}"/></p>
                        <p><label for="media_credit_${id}" >${_("Credited to")}</label><input id="media_credit_${id}"  name="media_credit_${id}"  type="text"                 value="${media['credit']}" /></p>
                    </div>
                </li>
            % endfor
            <!-- End list existing media -->
            
            <!-- Add media -->
            % if c.logged_in_user.username == "unittest" or ( self.content.get('parent') and self.content.get('parent').get('creator').get('username') == 'video-capture-beta-testers' ):
            <li class="hide_if_nojs">
            	${media_recorder()}
            </li>
            % endif
            
            <!-- Add media javascript - visible to JS enabled borwsers -->
            <li class="hide_if_nojs">
				<input id="file_upload" name="file_upload" type="file" />
				<script type="text/javascript">
				$(document).ready(function() {
						$('#file_upload').uploadify({
							'uploader'   : '/flash/uploadify.swf',
							'script'     : '/media',
							'scriptData' : {
								'content_id': ${self.id},
								'member_id' : ${c.logged_in_persona.id},
								'key'       : '${c.logged_in_persona.get_action_key("attach to %d" % self.id)}'
							},
							'cancelImg'  : '/images/cancel.png',
							'folder'     : '/uploads',
							'multi'      : true,
							'auto'       : true,
							'fileDataName':'file_data',
							'removeCompleted' : false,
							'onComplete'  : function(event, ID, fileObj, response, data) {
								//alert('There are ' + data.fileCount + ' files remaining in the queue.');
								// refresh the file list
								//Y.log("refresh the list now");
								refreshProgress($('form#edit_${self.id}'));
							}
							});
						});
				</script>
            </li>
            
            <!-- Add media non javascript version - hidden if JS enabled -->
            <li class="hide_if_js">
                <div class="media_preview">
                    <div class="media_preview_none">${_("Select a file to upload")}</div>
                </div>
                <div class="media_fields">
                    <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="file" class="field_file"/><input type="submit" name="submit_draft" value="${_("Upload")}" class="file_upload"/></p>
                    <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text" />${tooltip(_("extra_info"))}</p>
                    <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text" />${tooltip(_("extra_info"))}</p>
                </div>              
            </li>
            <!-- End Add media -->

        </ul>
        </div>
    </fieldset>
    <div class="separator"></div>
</%def>

##------------------------------------------------------------------------------
## Flash Media Recorder
##------------------------------------------------------------------------------
<%def name="media_recorder()">
	<script type="text/javascript">
		function cbFlashMedia${self.id}_DoFSCommand(command, args) {
			var args = args.split(',');
			if (command == 'flashresize') {
				aHeight = (args[0]*1)+5; 
				aWidth  = (args[1]*1)+14;
				$('#media_recorder_${self.id}').css('width', aWidth).css('height', aHeight);
			} else if (command == 'uploadcomplete') {
				refreshProgress($('form#edit_$(self.id}'));
			}
		}
		swfobject.embedSWF("https://bm1.civicboom.com:9443/cbFlashMedia.swf", "cbFlashMedia${self.id}", "100%", "100%", "9.0.0", "", {type:"v",host:"bm1.civicboom.com",user:"${c.logged_in_persona.id}",id:"${self.id}",key:"${c.logged_in_persona.get_action_key("attach to %d" % self.id)}"});
	</script>
	<div class="media_recorder" style="left:0px;width:360px;height:371px;" id="media_recorder_${self.id}">
		<div id="cbFlashMedia${self.id}">${_('If you see this text your browser is incompatible with our media recorder, please upload a video or audio file below')}</div>
	</div>
</%def>

##------------------------------------------------------------------------------
## Content Type
##------------------------------------------------------------------------------
<%def name="content_type()">
##    <fieldset>
##        <legend onclick="toggle_edit_section($(this));"><span class="icon16 i_plus"></span>${_("_%s Extras" % self.selected_type)}</legend>
##        <div class="hideable">

        
        <%
            type          = self.type
            selected_type = self.selected_type
            
            types = [
                #("draft"     , _("description of draft content")   ),
                ("article"   , _("description of _article")        ),
                ("assignment", _("description of _assignment")     ),
                ("syndicate" , _("description of syndicated stuff")),
            ]
        %>
        
        <%def name="type_option(type, description)">
            <%
                selected = ""
                if selected_type == type:
                    selected = h.literal('checked="checked"')
            %>
            <td id="type_${type}" onClick="highlightType('${type}');" class="section_selectable">
              <input class="hideable" type="radio" name="target_type" value="${type}" ${selected}/>
              <label for="type_${type}">${type}</label>
              <p class="type_description">${description}</p>
            </td>
        </%def>
        
        <%doc>
        % if type == "draft":
            <table id="type_selection"><tr>
            % for t in types:
                ${type_option(t[0],t[1])}
            % endfor
            <tr></table>
        % else:
            ${type}
        % endif
        </%doc>
            
    <fieldset>
        <label>Click here to set a deadline!</label>
        <legend onclick="toggle_edit_section($(this));" class="edit_input">
            <span class="icon16 i_plus"></span>
            <img src="/images/misc/contenticons/calendar.png" alt="Deadline" />
        </legend>
        <div class="hideable">
        <div class="separator"></div>
        <div id="content_type_additional_fields">
            ## See CSS for "active" class
            <div id="type_assignment_extras" class="hideable, additional_fields">
                <%
                    due_date   = str(self.content.get('due_date') or '')[:10]
                    event_date = str(self.content.get('event_date') or '')[:10]
                %>
                  <span class="padded"><label for="due_date">${_("Due Date")}</label></span>
                  <input class="detail" type="date" name="due_date"   value="${due_date}">
                  ##<span class="padded"><label for="event_date">${_("Event Date")}</label></span>
                  ##<input class="detail" type="date" name="event_date" value="${event_date}">
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
            </div>
        </div>


        <script type="text/javascript">
            // Reference: http://www.somacon.com/p143.php
            // set the radio button with the given value as being checked
            // do nothing if there are no radio buttons
            // if the given value does not exist, all the radio buttons are reset to unchecked
            function setCheckedValue(radioObj, newValue) {
                if(!radioObj) return;
                var radioLength = radioObj.length;
                if(radioLength == undefined) {
                    radioObj.checked = (radioObj.value == newValue.toString());
                    return;
                }
                for(var i = 0; i < radioLength; i++) {
                    radioObj[i].checked = false;
                    if(radioObj[i].value == newValue.toString()) {
                        radioObj[i].checked = true;
                    }
                }
            }
            
            function highlightType(type) {
                setCheckedValue(document.forms['content'].elements['target_type'], type); // Select radio button
                
                $('#type_selection .section_selectable').removeClass('section_selected');
                $('#type_'+type                        ).addClass(   'section_selected');
                
                $('#content_type_additional_fields .additional_fields').hide();
                $('#type_'+type+'_extras').show();
            }
            
            highlightType('${selected_type}'); //Set the default highlighted item to be the content type
        </script>
		##</div>
    ##</fieldset>
        </div>
    </fieldset>
    <div class="separator"></div>
</%def>


##------------------------------------------------------------------------------
## Location
##------------------------------------------------------------------------------
<%def name="location()">
    <!-- Licence -->
    <fieldset>
        <label>Add a location?</label>
        <legend onclick="toggle_edit_section($(this));" class="edit_input">
            <span class="icon16 i_plus"></span>
            <img src="/images/misc/contenticons/map.png" alt="Location" />
        </legend>
        <div class="hideable">
            <div class="separator"></div>
            ##${form_instruction(_("why give us this..."))}
			${loc.location_picker(field_name='location', always_show_map=True, width="100%")}
        </div>
    </fieldset>
    <div class="separator"></div>
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
        <legend onclick="toggle_edit_section($(this));"><span class="icon16 i_plus"></span>${_("Licence")}</legend>
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
    <span class="smaller"><a href="http://www.creativecommons.org" target="_blank" title="Creative Commons Attribution">View the Creative Commons license</a></span>
    ${what_now_link()}
    <div class="separator"></div>
</%def>


##------------------------------------------------------------------------------
## Privacy
##------------------------------------------------------------------------------
<%def name="privacy()">
    % if c.logged_in_persona.has_account_required('plus'):
	<%def name="selected(private, text='selected')">
		%if private == self.content.get('private'):
			${text}="${text}"
		%endif
	</%def>
    <fieldset>
        <label>Want to tell the world, or just a select few?</label>
        <legend onclick="toggle_edit_section($(this));" class="edit_input">
            <span class="icon16 i_plus"></span>
            <img src="/images/misc/contenticons/privacy.png" alt="Content Privacy" />
        </legend>
        <div class="hideable">
              <div class="padded">You can choose to make your ${_('_'+self.selected_type)} either public for anyone to see or private to you, your trusted followers and anyone you invite to respond to your request.</div>
              <div class="padded">
                  <div class="jqui-radios">
                      <input ${selected(False, "checked")} type="radio" id="private-false" name="private" value="False" /><label for="private-false">Public</label>
                      <input ${selected(True, "checked")} type="radio" id="private-true" name="private" value="True" /><label for="private-true">Private</label>
                  </div>
                  <script type="text/javascript">
                    $(function() {
                        $('.jqui-radios').buttonset().removeClass('.jqui-radios');
                    })
                  </script>
##                <select id="private" name="private">
##                    <option ${selected(False)} value="False">Public</option>
##                    <option ${selected(True)} value="True">Private</option>
##                </select>
              </div>
        </div>
    </fieldset>
    <div class="separator"></div>
    % endif
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
                onclick = "
                    % if onclick_js:
                        ${onclick_js}
                    % else:
                        ## AllanC - use the same disabling button technique with class's used in helpers.py:secrure_link to stop double clicking monkeys
                        
                        ## If button enabled
                        if (!$(this).hasClass('disabled_filter')) {
                            ## Disable this button
                            $(this).addClass('disabled_filter');
                            
                            ## Fake that a static submit button has been pressed
                            ##  - Standard HTML forms contain the name and value of the submit button pressed
                            ##  - JS Form submissions do not - this add's a fake input to the final submission to mimic this submit press
                            add_onclick_submit_field($(this));
                            
                            ## AllanC - I dont like the fact we start setting global var's here ... could we move to cb_frag.js:cb_frag_set_variable() ??
                            % if show_content_frag_on_submit_complete:
                                ## AllanC - Cleaner suggestion? - could this prompt aggregate be part of the python URL gen and not an appended string?
                                submit_complete_${self.id}_url = '${url('content', id=self.id, format='frag')}${'?prompt_aggregate=True' if prompt_aggregate else ''}';
                            % endif
                            
                            ## Re-enable button after 1 second
                            setTimeout(function() {$(this).removeClass('disabled_filter');}, 1000);
                            
                            ## Reload parent on post if publishing
                            ## AllanC - this was a nice idea - but the POST has not completed at this point and race hazzards occour
                            ##            if this is going to be used it needs to be at the end of the onsubmit event
                            ##% if name=='publish' and self.content.get('parent'):
                            ##    cb_frag_reload('${url('content', id=self.content['parent']['id'])}', $(this));
                            ##% endif
                        }
                        ## If button disabled - abort submit by returning false
                        else {
                            return false;
                        }
                    % endif
                "
            />
    % if mo_text:
        </span>
    % endif
</%def>



##------------------------------------------------------------------------------
## Submit buttons
##------------------------------------------------------------------------------
<%def name="submit_buttons()">

    <div style="font-size: 130%; text-align: center;" class="buttons">
        
        ${popup.popup_static('What happens now?', what_now_popup, '', html_class="what-now-pop")}
        
        ## Preview + Publish
        % if self.content['type'] == "draft":
            <span style="float: left; margin-left: 2em;">${submit_button('draft'  , _("Save draft"), mo_text=_("This _assignment will be saved to your profile for further editing prior to posting.") )}</span>
            ${submit_button('preview', _("Preview draft"), show_content_frag_on_submit_complete=True, mo_text=_("See how it will look once it's been posted.") )}
            % if 'publish' in self.actions:
            <span style="float: right; margin-right: 2em;">${submit_button('publish', _("Post"), show_content_frag_on_submit_complete=True, prompt_aggregate=True, mo_text=_("Ask the world!"), mo_class="mo-help-l", onclick_js="$(this).parents('.buttons').children('.what-now-pop').modal({appendTo: $(this).parents('form')}); return false;" )}</span>
            % endif
            
        ## Update
        % else:
            % if 'update' in self.actions:
            ${submit_button('publish', _("Update") , show_content_frag_on_submit_complete=True )}
            % endif
            <a class="button" href="${h.url('content', id=self.id)}" onclick="cb_frag_load($(this), '${url('content', id=self.id)}') return false;">${_("View Content")}</a>
        % endif
        
    </div>
    <div class="separator"></div><div class="separator"></div>
</%def>

##------------------------------------------------------------------------------
## What happens now?
##------------------------------------------------------------------------------
## This is the popup for post confirmation

<%def name="what_now_link()">
</%def>

<%def name="what_now_popup()">
    <div class="information">
        <p>${member_includes.avatar(c.logged_in_persona)} ${c.logged_in_persona}</p>
        % if self.selected_type == "assignment":
        	<div class="popup-title">
        	    ${_("Once you post this request, it will appear:")}
        	</div>
        	<div class="popup-message">
        	    <ol>
                    <li>${_("On your _Widget for your community to respond to")}</li>
                    <li>${_("In all your _site_name follower's notification stream")}</li>
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
                        <li>${_("Appear in your follower's notification stream")}</li>
                    </ol>
                </div>
            % else:
                <div class="popup-title">
                    ${_("Once you post this story:")}
                </div>
                <div class="popup-message">
                    <ol>
                        <li>${_('It will appear in your follower's notification stream.')}</li>
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
