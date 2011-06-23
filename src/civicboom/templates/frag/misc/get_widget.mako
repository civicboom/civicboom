<%namespace name="components" file="/html/web/common/components.mako" />

##------------------------------------------------------------------------------
## Imports
##------------------------------------------------------------------------------
<%!
    from civicboom.lib.widget import widget_defaults
    

    from civicboom.lib.web import current_protocol
    from pylons import config
    var_prefix = config['setting.widget.var_prefix']
    
    def normalize_member_username(member):
        member_username = ''
        if hasattr(member, 'to_dict'):
            member = member.to_dict()
        if isinstance(member, basestring):
            member_username = member
        if isinstance(member, dict):
            member_username = member.get('username')
        return member_username
%>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    ${widget_preview(c.logged_in_persona)}
</%def>


##------------------------------------------------------------------------------
## Widget Preview
##------------------------------------------------------------------------------

<%def name="widget_preview(member)">
    <%
        member = normalize_member_username(member);
    %>
    
    ${components.tabs(
        tab_id       ='get_widget_tabs',
        titles       = [_('What is a _widget?'), _('Stardard _widget'), _('Carousel _widget')],
        tab_contents = [what                   , basic                , gradient             ],
        member = member
    )}
    
    <%
        widget_url_base = h.url('member', id=member, sub_domain='widget', protocol='http')
        widget_url_base = widget_url_base.split('?')[0] # Failsafe - we don't want ANY additonal params
    %>
    <script type="text/javascript">
        var widget_var_prefix = '${var_prefix}';
        function preview_widget(element) {
            widget_creator = element.closest('.widget_creator');
            
            var link = ""
            link += "<iframe name='${_("_site_name")}' ";
            link += "title='${_("_site_name Widget")}' ";
            link += "src='${widget_url_base}";
            
            // Get all widget vars from param form
            var widget_vars = new Array();
            widget_creator.find('.params').find(':input').each(function(index) {
                widget_vars[$(this).attr('name')] = $(this).val()
            });
            
            // Overlay widget variables over link url
            if (widget_vars['base_list']) {
              link += "/" + Url.encode(widget_vars['base_list']);
              delete widget_vars['base_list'];
            }
            link += "?";
            
            //widget_vars[key]
            for (key in widget_vars) {
                var value = widget_vars[key];
                if (typeof value == 'string') {
                    link += widget_var_prefix+key+"="+Url.encode(value)+"&";
                }
            }
            
            link += "' width='"+widget_vars['width']+"' height='"+widget_vars['height']+"' scrolling='no' frameborder='0'>";
            link += "<a href='${h.url('member', id=member, sub_domain='www')}'>${_('%s on _site_name' % member)}</a>";
            link += "</iframe>";
            
            // Set preview area to generated iframe url
            widget_creator.find('.preview').html(link);
            // Populate textarea with generated iframe url string
            widget_creator.find('.code').find('textarea').val(link);
        }
    </script>
</%def>



##------------------------------------------------------------------------------
## Static IFRAME
##------------------------------------------------------------------------------
<%def name="widget_iframe(theme='basic', member=None, protocol='http')">
<%
    widget_default = dict(widget_defaults.get(theme, 'basic'))
    widget_default['owner'] = normalize_member_username(member)
%>
% if member:
<iframe \
 name='${_("_site_name")}'\
 id='CivicboomWidget'\
 title='${_("_site_name _widget")}'\
 src='${h.url('member_action', id=widget_default['owner'], action=widget_default['base_list'], sub_domain='widget', protocol=protocol)}'\
 width='${widget_default['width']}'\
 height='${widget_default['height']}'\
 scrolling='no'\
 frameborder='0'\
>\
<a href='${h.url('member', id=widget_default['owner'], sub_domain='www')}'>${_('%s on _site_name' % widget_default['owner'])}</a>\
</iframe>\
% endif
</%def>



##------------------------------------------------------------------------------
## Tab content
##------------------------------------------------------------------------------

<%def name="what(member)">
what
</%def>

<%def name="basic(member)">
<div class="widget_creator">
    <%
        theme          = 'basic'
        widget_default = widget_defaults[theme]
    %>
    <div class="params">
        <form name="widget_customisation" action="">
            
            <label>${_("Title")}</label>
                <input type="text" name="title" value="${widget_default['title']}" size="30"/><br/>
            
            <label>${_("Base list")}</label>
                <%
                    base_lists = [
                        ('assignments_active'   , _('My active _assignments')                ),
                        ('assignments_accepted' , _('_Assignments I have accepted')          ),
                        ('content_and_boomed'   , _('My _content and _content I have boomed')),
                        ('boomed'               , _('_Content I have boomed')                ),
                        ('content'              , _('My _content')                           ),
                    ]
                %>
                <select name="base_list">
                    % for list_name, list_description in base_lists:
                    <%
                        selected = ''
                        if widget_default['base_list'] == list_name:
                            selected = 'selected'
                    %>
                    <option value="${list_name}" ${selected}>${list_description}</option>
                    % endfor
                </select>
            
            <label>${_("Size")}</label>
                <label>${_('Width')} </label><input type="text" name="width"  value="${widget_default['width' ]}" size="3" />
                <label>${_('Height')}</label><input type="text" name="height" value="${widget_default['height']}" size="3" />
            
            <fieldset><legend>${_("Colours")}</legend>
                <%
                    colors = [
                        (_('Border') , 'color_border'    ),
                        (_('Header') , 'color_header'    ),
                        (_('Action') , 'color_action_bar'),
                        (_('Content'), 'color_content'   ),
                        (_('Font')   , 'color_font'      ),
                    ]
                %>
                % for color_name, color_field in colors:
                <label>${color_name}</label><input type="text" id="${color_field}" name="${color_field}" value="${widget_default[color_field]}" size="6" />
                % endfor
            </fieldset>
        
        </form>
        <input type="button" value=${_("Preview _widget")} onClick="preview_widget($(this));" />
    </div>
    
    <div class="preview">
        ${widget_iframe(theme=theme, member=member, protocol=current_protocol())}
    </div>
    
    <div class="code">
        <form action="">
            <textarea>${widget_iframe(theme=theme, member=member, protocol=current_protocol())}</textarea>
        </form>
    </div>
</div>
</%def>

<%def name="gradient(member)">
gradient
</%def>