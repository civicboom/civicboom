<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes

<%namespace name="edit_full" file="/frag/contents/edit.mako" />

##<%namespace name="components"      file="/html/mobile/common/components.mako" />
##<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
##<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

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
    %>
</%def>


##------------------------------------------------------------------------------

<%def name="page_title()">
    ${_(d['content']['title'])}
</%def>

##------------------------------------------------------------------------------

<%def name="body()">
    ## page structure defs
    ${content_edit()}
    
</%def>

##------------------------------------------------------------------------------

<%def name="content_edit()">

    <h1>
        % if self.content.get('parent'):
            ${_("You are responding to: %s") % self.content['parent']['title']}
        % elif self.selected_type == 'assignment':
            ${_("Ask for stories")}
        % elif self.selected_type == 'article':
            ${_("Post a story")}
        % endif
    </h1>

    ## parent?

    ${h.form(
        ##h.args_to_tuple(
        h.url('content', id=self.id, format="redirect"),
        id           = 'edit_%s' % self.id,
        name         = "content",
        method       = 'PUT',
        multipart    = True,
        ##pre_onsubmit = "tinyMCE.triggerSave(true,true);",
        ##json_form_complete_actions = "json_submit_complete_for_%(id)s();" % dict(id=self.id)
    )}
        
        ${edit_full.invalid_messages()}
        ${base_content()}
        ${media()}
        ${content_extra_fields()}
        ${location()}
        % if not self.content.get('parent'):
            ${privacy()}
        % endif
        ##${edit_full.tags()}
        ${submit_buttons()}
        ${license()}
        
    ${h.end_form()}

</%def>

##------------------------------------------------------------------------------

<%def name="base_content()">
    ## auto save?
    <input    id="title_${self.id}"   name="title"   class="edit_input"        value="${self.content['title']}" type="text" placeholder="${_('Enter a story title')}"/><br />
    <textarea id="content_${self.id}" name="content" class="editor edit_input"       >${self.content['content']}</textarea>
</%def>

##------------------------------------------------------------------------------

<%def name="media()">

    <ul class="media_files">
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
                    ## Clients with    javascript can have live updates from the media controller
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
    </ul>
    
    <div class="media_preview">
        <div class="media_preview_none">${_("Select a file to upload")}</div>
    </div>
    <div class="media_fields">
        <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="file" class="field_file"/><input type="submit" name="submit_draft" value="${_("Upload")}" class="file_upload"/></p>
        <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text" /></p>
        <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text" /></p>
    </div>              

</%def>

##------------------------------------------------------------------------------

<%def name="content_extra_fields()">

    % if self.selected_type == 'assignment':
        Due date n stuff
    % endif
</%def>

##------------------------------------------------------------------------------    

<%def name="location()">
    ## location
    ## (just a use my location) tick box
</%def>

<%def name="privacy()">
privacy
</%def>

<%def name="license()">
licence
</%def>

##------------------------------------------------------------------------------

<%def name="submit_buttons()">

    <%def name="submit_button(name, text)">
        <input type='submit' name='submit_${name}' value='${text}'>
    </%def>

    ## Preview + Publish
    % if self.content['type'] == "draft":
        ${submit_button('draft'  , _("Save draft"))}
        ${submit_button('preview', _("Preview draft"))}
        % if 'publish' in self.actions:
            ${submit_button('publish', _("Post"))}
        % endif        
    ## Update
    % else:
        % if 'update' in self.actions:
        ${submit_button('publish', _("Update"))}
        % endif
        <a class="button" href="${h.url('content', id=self.id)}">${_("View Content")}</a>
    % endif
</%def>

##------------------------------------------------------------------------------