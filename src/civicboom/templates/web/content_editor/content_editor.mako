<%inherit file="/web/common/html_base.mako"/>

<%namespace name="YUI" file="/web/common/YUI_components.mako" />
<%namespace name="loc" file="/web/common/location.mako" />

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Edit _article")}</%def>


##------------------------------------------------------------------------------
## Additional CSS and Javascripts
##------------------------------------------------------------------------------
<%def name="head_links()">
  ${parent.head_links()}
  <script type="text/javascript" src ="/javascript/tiny_mce/tiny_mce.js"></script>
  <link   type="text/css"        href="/styles/common/content_editor.css" rel="stylesheet" />
</%def>


##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
<%def name="styleOverides()">
  .section_selectable {border: 1px solid transparent;}
  .section_selected   {border: 1px solid black; background-color: #ccc;}
</%def>





##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">

    ${parent_preview()}

    <div class="content_form">
        ${h.form(url('content', id=c.content.id, format="redirect"), method='PUT', multipart=True, name="content")}
            ${base_content()}
            ${media()}
            ${content_type()}
            ${location()}
            ${license()}
			${submit_buttons()}
        ${h.end_form()}
        
        % if c.content.id:
          ${h.form(url('content', id=c.content.id), method="DELETE")}
            <input type="submit" name="submit_delete"  value="${_("Delete")}"/>
          ${h.end_form()}
        % endif

    </div>
    
</%def>


##------------------------------------------------------------------------------
## Popup
##------------------------------------------------------------------------------
<%def name="popup(text)">
<span class="tooltip tooltip_icon"><span>${_(text)}</span></span>
</%def>

<%def name="form_instruction(text)">
<p class="instuctions">${_(text)}</p>
</%def>


##------------------------------------------------------------------------------
## Parent Preview
##------------------------------------------------------------------------------
<%def name="parent_preview()">
    % if c.content.parent:
        <p>Responding to: ${c.content.parent.title}</p>
    % endif
</%def>

##------------------------------------------------------------------------------
## Base Form Text Content
##------------------------------------------------------------------------------
<%def name="base_content()">
    <fieldset><legend>${_("Content")}</legend>
        ${form_instruction("Got an opinion? want to ask a question?")}

        <p>
            <label for="title">${_("Title")}</label>
            <input id="title" name="title" type="text" value="${c.content.title}" style="width:80%;"/>
            ${popup("extra info")}
        </p>
  
        ##${YUI.richtext(c.content.content, width='100%', height='300px')}
		<textarea name="content" id="content" style="width:100%; height:300px;">${c.content.content}</textarea>
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
				url     : "${url('content', id=c.content.id, format='json')}",
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
        % if c.content.__type__ == "draft":
		var autoSaveDraftTimer = setInterval('ajaxSave()', 60000);
        % endif
		</script>

        % if c.content.__type__ == "draft":
            <input type="submit" name="submit_draft"   value="Save Draft"   style="float: right;"/>
        % endif

        ## Owner
        <p><label for="owner">${_("By")}</label>
        <select name="owner">
            <%
            owners = []
            owners.append(c.logged_in_user)
            # TODO - unfinished
            # AllanC - this is really odd! activating the hasattr triggers a query (im cool with that, it's expected) but an INSERT query?! that then errors?
            #if hasattr(c.logged_in_user,"groups"):
            #    pass
            #owners += c.logged_in_user.groups
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
        ${popup("extra_info")}
        </p>
        
        
        ## Tags
        <p>
            <label for="tags">${_("Tags")}</label>
            <%
            tag_string = u""
            for tag in [tag.name for tag in c.content.tags]:
                tag_string += tag + u" "
            %>
            <input id="tags" name="tags" type="text" value="${tag_string}"/>
            ${popup("extra_info")}
        </p>

    </fieldset>
</%def>




##------------------------------------------------------------------------------
## Media Upload and Editor
##------------------------------------------------------------------------------

<%def name="media()">

    <fieldset><legend>${_("Attach Media (optional)")}</legend>      
        ${form_instruction("Add any relevent pictures, videos, sounds, links to your content")}
        
        <ul class="media_files">

            <!-- List existing media -->
            % for media in c.content.attachments:
            <li>
                <div class="file_type_overlay icon_${media.type}"></div>
                <a href="${media.original_url}">
                    <img id="media_thumbnail_${media.id}" class="media_preview" src="${media.thumbnail_url}" alt="${media.caption}"/>
                    
                    % if app_globals.memcache.get(str("media_processing_"+media.hash)):
                        <!-- Media still undergoing proceccesing -->
                        ## Clients without javascript could have the current status hard in the HTML text
                        ## TODO
                        
                        ## Clients with    javascript can have live updates from "get_media_processing_staus"
                        <script type="text/javascript">
							function updateMedia${media.id}() {
                            	$.getJSON(
									"${url(controller='content', action='get_media_processing_staus', id=media.hash)}",
									processingStatus${media.id}
								);
							}
                            function processingStatus${media.id}(data) {
                                YAHOO.log("Status got = "+data.data);
                                if(!data.data) {
                                    clearInterval(media_thumbnail_timer_${media.id});
                                    YAHOO.log("processing complete reload the image!!!");
									var mt = $("#media_thumbnail_${media.id}");
									mt.src = mt.src + "?" + (new Date().getTime());
                                }
                            }
                            var media_thumbnail_timer_${media.id} = setInterval('updateMedia${media.id}()', 10000);
                        </script>
                        <!-- End media still undergoing proceccesing -->
                    % endif
                    
                </a>
                
                <div class="media_fields">
                    <p><label for="media_file_${media.id}"   >${_("File")}       </label><input id="media_file_${media.id}"    name="media_file_${media.id}"    type="text" disabled="true" value="${media.name}"   /><input type="submit" name="file_remove_${media.id}" value="Remove" class="file_remove"/></p>
                    <p><label for="media_caption_${media.id}">${_("Caption")}    </label><input id="media_caption_${media.id}" name="media_caption_${media.id}" type="text"                 value="${media.caption}"/></p>
                    <p><label for="media_credit_${media.id}" >${_("Credited to")}</label><input id="media_credit_${media.id}"  name="media_credit_${media.id}"  type="text"                 value="${media.credit}" /></p>
                </div>
            </li>
            % endfor
            <!-- End list existing media -->

            <!-- Add media -->
            
            <!-- Add media javascript-->
            % if c.content.id:
            <li>
                YUI SWF Uploader disabled for now
                ##${YUI.file_uploader()}
            </li>
            % endif

            <!-- Add media non javascript -->
            <li>
                <div class="media_preview">
                    <div class="media_preview_none">${_("Select a file to upload")}</div>
                </div>
                <div class="media_fields">
                    <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="file" class="field_file"/><input type="submit" name="submit_draft" value="${_("Upload")}" class="file_upload"/></p>
                    <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text" />${popup("extra_info")}</p>
                    <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text" />${popup("extra_info")}</p>
                </div>              
            </li>
            <!-- End Add media -->

        </ul>
        
    </fieldset>

</%def>

##------------------------------------------------------------------------------
## Content Type
##------------------------------------------------------------------------------
<%def name="content_type()">
    <fieldset><legend>${_("Publish Type")}</legend>
        ${form_instruction("What do you want to do with your content?")}

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
                // Select radio button
                setCheckedValue(document.forms['content'].elements['type'], type);
                // reset all radio buttons to unselected
                setSingleCSSClass(document.getElementById('type_'+type), 'section_selected', 'type_selection');
                ##var elements = getElementByClass("section_selectable","type_selection");
                ##for (var element in elements) {
                ##    removeClass(elements[element], "section_selected");
                ##}
                ##// select section by setting selected class
                ##addClass(YAHOO.util.Dom.get('type_'+type), "section_selected");
            }

            highlightType('${c.content.__type__}'); //Set the default highlighted item to be the content type
        </script>
        
        <%
        types = [
            #("draft"     ,"description of draft content"   ),
            ("article"   ,"description of _article"        ),
            ("assignment","description of _assignemnt"     ),
            ("syndicate" ,"description of syndicated stuff"),
        ]
        %>
        
        <%def name="type_option(type, description)">
            <%
                selected = ""
                if c.content.__type__ == type:
                    selected = 'checked="checked"'
            %>
            <td id="type_${type}" onClick="highlightType('${type}');" class="section_selectable">
              <input class="hideable" type="radio" name="type" value="${type}" ${selected}/>
              <label for="type_${type}">${type}</label>
              <p class="type_description">${_(description)}</p>
            </td>
        </%def>
        
        % if c.content.__type__ == "draft":
            <table id="type_selection"><tr>
            % for type in types:
                ${type_option(type[0],type[1])}
            % endfor
            <tr></table>
        % else:
            ${c.content.__type__}
        % endif

        <div style="float: right;">
            % if c.content.__type__ == "draft":
            <input type="submit" name="submit_publish" value="${_("Publish")}"      />
            % else:
            <input type="submit" name="submit_publish" value="${_("Publish Update")}"/>
            % endif
        </div>


    </fieldset>
