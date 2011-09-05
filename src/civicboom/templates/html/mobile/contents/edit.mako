<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

<%def name="page_title()">
    ${_("Edit~")}
</%def>

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
    %>
</%def>

## page structure defs
<%def name="body()">
    <div data-role="page">
        ${components.header()}
        <div data-role="content">

            ${parent.flash_message()}

            ${h.form(
                h.args_to_tuple('content', id=self.id, format="redirect"),
                id           = 'edit_%s' % self.id,
                name         = "content",
                method       = 'PUT',
                multipart    = True,
            )}
            
                <div data-role="fieldcontain" data-theme="b">
                    ## TITLE
                    <label for="title_${self.id}">${_('Add your title')}</label>
                    <input id="title_${self.id}" name="title" type="text" class="edit_input" value="${self.content['title']}" placeholder="${_('Enter a title')}"/><br />

                    ## CONTENT
                    <%
                        area_id = h.uniqueish_id("content")
                    %>
                    <label for="${area_id}">${_("Add more detail and supporting links, etc")}</label>
                    <textarea class="editor edit_input" name="content" id="${area_id}">${self.content['content']}</textarea>
                    
                    ## TAGS
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
                        <span>(${_('separated by commas')})</span>
                    </fieldset>
                    
                </div>
                <div data-role="fieldcontain" data-theme="b">
                    ${submit()}
                </div>
                
            ${h.end_form()}

        </div>
    </div>
</%def>

## SUBMISSION HACKING CORNER :D
<%def name="submit()">

    <%def name="submit_button(name, title_text=None, show_content_frag_on_submit_complete=False, prompt_aggregate=False, mo_text=None, mo_class='mo-help-r', onclick_js='')">
        <%
            button_id = "submit_%s_%s" % (name, self.id)
            if not title_text:
                title_text = _(name)
        %>
    
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
                            submit_complete_${self.id}_url = '${url('content', id=self.id, format="html")}';
                        % endif
                        
                        ## Re-enable button after 1 second
                        setTimeout(function (elem){elem.removeClass('disabled_filter');}, 1000, $(this));
                    }
                % endif
            "
        />
    </%def>

    ${submit_button('publish', _("Post"), show_content_frag_on_submit_complete=True, prompt_aggregate=True, mo_text=_(tooltip), mo_class="mo-help-l", onclick_js="$(this).parents('.buttons').children('.what-now-pop').modal({appendTo: $(this).parents('form')}); return false;" )}

</%def>