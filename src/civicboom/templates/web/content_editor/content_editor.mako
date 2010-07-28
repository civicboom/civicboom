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
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="content_form">
        <form action="" method="post" enctype="multipart/form-data">
            ${base_content()}
            ${media()}
            ${license()}
            
            <div style="text-align: right;">
                % if c.content.id:
                <input type="submit" name="submit_delete"  value="${_("Delete")}"       />
                % endif
                <input type="submit" name="submit_draft"   value="${_("Save Draft")}"   />
                <input type="submit" name="submit_preview" value="${_("Preview Draft")}"/>
                <input type="submit" name="submit_publish" value="${_("Publish")}"      />
            </div>

        </form>  
    </div>
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
  
        <input type="submit" name="submit_draft"   value="Save Draft"   style="float: right;"/>

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
                <img class="media_preview" src="${media.thumbnail_url}" alt="${media.caption}"/>
                
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
## License
##------------------------------------------------------------------------------
<%def name="license()">
    <!-- Licence -->
    <fieldset><legend><span onclick="toggle(this);">${_("Licence (optional)")}</span></legend>
      <div class="hideable">
        ${instruction("What is licensing explanation")}
        
        % for license in c.licenses:
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