</%def>


##------------------------------------------------------------------------------
## Location
##------------------------------------------------------------------------------
<%def name="location()">
    <!-- Licence -->
    <fieldset><legend><span onclick="toggle(this);">${_("Location (optional)")}</span></legend>
        <div class="hideable">
            ${form_instruction("why give us this...")}
            stuff!!
      </div>
	  ${loc.location_picker(field_name='location', always_show_map=True, width="100%")}
    </fieldset>
</%def>


##------------------------------------------------------------------------------
## License
##------------------------------------------------------------------------------
<%def name="license()">
    <% from civicboom.lib.database.get_cached import get_licenses %>
    <!-- Licence -->
    <fieldset><legend><span onclick="toggle(this);">${_("Licence (optional)")}</span></legend>
        <div class="hideable">
            ${form_instruction("What is licensing explanation")}
			<table>
            % for license in get_licenses():
				<tr>
                <%
                  license_selected = ''
                  if c.content.license and license.id == c.content.license_id:
                      license_selected = h.literal('checked="checked"')
                %>
                <td><input id="licence_${license.id}" type="radio" name="licence" value="${license.id}" ${license_selected} /></td>
				<td><a href="${license.url}" target="_blank" title="${_(license.name)}"><img src="/images/licenses/${license.code}.png" alt="${_(license.name)}"/></a></td>
                <td><label for="licence_${license.id}">${license.description}</label></td>
				</tr>
                ##${popup(license.description)}
            % endfor
			</table>
        </div>
    </fieldset>
</%def>


##------------------------------------------------------------------------------
## Submit buttons
##------------------------------------------------------------------------------
<%def name="submit_buttons()">
<div style="text-align: right;">

	% if c.content.__type__ == "draft":
	<input type="submit" name="submit_preview" value="${_("Preview Draft")}"/>
	<input type="submit" name="submit_draft"   value="${_("Save Draft")}"   />
	% else:
	<a href="${h.url('content', id=c.content.id)}">View Content</a>
	% endif

</div>
</%def>
