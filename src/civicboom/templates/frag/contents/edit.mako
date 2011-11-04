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
                        ## Why update just this frag, if we set the frag source then it will be
                        ## reloaded along with the reload of other frags with this content id
                        ##cb_frag_load($('#edit_${self.id}'), submit_complete_${self.id}_url);
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
        ${h.confirmed_link(
            _('Discard Changes and view'),
            icon='close_edit',
            href=h.url('content', id=self.id),
            modal_params = dict(
                title   = 'Discard changes',
                message = HTML.p('You are about to discard any changes you have made, are you sure you wish to continue?'),
                buttons = dict(
                    yes = 'Yes. Discard',
                    no  = 'No. Take me back',
                ),
                icon_image = '/images/misc/contenticons/disassociate.png',
            ),
        )}
        
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
            <input id="title_${self.id}" name="title" type="text" class="edit_input" value="${self.content['title']}" placeholder="${_('Enter a story title')}"/>
        </td></tr>
        <tr><td>
		<%
		area_id = h.uniqueish_id("content")
		%>
		<label for="${area_id}">${_("Add more detail and supporting links, etc")}</label>
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
                        "title"  : $('#title_${self.id}').val(),
                        ## AllanC - it may be possible to autosave other fields here, however, caution,
                        ## what happens if a user is half way through editing a date and the autosave
                        ## kicks in and the validators fire?. This needs testing issue #698
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
        <%doc>
        ## Owner
        <tr><td>
            <label for="owner">${_("By")}</label>
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
        </td></tr>
        </%doc>
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
                        updateMedia(${id}, '${media['hash']}', $('#media_attachment_${id}'));
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
        <!-- Add media javascript - visible to JS enabled borwsers -->
        <li class="hide_if_nojs">
            <input id="file_upload" name="file_upload" type="file" />
            <script type="text/javascript">
            $(document).ready(function() {
                    $('#file_upload').uploadify({
                        'uploader'   : '/flash/uploadify.swf',
                        'script'     : '/media',
                        'scriptData' : {
                            'content_id': '${self.id}',
                            'member_id' : '${c.logged_in_persona.id}',
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
            <a href="#" onclick="$('#recorder-${self.id}').modal(); return false;">Record from Webcam</a>
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

        <div id="recorder-${self.id}" style="display: none;">
        ${media_recorder()}
        </div>
##        ${popup.popup_static('Webcam Recorder', media_recorder, '', html_class="recorder-${self.id}")}
    </ul>
</%def>

##------------------------------------------------------------------------------
## Flash Media Recorder
##------------------------------------------------------------------------------
<%def name="media_recorder()">
    ## AllanC - A horrible temp close button
    <a href='' title='${_('Close pop-up')}' class="simplemodalClose icon16 i_delete" style="float:right;"><span>Close</span></a>
    
    <p>${_('(Please note this is in beta, please use the feedback link at<br>the bottom of the page if you experience any problems.)')|n}</p>
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
		swfobject.embedSWF("https://bm1.civicboom.com:9443/api_flash_server/cbFlashMedia.swf", "cbFlashMedia${self.id}", "100%", "100%", "9.0.0", "", {type:"v",host:"bm1.civicboom.com",user:"${c.logged_in_persona.id}",id:"${self.id}",key:"${c.logged_in_persona.get_action_key("attach to %d" % self.id)}"}, {wmode: "window"});
	</script>
	<div class="media_recorder" style="width:360px; height:371px;" id="media_recorder_${self.id}">
		<div id="cbFlashMedia${self.id}">${_('If you see this text your browser is incompatible with our media recorder, please upload a video or audio file below')}</div>
	</div>
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
                            
                            ## GrrrrregM: Damn this is annoying, we need to check if we're in a modal box & close if we are.
                            var popup = $(this).parents('#simplemodal-data');
                            if (popup.length > 0) {
                                $.modal.close();
                            }
                            
                            ## AllanC - I dont like the fact we start setting global var's here ... could we move to cb_frag.js:cb_frag_set_variable() ??
                            % if show_content_frag_on_submit_complete:
                                ## AllanC - Cleaner suggestion? - could this prompt aggregate be part of the python URL gen and not an appended string?
                                submit_complete_${self.id}_url = '${url('content', id=self.id, format='frag')}${'?prompt_aggregate=True' if prompt_aggregate else ''}';
                            % endif
                            
                            ## Re-enable button after 1 second
                            setTimeout(function (elem){elem.removeClass('disabled_filter');}, 1000, $(this));
                            
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
    <div style="font-size: 130%; text-align: center; padding: 1em; position: absolute; bottom: 0px; left: 0px; right: 0px;" class="buttons">
        ${popup.popup_static('What happens now?', what_now_popup, '', html_class="what-now-pop")}
        
        ## Preview + Publish
        % if self.content['type'] == "draft":
            <span style="float: left;">${submit_button('draft'  , _("Save draft"), mo_text=_("This _assignment will be saved to your profile for further editing prior to posting.") )}</span>
            ${submit_button('preview', _("Preview draft"), show_content_frag_on_submit_complete=True, mo_text=_("See how it will look once it's been posted.") )}
            % if 'publish' in self.actions:
                <%
                    tooltip = "Ask the world!"
                    if self.selected_type == "article":
                        tooltip = "Tell the world!"
                %>
                <span style="float: right;">${submit_button('publish', _("Post"), show_content_frag_on_submit_complete=True, prompt_aggregate=True, mo_text=_(tooltip), mo_class="mo-help-l", onclick_js="$(this).parents('.buttons').children('.what-now-pop').modal({appendTo: $(this).parents('form')}); return false;" )}</span>
            % endif
            
        ## Update
        % else:
            % if 'update' in self.actions:
            ${submit_button('publish', _("Update") , show_content_frag_on_submit_complete=True )}
            % endif
            <a class="button" href="${h.url('content', id=self.id)}" onclick="cb_frag_load($(this), '${url('content', id=self.id)}') return false;">${_("View Content")}</a>
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
