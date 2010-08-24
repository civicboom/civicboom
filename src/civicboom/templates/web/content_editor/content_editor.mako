<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Edit _article")}</%def>


##------------------------------------------------------------------------------
## Additional CSS and Javascripts
##------------------------------------------------------------------------------
<%def name="head_links()">
  ${parent.head_links()}
  
  <!-- Additional YUI imports-->
  <link   type="text/css"        href="http://yui.yahooapis.com/2.8.1/build/assets/skins/sam/skin.css"       rel="stylesheet" />
  <script type="text/javascript" src ="http://yui.yahooapis.com/2.8.1/build/container/container_core-min.js" ></script><!-- Needed for Menus, Buttons and Overlays used in the Toolbar -->
  <script type="text/javascript" src ="http://yui.yahooapis.com/2.8.1/build/editor/simpleeditor-min.js"      ></script><!-- Source file for Rich Text Editor-->
  <script type="text/javascript" src ="http://yui.yahooapis.com/2.8.1/build/uploader/uploader-min.js"        ></script>

  <link   type="text/css"        href="/styles/content_editor/content_editor.css" rel="stylesheet" />
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
        <form action="" method="post" enctype="multipart/form-data" name="content">
			<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">

            ${base_content()}
            ${media()}
            ${content_type()}
            ${license()}
            
            <div style="text-align: right;">
                
                % if c.content.id:
                <input type="submit" name="submit_delete"  value="${_("Delete")}"       />
                % endif
                
                % if c.content.__type__ == "draft":
                <input type="submit" name="submit_preview" value="${_("Preview Draft")}"/>
                <input type="submit" name="submit_draft"   value="${_("Save Draft")}"   />
                % else:
                <a href="${h.url(controller='content', action='view', id=c.content.id)}">View Content</a>
                % endif
                
                
            </div>
        
        </form>
    </div>
    
    % if c.content.id:
      ${file_uploader()}
    % endif
</%def>


##------------------------------------------------------------------------------
## Popup
##------------------------------------------------------------------------------
<%def name="popup(text)">
<span class="tooltip tooltip_icon"><span>${_(text)}</span></span>
</%def>

<%def name="instruction(text)">
<p class="form_instuctions">${_(text)}</p>
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
        ${instruction("Got an opinion? want to ask a question?")}

        <p>
            <label for="form_title">${_("Title")}</label>
            <input id="form_title" name="form_title" type="text" value="${c.content.title}" style="width:80%;"/>
            ${popup("extra info")}
        </p>
  
        ${richtext(c.content.content)}
  
        % if c.content.__type__ == "draft":
            <input type="submit" name="submit_draft"   value="Save Draft"   style="float: right;"/>
        % endif

        ## Owner
        <p><label for="form_owner">${_("By")}</label>
        <select name="form_owner">
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
            <label for="form_tags">${_("Tags")}</label>
            <%
            tag_string = u""
            for tag in [tag.name for tag in c.content.tags]:
                tag_string += tag + u" "
            %>
            <input id="form_tags" name="form_tags" type="text" value="${tag_string}"/>
            ${popup("extra_info")}
        </p>

    </fieldset>
</%def>


##------------------------------------------------------------------------------
## YUI Rich Text Component
##------------------------------------------------------------------------------
<%def name="richtext(content, width='100%', height='300px')">

  <!-- Rich Text Component -->
  <div class="yui-skin-sam">
    <textarea id="form_content" name="form_content" style="width:${width}; height:${height};">${content}</textarea>  
    <script type="text/javascript">
      var myEditor = new YAHOO.widget.SimpleEditor('form_content', {
          height: '${height}',
          width: '${width}',
          //dompath: true //Turns on the bar at the bottom
          toolbar: {
            collapse: true,
            titlebar: 'Editing Tools',
            draggable: false,
            buttons: [
              { group: 'text', label: 'Text Effects',
                  buttons: [
                    { type: 'push', label: 'Bold CTRL + SHIFT + B', value: 'bold' },
                    { type: 'push', label: 'Italic CTRL + SHIFT + I', value: 'italic' }
                  ]
              },
              { type: 'separator' },
              { group: 'indentlist', label: 'Lists',
                  buttons: [
                      { type: 'push', label: 'Create an Unordered List', value: 'insertunorderedlist' },
                      { type: 'push', label: 'Create an Ordered List', value: 'insertorderedlist' }
                  ]
              },
              { type: 'separator' },
              { group: 'insertitem', label: 'Insert Link',
                  buttons: [
                      { type: 'push', label: 'HTML Link CTRL + SHIFT + L', value: 'createlink', disabled: true }
                  ]
              }
            ]
          }
      });
      myEditor.set("handleSubmit", true); 
      myEditor.render();										
    </script>

  </div>
  <!-- End Rich Text Component -->

