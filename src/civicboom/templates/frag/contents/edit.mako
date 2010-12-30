<%inherit file="/frag/common/frag.mako"/>

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
        self.attr.title     = _('Edit')
        self.attr.icon_type = 'edit'
        
        self.content = d['content']
        self.id      = d['content']['id']
    %>
</%def>

##------------------------------------------------------------------------------
## Edit Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">

    <div class="frag_col">
        
        % if 'parent' in self.content:
            <p>${_("Responding to: %s") % self.content['parent']['title']}</p>'
        % endif
        
        ## AllanC - TODO need to update h.form() to accept url as a tuple for AJAX submission
        ${h.form(url('content', id=c.content.id, format="redirect"), method='PUT', multipart=True, name="content")}
            ${base_content()}
            ${media()}
            ##${content_type()}
            ##${location()}
            ##${license()}
			${submit_buttons()}
        ${h.end_form()}
    </div>
</%def>

##------------------------------------------------------------------------------
## Actions
##------------------------------------------------------------------------------
<%def name="actions_common()">
    % if d['content'].get('id'):
        ${h.secure_link(h.args_to_tuple('content', id=d['content'].get('id'), format='redirect'), method="DELETE", value="", title=_("Delete"), css_class="icon icon_delete", confirm_text=_("Are your sure you want to delete this content?") )}
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
    <fieldset><legend>${_("Content")}</legend>
        ${form_instruction(_("Got an opinion? want to ask a question?"))}

        <p>
            <label for="title">${_("Title")}</label>
            <input id="title" name="title" type="text" value="${self.content['title']}" style="width:80%;"/>
            ${popup(_("extra info"))}
        </p>
  
        ##${YUI.richtext(c.content.content, width='100%', height='300px')}
		<textarea name="content" id="content" style="width:100%; height:300px;">${self.content['content']}</textarea>'
        <script type="text/javascript" src ="/javascript/tiny_mce/tiny_mce.js"></script>
		<script type="text/javascript">
		tinyMCE.init({
			mode : "textareas",
			theme : "advanced",
			theme_advanced_buttons1 : "bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,undo,redo,link,unlink",
			theme_advanced_buttons2 : "",
			theme_advanced_buttons3 : "",
			theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
		});
		function ajaxSave() {
			var ed = tinyMCE.get('content');
			ed.setProgressState(1); // Show progress spinner
			$.ajax({
				type    : 'POST',
				dataType: 'json',
				url     : "${url('formatted_content', id=c.content.id, format='json')}",
				data    : {
                    "_method"     : 'PUT',
					"content": ed.getContent(),
					"mode"        : 'autosave',
                    "_authentication_token": '${h.authentication_token()}'
                    ##"upload_key": '${c.content_media_upload_key}',
				},
				success: function(data) {
					ed.setProgressState(0);
					flash_message(data);
				},
			});
		}
        % if self.content['type'] == "draft":
		var autoSaveDraftTimer = setInterval('ajaxSave()', 60000);
        % endif
		</script>

        % if self.content['type'] == "draft":
            <input type="submit" name="submit_draft"   value="${_("Save Draft")}"   style="float: right;"/>
        % endif

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
            <label for="tags">${_("Tags")}</label>
            <%
            tag_string = u""
            for tag in [tag.name for tag in c.content.tags]:
                tag_string += tag + u" "
            %>
            <input id="tags" name="tags" type="text" value="${tag_string}"/>
            ${popup(_("extra_info"))}
        </p>

    </fieldset>
</%def>

##------------------------------------------------------------------------------
## Media Upload and Editor
##------------------------------------------------------------------------------

<%def name="media()">

    <fieldset><legend>${_("Attach Media (optional)")}</legend>      
        ${form_instruction(_("Add any relevent pictures, videos, sounds, links to your content"))}
        
        <ul class="media_files">
            
            <!-- List existing media -->
            % for media in self.content['attachments']:
                <% id = media['id'] %>
                <li>
                    <div class="file_type_overlay icon icon_${media['type']}"></div>
                    <a href="${media['original_url']}">
                        <img id="media_thumbnail_${id}" class="media_preview" src="${media['thumbnail_url']}?0" alt="${media['caption']}" onerror='this.onerror=null;this.src="/images/media_placeholder.gif"'/>
                        
                        % if app_globals.memcache.get(str("media_processing_"+media['hash'])):
                            <!-- Media still undergoing proceccesing -->
                            ## Clients without javascript could have the current status hard in the HTML text
                            ## TODO
                            
                            ## Clients with    javascript can have live updates from "get_media_processing_staus"
                            <script type="text/javascript">
                                function updateMedia${id}() {
                                    $.getJSON(
                                        "${url(controller='media', action='get_media_processing_staus', id=media['hash'], format='json')}",
                                        processingStatus${id}
                                    );
                                }
                                function processingStatus${id}(data) {
                                    _status = data.data.status;
                                    /*alert("Status got = "+_status);*/
                                    if(!_status) {
                                        clearInterval(media_thumbnail_timer_${id});
                                        /*alert("processing complete reload the image!!!");*/
                                        $("#media_thumbnail_${id}").src = "${media['thumbnail_url']}" + "?" + (new Date().getTime());
                                        $("#media_status_${id}").text("");
                                    }
                                    else {
                                        $("#media_status_${id}").text(_status);
                                    }
                                }
                                var media_thumbnail_timer_${id} = setInterval('updateMedia${id}()', 5000);
                            </script>
                            <!-- End media still undergoing proceccesing -->
                        % endif
                    </a>
                    <span id="media_status_${id}" style="display: none">(status)</span>
                    
                    <div class="media_fields">
                        <p><label for="media_file_${id}"   >${_("File")}       </label><input id="media_file_${id}"    name="media_file_${id}"    type="text" disabled="true" value="${media['name']}"   /><input type="submit" name="file_remove_${id}" value="Remove" class="file_remove"/></p>
                        <p><label for="media_caption_${id}">${_("Caption")}    </label><input id="media_caption_${id}" name="media_caption_${id}" type="text"                 value="${media['caption']}"/></p>
                        <p><label for="media_credit_${id}" >${_("Credited to")}</label><input id="media_credit_${id}"  name="media_credit_${id}"  type="text"                 value="${media['credit']}" /></p>
                    </div>
                </li>
            % endfor
            <!-- End list existing media -->
            
            <!-- Add media -->
            
            <!-- Add media javascript - visable to JS enabled borwsers -->
            <li class="hide_without_js">
                Javascript/Flash uploader goes here
                ##% if c.content.id:
                ##<li>
                    ##${YUI.file_uploader()}
                ##</li>
                ##% endif
            </li>
            
            <!-- Add media non javascript version - hidden if JS enabled -->
            <li class="hideable">
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
        
    </fieldset>

</%def>


##------------------------------------------------------------------------------
## Submit buttons
##------------------------------------------------------------------------------
<%def name="submit_buttons()">
    <div style="text-align: right;">
    
        % if self.content['type'] == "draft":
        <input type="submit" name="submit_preview" value="${_("Preview Draft")}"/>
        <input type="submit" name="submit_draft"   value="${_("Save Draft")}"   />
        % else:
        <a href="${h.url('content', id=self.id)}">${_("View Content")}</a>
        % endif
    
    </div>
</%def>

