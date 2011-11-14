<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%!
import html2text
%>

<%namespace name="content_list_includes" file="/html/mobile/contents/index.mako" />
<%namespace name="edit_full"             file="/frag/contents/edit.mako"         />



##------------------------------------------------------------------------------

<%def name="title()">${_(d['content']['title'])}</%def>

##------------------------------------------------------------------------------

<%def name="body()">
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
    
    <div data-role="page" data-theme="b" id="content-edit-${self.id}">
        ${self.header()}
        
        ## AllanC - could use swipe events to see parent conent?
        ##${self.swipe_event('#content-main-%s' % id, '#content-info-%s' % id, 'left')}
        
        <div data-role="content">
            ${content_edit()}
        </div>
    </div>
    
    ${confirm_dialogs(self.content)}
</%def>

##------------------------------------------------------------------------------

<%def name="content_edit()">

    <h1>
        % if self.content.get('parent'):
            ${_("You are responding to: %s") % self.content['parent']['title']}
        % elif self.selected_type == 'assignment':
            ${_("Ask for _articles")}
        % elif self.selected_type == 'article':
            ${_("Post _content")}
        % endif
    </h1>

    <%doc>
    % if self.content['parent']:
    <ul data-role="listview" data-inset="true">
        ${content_list_includes.parent_content(self.content)}
    </ul>
    % endif
    </%doc>


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
    
    <div data-role="collapsible-set" data-theme="a">
        ${base_content()}
        ${media()}
        ${content_extra_fields()}
        ${location()}
        ${license()}
        % if not self.content.get('parent'):
            ${privacy()}
        % endif
    </div>
        ${submit_buttons()}

        
    ${h.end_form()}

</%def>

##------------------------------------------------------------------------------

<%def name="base_content()">
<div data-role="collapsible" data-content-theme="c" data-collapsed="false">
    <h3>Content</h3>
    <fieldset data-role="fieldcontain">
        <label   for="title_${self.id}">${_('Title')}</label>
        <input    id="title_${self.id}"   name="title"   class="edit_input"        value="${self.content['title']}" type="text" placeholder="${_('Enter _article title')}"/>
        
        <label   for="content_${self.id}">${_('Content')}</label>
        <textarea id="content_${self.id}" name="content" class="editor edit_input">${html2text.html2text(self.content['content'])}</textarea>
        <input id="content_text_format_${self.id}" type="hidden" name="content_text_format" value="markdown" />
        
        <label for="tags_${self.id}">${_("Tags")}</label>
        <span>(${_('separated by commas')})</span>
        <%
        tags = []
        separator = config['setting.content.tag_string_separator']
        if   isinstance(self.content['tags'], list):
            tags = self.content['tags']
        elif isinstance(self.content['tags'], basestring):
            tags = self.content['tags'].split(separator)
            
        #tags_string = u""
        #for tag in tags:
        #    tags_string += tag + separator
        tags_string = separator.join(tags)
        %>
        <input class="edit_input" name="tags_string" type="text" value="${tags_string}" id="tags_${self.id}"/>
    </fieldset>
</div>

## Autosave
<script type="text/javascript">
    function ajaxSave() {
        $.ajax({
            type    : 'POST',
            dataType: 'json',
            url     : "${url('content', id=self.id, format='json')}",
            data    : {
                "_method": 'PUT',
                "title"              : $('#title_${self.id}'  ).val(),
                "content"            : $('#content_${self.id}').val(),
                "content_text_format": $('#content_text_format_${self.id}').val(),
                ## AllanC - it may be possible to autosave other fields here, however, caution, what happens if a user is half way through editing a date and the autosave kicks in and the validators fire?. This needs testing issue #698
                "mode"   : 'autosave',
                "_authentication_token": '${h.authentication_token()}'
            },
            success: function(data) {
                flash_message(data);
            },
            error: function (jqXHR, status, error) {
                flash_message({status:'error', message:'${_('Error automatically saving your content')}'});
            },
        });
    }
    % if self.content['type'] == "draft":
        setInterval('ajaxSave()', 60 * 1000);
    % endif
</script>

</%def>

##------------------------------------------------------------------------------

<%def name="media()">
<div data-role="collapsible" data-content-theme="c">
    <h3>${_('Media')}</h3>

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
        <p><label for="media_file"   >${_("File")}       </label><input id="media_file"    name="media_file"    type="file" class="field_file" onchange="$('.media_fields input:submit').button('enable');"/><input type="submit" name="submit_draft" value="${_("Upload selected file")}" class="file_upload" disabled='disabled'/></p>
        <p><label for="media_caption">${_("Caption")}    </label><input id="media_caption" name="media_caption" type="text" /></p>
        <p><label for="media_credit" >${_("Credited to")}</label><input id="media_credit"  name="media_credit"  type="text" /></p>
    </div>

    <%doc>
    <script type="text/javascript">    
        $(document).ready(
            function(){
                $('input:file').change(
                    function(){
                        if ($(this).val()) {
                            $('input:submit').attr('disabled',false);
                            // or, as has been pointed out elsewhere:
                            // $('input:submit').removeAttr('disabled'); 
                        } 
                    }
                    );
            }
        );
    </script>
    </%doc>

    
</div>
</%def>

##------------------------------------------------------------------------------