</%def>


##------------------------------------------------------------------------------
## Media Upload and Editor
##------------------------------------------------------------------------------

<%def name="media()">

    <fieldset><legend>${_("Attach Media (optional)")}</legend>      
        ${instruction("Add any relevent pictures, videos, sounds, links to your content")}
        
        <ul class="media_files">

            <!-- List existing media -->
            % for media in c.content.attachments:
            <li>
                <div class="file_type_overlay icon_${media.type}"></div>
                <a href="${media.original_url}">
                    <img class="media_preview" src="${media.thumbnail_url}" alt="${media.caption}"/>
                </a>
                
                <div class="media_fields">
                    <p><label for="form_media_file_${media.id}"   >${_("File")}       </label><input id="form_media_file_${media.id}"    name="form_media_file_${media.id}"    type="text" disabled="true" value="${media.name}"   /><input type="submit" name="form_file_remove_${media.id}" value="Remove" class="form_file_remove"/></p>
                    <p><label for="form_media_caption_${media.id}">${_("Caption")}    </label><input id="form_media_caption_${media.id}" name="form_media_caption_${media.id}" type="text"                 value="${media.caption}"/></p>
                    <p><label for="form_media_credit_${media.id}" >${_("Credited to")}</label><input id="form_media_credit_${media.id}"  name="form_media_credit_${media.id}"  type="text"                 value="${media.credit}" /></p>
                </div>
            </li>
            % endfor
            <!-- End list existing media -->

            <!-- Add media -->
            <li>
                <div class="media_preview">
                    <div class="media_preview_none">${_("Select a file to upload")}</div>
                </div>
                <div class="media_fields">
                    <p><label for="form_media_file"   >${_("File")}       </label><input id="form_media_file"    name="form_media_file"    type="file" class="form_field_file"/><input type="submit" name="submit_draft" value="${_("Upload")}" class="form_file_upload"/></p>
                    <p><label for="form_media_caption">${_("Caption")}    </label><input id="form_media_caption" name="form_media_caption" type="text" />${popup("extra_info")}</p>
                    <p><label for="form_media_credit" >${_("Credited to")}</label><input id="form_media_credit"  name="form_media_credit"  type="text" />${popup("extra_info")}</p>
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
        ${instruction("What do you want to do with your content?")}

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
                setCheckedValue(document.forms['content'].elements['form_type'], type);
                // reset all radio buttons to unselected
                var elements = getElementByClass("section_selectable","type_selection")
                for (var element in elements) {
                    removeClass(elements[element], "section_selected")
                }
                // select section by setting selected class
                addClass(YAHOO.util.Dom.get('form_type_'+type), "section_selected");
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
            <td id="form_type_${type}" onClick="highlightType('${type}');" class="section_selectable">
              <input class="hideable" type="radio" name="form_type" value="${type}" ${selected}/>
              <label for="form_type_${type}">${type}</label>
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
## License
##------------------------------------------------------------------------------
<%def name="license()">
<%
from civicboom.lib.database.get_cached import  get_licenses
%>
    <!-- Licence -->
    <fieldset><legend><span onclick="toggle(this);">${_("Licence (optional)")}</span></legend>
      <div class="hideable">
        ${instruction("What is licensing explanation")}
        
        % for license in get_licenses():
          <%
            license_selected = ''
            if c.content.license and license.id == c.content.license_id:
                license_selected = h.literal('checked="checked"')
          %>
          <input id="form_licence_${license.id}" type="radio" name="form_licence" value="${license.id}" ${license_selected} />
          <label for="form_licence_${license.id}">
            <a href="${license.url}" target="_blank" title="${_(license.name)}"><img src="/images/licenses/${license.code}.png" alt="${_(license.name)}"/></a>
          </label>
          ##${popup(license.description)}
        % endfor
        
      </div>
    </fieldset>
</%def>


