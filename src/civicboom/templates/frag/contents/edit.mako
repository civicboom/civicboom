<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/html/web/common/location.mako" />

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
        
    %>
</%def>

##------------------------------------------------------------------------------
## Edit Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">

    <div class="frag_col">
        
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
        
        % if self.content.get('parent'):
            <p>${_("Responding to: %s") % self.content['parent']['title']}</p>
        % endif
        
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
            ${base_content()}
            ${content_type()}
            ${media()}
            ${location()}
            ${license()}
			${submit_buttons()}
        ${h.end_form()}
    </div>
</%def>

##------------------------------------------------------------------------------
## Actions
##------------------------------------------------------------------------------

<%def name="actions_specific()">
    ## AllanC - for now just use buttons at bottom
    ##<a href='' class="icon icon_save"    onclick="$('#edit_${self.id} input.submit_draft').click(); return false;" title="${_('Save')}"            ><span>${_('Save')}            </span></a>
    ##<a href='' class="icon icon_preview" onclick="$('#edit_${self.id} input.submit_draft').click(); return false;" title="${_('Save and Preview')}"><span>${_('Save and Preview')}</span></a>
    
    ##cb_frag_load($(this), '${h.url('content', id=self.id, format='frag')}');
</%def>

<%def name="actions_common()">
    % if self.id:
        <a href="${h.url('content', id=self.id)}"
           class="icon icon_close_edit"
           title="${_('Discard Changes and view')}"
           onclick="if (confirm('${_('View _content without saving your changes?')}')) {cb_frag_load($(this), '${h.url('content', id=self.id, format='frag')}');} return false;"
        ><span>${_("Discard Changes and view")}</span></a>
        
        ${h.secure_link(
            h.args_to_tuple('content', id=self.id, format='redirect'),
            method="DELETE" ,
            value="" ,
            title=_("Delete") ,
            css_class="icon icon_delete" ,
            confirm_text=_("Are your sure you want to delete this content?") ,
            json_form_complete_actions = "cb_frag_remove($(this));" ,
        )}
    % endif
</%def>

##------------------------------------------------------------------------------
## Display Utils
##------------------------------------------------------------------------------
<%def name="popup(text)">
<span class="tooltip tooltip_icon"><span>${_(text)}</span></span>
</%def>

<%def name="form_instruction(text)">
<p class="instuctions">${_(text)}</p>
</%def>