<%def name="content_extra_fields()">
    % if self.selected_type == 'assignment':
    <div data-role="collapsible" data-content-theme="c">
        <h3>${_('_assignment Dates')}</h3>
        <%
            due_date                      = str(self.content.get('due_date'  )                    or self.content.get('extra_fields',{}).get('due_date'  ) or '')[:16]
            event_date                    = str(self.content.get('event_date')                    or self.content.get('extra_fields',{}).get('event_date') or '')[:16]
            auto_publish_trigger_datetime = str(self.content.get('auto_publish_trigger_datetime') or '')[:16]
        %>
        <input class="detail" type="datetime" name="due_date"                      value="${due_date}"                      />
        <input class="detail" type="datetime" name="event_date"                    value="${event_date}"                    />
        % if self.content['type']=='draft' and c.logged_in_persona.has_account_required('plus'):
        <input class="detail" type="datetime" name="auto_publish_trigger_datetime" value="${auto_publish_trigger_datetime}" />
        % endif
    </div>
    % endif
</%def>

##------------------------------------------------------------------------------    

<%def name="location()">
<div data-role="collapsible" data-content-theme="c">
    <h3>${_('Location')}</h3>

    <script type="text/javascript">
        function set_location(position) {
			var latitude = position.coords.latitude;
			var longitude = position.coords.longitude;
            // Set the form location value
            $('#location').val(""+ longitude + " " + latitude)
        }
        
        function get_location() {
            if (geo_position_js.init()) {
               geo_position_js.getCurrentPosition(set_location);
            }
        }
        
        % if not self.content.get('location'):
        $("#content-edit-${self.id}").live('pageinit', function() {
            get_location();
        });
        % endif
    </script>
    
    ##<input type="checkbox" name="auto_get_location" onclick="">
    <label for="location">${_('GPS location')}</label>
    <input id="location" type="text" name="location" value="${self.content['location']}" checked="checked" readonly="readonly"/>
    <button onclick="get_location(); return false;">Update GPS Location</button>
</div>
</%def>

<%def name="privacy()">
<div data-role="collapsible" data-content-theme="c">
    <h3>${_('Content Visibility')}</h3>
    
</div>
</%def>

<%def name="license()">
<div data-role="collapsible" data-content-theme="c">
    <h3>${_('License')}</h3>
    <p>${_('This content will be posted under the')} <a href="http://creativecommons.org/licenses/by/2.0/uk/" rel="external">Creative Commons Attributed Licence.</a> <img src="/images/licenses/CC-BY.png" />
</div>
</%def>

##------------------------------------------------------------------------------


<%def name="submit_buttons()">

    <hr/>

    <%def name="submit_button(name, text)">
        <input type='submit' name='submit_${name}' value='${text}'>
    </%def>

    ## Preview + Publish
    % if self.content['type'] == "draft":
        ${submit_button('draft'  , _("Save draft"))}
        ${submit_button('preview', _("Preview draft"))}
        % if 'publish' in self.actions:
            ${submit_button('publish', _("Publish"))}
        % endif        
    ## Update
    % else:
        % if 'update' in self.actions:
        ${submit_button('publish', _("Update"))}
        % endif
        <a data-role="button" data-theme="c" href="${h.url('content', id=self.id)}">${_("View Content")}</a>
    % endif
    
    <hr/>
    
    <a data-role="button" data-theme="c" href="#confirm_discard" data-rel="dialog" data-transition="fade">${_('Return to profile')}</a>
    <a data-role="button" data-theme="c" href="#confirm_delete"  data-rel="dialog" data-transition="fade">${_('Delete')}</a>

</%def>


<%def name="confirm_dialogs(content)">
    <%doc>
        These are reusable dialog templates.
        These can be included by other templates.
        They do not all need to be linked to - including all of them here is not a problem
    </%doc>

    <div data-role="page" id="confirm_discard">
        <div data-role="header"><h1>${_('Discard changes?')}</h1></div>
        <div data-role="content">
            <h3>${_('You will loose any unsaved changes to this _content')}</h3>
            <a href="${h.url(controller='profile', action='index')}"><button>${_('Return to profile (discard changes)')}</button></a>
            <a href="#" data-rel="back" data-direction="reverse"><button>${_('No, take me back!')}</button></a>
        </div>
    </div>

    ## Delete Dialog------------------------------------------------------------
    ##% if "delete" in d.get('actions', []):
    <div data-role="page" id="confirm_delete">
        <div data-role="header"><h1>${_('Delete _content?')}</h1></div>
        <div data-role="content">
            <h3>${_("Are you sure you want to delete '%s'? The posting will be permanently deleted from _site_name.") % content.get('title')}</h3>
            ${self.form_button(h.url('content', id=content['id']), _('Delete'), method="delete")}
            <a data-role="button" href="#" data-rel="back" data-direction="reverse">${_('No, take me back!')}</a>
        </div>
    </div>
    ##% endif

    ## AllanC - NOTE! this is NOT to be used for the main Publish action ... as this publishes the existing draft and does not submit the rest of the current form
    <div data-role="page" id="confirm_publish">
        <div data-role="header"><h1>${_('Publish _content?')}</h1></div>
        <div data-role="content">
            <h3>${_('You are about to publish "%s" as "%s".') % (content.get('title'), content['creator']['name'])}</h3>
            <p>${_('All your followers will be notified and it will be visible for other _site_name users to see')}</p>
            ${h.secure_form(h.url('content', id=content['id'], format='redirect', submit_publish='publish'), data_ajax=False, method="put")}
            <input type="submit" value="${_('Publish')}">
            ${h.end_form()}
            <a data-role="button" href="#" data-rel="back" data-direction="reverse">${_('No, take me back!')}</a>
        </div>
    </div>
    
</%def>