##------------------------------------------------------------------------------
## File Uploader
##------------------------------------------------------------------------------
<%def name="file_uploader(progressbar_size=(300,5))">
    
    ## YUI 2.8.1 - File Uploader Component
    ## Reference - http://developer.yahoo.com/yui/uploader/
    
    ## Overlay a transparent SWF object over the button by using CSS absolute positioning
    <div id="uploaderContainer" style="width:80px; height:30px; position: absolute"></div>
    <button type="button"                                            >Select file</button>
    <button type="button" onClick="upload();           return false;">Upload     </button>
    <button type="button" onClick="handleClearFiles(); return false;">Clear      </button>
    
    <div style="border: black 1px solid; width:${progressbar_size[0]}px; height:40px;">
        <div id="upload_file"     style="text-align:center; margin:5px; font-size:15px; width:${progressbar_size[0]-10}px; height:25px; overflow:hidden"></div>
        <div id="upload_progress" style="width:${progressbar_size[0]}px;height:${progressbar_size[1]}px;background-color:#CCCCCC"></div>
    </div>

    <script type="text/javascript">
        YAHOO.widget.Uploader.SWFURL = "http://yui.yahooapis.com/2.8.1/build/uploader/assets/uploader.swf";
        ## Flash has a security model to stop uploaded to unauthorised domains
        ## If the .swf file is not served fromt the local server
        ## the file crossdomain.xml MUST be present in the root public dir for the flash component to upload to the server
        ## Example crossdomain.xml
        ##  <?xml version="1.0"?>
        ##  <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
        ##  <cross-domain-policy>
        ##    <allow-access-from domain="*"/>
        ##    <site-control permitted-cross-domain-policies="master-only"/>
        ##  </cross-domain-policy>

        
        var uploader = new YAHOO.widget.Uploader( "uploaderContainer" ); //, "assets/buttonSprite.jpg"
        var fileID;
    
        uploader.addListener('contentReady'      , handleContentReady);
        uploader.addListener('fileSelect'        , onFileSelect      );
        uploader.addListener('uploadStart'       , onUploadStart     );
        uploader.addListener('uploadProgress'    , onUploadProgress  );
        uploader.addListener('uploadCancel'      , onUploadCancel    );
        uploader.addListener('uploadComplete'    , onUploadComplete  );
        uploader.addListener('uploadCompleteData', onUploadResponse  );
        uploader.addListener('uploadError'       , onUploadError     );
    
        function handleContentReady () {
            uploader.setAllowLogging(true);  	   // Allows the uploader to send log messages to trace, as well as to YAHOO.log
            uploader.setAllowMultipleFiles(false); // Restrict selection to a single file (that's what it is by default).
            var ff = new Array({description:"Images", extensions:"*.jpg;*.png;*.gif;*.jpeg"}, // New set of file filters.
                               {description:"Videos", extensions:"*.avi;*.mov;*.mpg;*.3gp;*.3gpp;*.flv;*.mp4"});
            uploader.setFileFilters(ff);           // Apply new set of file filters to the uploader.
        }

        function handleClearFiles() {
            uploader.clearFileList();
            uploader.enable();
            fileID = null;
            document.getElementById("upload_file"    ).innerHTML = "";
            document.getElementById("upload_progress").innerHTML = "";
        }

        function onFileSelect(event) {
            for (var item in event.fileList) {
                if(YAHOO.lang.hasOwnProperty(event.fileList, item)) {
                    YAHOO.log(event.fileList[item].id);
                    fileID = event.fileList[item].id;
                }
            }
            uploader.disable();
            document.getElementById("upload_file"    ).innerHTML = event.fileList[fileID].name;
            document.getElementById("upload_progress").innerHTML = "";
        }
    
        function upload() {
            if (fileID != null) {
                ##uploader.upload(fileID, "${app_globals.site_url}/content/upload_media/${c.content_media_upload_key}", "POST");
                uploader.upload(fileID, "${url(host=app_globals.site_host, controller='content', action='upload_media', id=c.content_media_upload_key)}", "POST");
                fileID = null;
            }
        }

        function onUploadProgress(event) {
            setProgressBar(event["bytesLoaded"]/event["bytesTotal"]);
        }
        
        function onUploadComplete(event) {
            uploader.clearFileList();
            uploader.enable();
            setProgressBar(1);
            ## submit save draft (to reload page with preview thumbnail)
        }

        function onUploadStart   (event) {YAHOO.log("Upload Start");    YAHOO.log(event);}
        function onUploadError   (event) {YAHOO.log("Upload Error");    YAHOO.log(event);}
        function onUploadCancel  (event) {YAHOO.log("Upload Cancel");   YAHOO.log(event);}
        function onUploadResponse(event) {YAHOO.log("Upload Response"); YAHOO.log(event);}

        function setProgressBar(percent) {
            document.getElementById("upload_progress").innerHTML = "<div style='background-color: #0f0; height: ${progressbar_size[1]}px; width: "+ Math.round(percent*${progressbar_size[0]}) + "px'/>";
        }

    </script>

</%def>