##------------------------------------------------------------------------------
## Base Form Text Content
##------------------------------------------------------------------------------
<%def name="base_content()">
    <fieldset>
        ##<legend>${_("Content")}</legend>
        ##${form_instruction(_("Got an opinion? want to ask a question?"))}
        
        ##<p>
            <label for="title_${self.id}"><h2>${_('Title')}</h2></label><input id="title_${self.id}" name="title" type="text" value="${self.content['title']}" style="width:100%;" placeholder="${_('Enter a title')}"/>
            ##${popup(_("extra info"))}
        ##</p>
        
        ##${YUI.richtext(c.content.content, width='100%', height='300px')}
		<%
		area_id = h.uniqueish_id("content")
		%>
		<label for="${area_id}"><h2>Content</h2></label>
		<textarea name="content" id="${area_id}" style="width:100%; height:250px;">${self.content['content']}</textarea>
        <!-- http://tinymce.moxiecode.com/ -->
        
		<script type="text/javascript">
			$(function() {
                tinyMCE.init({
                    mode     : "exact" ,
                    elements : "${area_id}" ,
                    theme    : "advanced" ,
                    theme_advanced_buttons1 : "bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,undo,redo,link,unlink",
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
                    url     : "${url('formatted_content', id=self.id, format='json')}",
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
                });
            }
            % if self.content['type'] == "draft":
            if (typeof cb_frag_get_variable($("#${area_id}"), 'autoSaveDraftTimer') != "undefined")
                clearInterval(cb_frag_get_variable($("#${area_id}"), 'autoSaveDraftTimer'));
            cb_frag_set_variable($("#${area_id}"), 'autoSaveDraftTimer', setInterval('ajaxSave()', 60000));
            % endif
		</script>

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
        
        
        ## Tags

        <p>
            <label style="display: inline-block; width: 50pt;" for="tags_${self.id}">${_("Tags")}</label>
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
            <input style="width: 100pt;" id="tags_${self.id}" name="tags_string" type="text" value="${tags_string}"/>
            <span>(${_('separated by commas')} ',')</span>
            ##${popup(_("extra_info"))}
        </p>

    </fieldset>
</%def>

##------------------------------------------------------------------------------
## Media Upload and Editor
##------------------------------------------------------------------------------

<%def name="media()">
    <fieldset>
        <legend onclick="toggle_edit_section($(this));"><span class="icon icon_plus"></span>${_("Media")}</legend>
        <div class="hideable">
        ##${form_instruction(_("Add any relevent pictures, videos, sounds, links to your content"))}
        
        <ul class="media_files">
            <li class="media_file" style="display: none;" id="mediatemplate">
              <div class="file_type_overlay icon"></div>
              <a href="#">
                <img id="media_thumbnail" class="media_preview" src="/images/media_placeholder.gif" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/>
              </a>
              <div class="media_fields">
                  <span id="media_status" style="display: none">(status)</span>
                  <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="text" disabled="true" value=""   /><input type="submit" name="file_remove" value="Remove" class="file_remove icon icon_delete"/></p>
                  <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text"                 value=""/></p>
                  <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text"                 value="" /></p>
              </div>
            </li>
            <!-- List existing media -->
            % for media in self.content['attachments']:
                <% id = media['id'] %>
                <li class="media_file" id="media_attachment_${id}">
                    <div class="file_type_overlay icon icon_${media['type']}"></div>
                    <a href="${media['original_url']}">
                        <img id="media_thumbnail_${id}" class="media_preview" src="${media['thumbnail_url']}?0" alt="${media['caption']}" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/>
                        
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
                    </a>
                    <span id="media_status_${id}" style="display: none">(status)</span>
                    
                    <div class="media_fields">
                        <p><label for="media_file_${id}"   >${_("File")}       </label><input id="media_file_${id}"    name="media_file_${id}"    type="text" disabled="true" value="${media['name']}"   /><input type="submit" name="file_remove_${id}" value="Remove" class="file_remove icon icon_delete"/></p>
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
								'content_id': ${self.id},
								'member_id' : ${c.logged_in_persona.id},
								'key'       : '${c.logged_in_persona.get_action_key("attach to %d" % c.content.id)}'
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
								Y.log("refresh the list now");
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
                    <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text" />${popup(_("extra_info"))}</p>
                    <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text" />${popup(_("extra_info"))}</p>
                </div>              
            </li>
            <!-- End Add media -->

        </ul>
        </div>
    </fieldset>
</%def>

##------------------------------------------------------------------------------
## Content Type
##------------------------------------------------------------------------------
<%def name="content_type()">
##    <fieldset>
##        <legend onclick="toggle_edit_section($(this));"><span class="icon icon_plus"></span>${_("_%s Extras" % self.selected_type)}</legend>
##        <div class="hideable">

        
        <%
            type          = self.type
            selected_type = self.selected_type
            
            types = [
                #("draft"     , _("description of draft content")   ),
                ("article"   , _("description of _article")        ),
                ("assignment", _("description of _assignemnt")     ),
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

        <div id="content_type_additional_fields">
            ## See CSS for "active" class
            <div id="type_assignment_extras" class="hideable, additional_fields">
                <%
                    due_date   = str(self.content.get('due_date') or '')[:10]
                    event_date = str(self.content.get('event_date') or '')[:10]
                %>
                <span>
                  <span style="display: inline-block; width: 50pt;">${_("Due Date:")}</span>
                  <input style="width: 100pt;" type="date" name="due_date"   value="${due_date}">
                </span>
                <span>
                  <span style="display: inline-block; width: 50pt;">${_("Event Date:")}</span>
                  <input style="width: 100pt;" type="date" name="event_date" value="${event_date}">
                </span>
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
</%def>


##------------------------------------------------------------------------------
## Location
##------------------------------------------------------------------------------
<%def name="location()">
    <!-- Licence -->
    <fieldset>
        <legend onclick="toggle_edit_section($(this));"><span class="icon icon_plus"></span>${_("Location")}</legend>
        <div class="hideable">
            ##${form_instruction(_("why give us this..."))}
			${loc.location_picker(field_name='location', always_show_map=True, width="100%")}
        </div>
    </fieldset>
</%def>


##------------------------------------------------------------------------------
## License
##------------------------------------------------------------------------------
<%def name="license()">

    % if self.content['type'] == 'draft':
    <% from civicboom.lib.database.get_cached import get_licenses %>
    <!-- Licence -->
    <fieldset>
        <legend onclick="toggle_edit_section($(this));"><span class="icon icon_plus"></span>${_("Licence selection")}</legend>
        <div class="hideable">
            <%doc>
            ${form_instruction(_("What is licensing explanation"))}
			<table>
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
            </%doc>
        
            <p>This content will be published under the Creative Commons Attributed licence</p>
            <a href="http://www.creativecommons.org" target="_blank" title="Creative Commons Attribution"><img src="/images/licenses/CC-BY.png" alt="Creative Commons Attribution"/></a>
        </div>
    </fieldset>
    % endif

    

</%def>


##------------------------------------------------------------------------------
## Submit buttons
##------------------------------------------------------------------------------
<%def name="submit_buttons()">
    <div style="text-align: right;">
        % if self.content['type'] == "draft":
			## AllanC - note the class selectors are used by jQuery to simulate clicks
			<input
                type    = "submit"
                name    = "submit_draft"
                class   = "button submit_draft"
                value   = "${_("Save")}"
                onclick = "add_onclick_submit_field($(this));"
            />
			<input
                type    = "submit"
                name    = "submit_preview"
                class   = "button submit_preview"
                value   = "${_("Preview")}"
                onclick = "add_onclick_submit_field($(this)); submit_complete_${self.id}_url='${url('content', id=self.id, format='frag')}';"
            />            
            <input
                type    = "submit"
                name    = "submit_publish"
                class   = "button"
                value   = "${_("Publish")}"
                onclick = "add_onclick_submit_field($(this)); submit_complete_${self.id}_url='${url('content', id=self.id, format='frag')}';"
            />
        % else:
            <input
                type    = "submit"
                name    = "submit_publish"
                class   = "button"
                value   = "${_("Update")}"
                onclick = "add_onclick_submit_field($(this)); submit_complete_${self.id}_url='${url('content', id=self.id, format='frag')}';"
            />
			<a class="button" href="${h.url('content', id=self.id)}" onclick="cb_frag_load($(this), '${url('content', id=self.id)}') return false;">${_("View Content")}</a>
        % endif
    </div>
</%def>

