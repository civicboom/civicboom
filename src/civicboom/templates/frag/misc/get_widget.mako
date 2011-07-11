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
    ${widget_preview(c.widget_user_preview or c.logged_in_persona)}
</%def>


##------------------------------------------------------------------------------
## Widget Preview
##------------------------------------------------------------------------------

<%def name="widget_preview(member)">
<div class="get_widget">
    ## style="height: 400px; padding-right: 2em;"
    ## AllanC - style hack above - to get the ***ing popup to pad and size properly in the popup ... $.modal.update() dose not work, the tabs mess with stuff
    <%
        member = normalize_member_username(member);
    %>
    
    ${components.tabs(
        tab_id       ='get_widget_tabs',
        titles       = [_('What is a _widget?'), _('Standard _widget'), _('Animated _widget')],
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
            
            % if current_protocol() != 'http':
            link = link.replace('http://','${current_protocol()}://');
            % endif
            
            // Set preview area to generated iframe url
            widget_creator.find('.preview').html(link);
            // Populate textarea with generated iframe url string
            widget_creator.find('.code').find('textarea').val(link);
        }
    </script>
</div>
</%def>



##------------------------------------------------------------------------------
## Static IFRAME
##------------------------------------------------------------------------------
<%def name="widget_iframe(theme='basic', member=None, protocol='http')">
<%
    widget_default = dict(widget_defaults.get(theme, widget_defaults[config['setting.widget.default_theme']]))
    widget_default['owner'] = normalize_member_username(member)
     ##name='${_("_site_name")}'\
%>
% if member:
<iframe \
 id='CivicboomWidget-${theme}'\
 title='${_("_site_name _widget")}'\
 src='${h.url('member_action', id=widget_default['owner'], action=widget_default['base_list'], theme=theme ,sub_domain='widget', protocol=protocol)}'\
 width='${widget_default['width']}'\
 height='${widget_default['height']}'\
 scrolling='no'\
 frameborder='0'\
>\
<a href='${h.url('member', id=widget_default['owner'], sub_domain='www')}'>${_('%s on _site_name') % widget_default['owner']}</a>\
</iframe>\
% endif
</%def>



##------------------------------------------------------------------------------
## Tab content
##------------------------------------------------------------------------------

##----------------------------------
## What is a widget
##----------------------------------

<%def name="what(member)">
<div class="widget_creator"><div class="padding">
    <h1>What is a _Widget?</h1>
    <p>
        ${_('The _Widget is a little "widget" that lives on your website within which all requests for stories set by you will automatically appear.')}
        ${_('People can respond to requests for news and submit their news through your _Widget, as video, images or audio directly to you for you to edit and publish.')}
    </p>
    
    <p style="font-weight: bold; margin-top: 1em; margin-bottom:1em;">${_('We offer two versions of the _Widget:')}</p>
    
    ## AllanC - I know, it's a table for layout - rewrite it properly, I didnt have time
    <table class="what_table"><tr>
        
        <td>
            <p>1. Standard design: Customizable</p>
            <ul>
                <li>Size adaptable to fit website needs</li>
                <li>Editable colours</li>
                <li>List your _assignments and _articles</li>
                ##<li>Direct "Share your _article" button</li>
            </ul>
        </td>
        <td>
            <img src="/images/widget/preview_basic.png" alt="basic_widget_preview" style="margin-right: 2em;"/>
        </td>
        <td>
            <p>2. Animated Design: Fixed size</p>
            <ul>
                <li>Requests appear on a carousel</li>
                <li>Larger font for clear reading</li>
                ##<li>Direct "Share your story" button</li>
            </ul>
        </td>
        <td>
            <img src="/images/widget/preview_gradient.png" alt="gradient_widget_preview" />
        </td>
        
    </tr></table>

</div></div>
</%def>

##----------------------------------
## Basic
##----------------------------------

<%def name="basic(member)">
<div class="widget_creator">
    <%
        theme          = 'basic'
        widget_default = widget_defaults[theme]
    %>
    <table><tr>
        <td class="description">
            <h2>${_('Grab the _widget')}</h2>
            <ol>
                <li>${_('Give your _widget a title')}</li>
                <li>${_('Choose from the dropdown the content you want to show on the Boombox')}</li>
                <li>${_('Add the right colours and set your size of the _widget (note the font size will remain the same).')}</li>
                <li>${_('Click on preview')}</li>
                <li>${_("When you're happy, copy and paste the code into an HTML page")}</li>
                <li>${_('Start Booming out your _assignments for _articles!')}</li>
            </ol>
        </td>
    
        <td class="params">
            <form action="">
                
                <feildset>
                    <legend>${_("Title")}</legend>
                    <input type="text" name="title" value="${widget_default['title']}" size="30"/><br/>
                </feildset>
                
                <feildset>
                    <legend>${_("Content to show on _widget")}</legend>
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
                </feildset>
                
                <feildset>
                    <legend>${_("Size")}</legend>
                    <div class="params_extra">
                    <label>${_('Width')} </label><input type="text" name="width"  value="${widget_default['width' ]}" size="3" /><br/>
                    <label>${_('Height')}</label><input type="text" name="height" value="${widget_default['height']}" size="3" />
                    </div>
                </feildset>
                
                <fieldset>
                    <legend>${_("Colours")}</legend>
                    <div class="params_extra">
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
                    <label>${color_name}</label><input type="text" id="${color_field}" name="${color_field}" value="${widget_default[color_field]}" size="6" /><br/>
                    % endfor
                    </div>
                    <script type="text/javascript">
                        $(document).ready(function() {
                            % for color_name, color_field in colors:
                            $('#${color_field}').simpleColorPicker();
                            % endfor
                        });
                    </script>
                </fieldset>
            
            </form>
            <input type="button" value=${_("Preview _widget")} onClick="preview_widget($(this));" />
        </td>
        
        <td class="preview" style="width: 280px;">
            ${widget_iframe(theme=theme, member=member, protocol=current_protocol())}
        </td>
    
        <td class="code">
            <form action="">
                <textarea>${widget_iframe(theme=theme, member=member, protocol=current_protocol())}</textarea>
            </form>
        </td>
    
    </tr></table>
</div>
</%def>

##----------------------------------
## Gradient
##----------------------------------

<%def name="gradient(member)">
<div class="widget_creator">
    <%
        theme          = 'gradient'
        widget_default = widget_defaults[theme]
    %>
    <table class="">
        <td class="description">
            <h2>${_('Grab the Animated _widget:')}</h2>
            <ul>
                <li>${_('This _widget animates your _assignments for _articles.')}</li>
                <li>${_('It has a fixed size of 280 x 180.')}</li>
                <li>${_('To get your _widget, simply copy and paste the code into an HTML page.')}</li>
                <li>${_('Note: The dynamic _widget requires Javascript for all viewers.')}</li>
            </ul>
        </td>
        <td class="preview">
            ${widget_iframe(theme=theme, member=member, protocol=current_protocol())}
        </div>
        <td class="code">
            <form action="">
                <textarea>${widget_iframe(theme=theme, member=member, protocol=current_protocol())}</textarea>
            </form>
        </div>
    </table>
</div>
</%def>
