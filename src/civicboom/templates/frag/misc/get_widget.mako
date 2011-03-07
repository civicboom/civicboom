##<%namespace name="widget_code" file="/html/widget/get_widget_code.mako" />

<%!
    from civicboom.lib.web import current_protocol
    from pylons import config
    var_prefix = config['setting.widget.var_prefix']
    
    def get_member_username(member):
        member_username = ''
        if hasattr(member, 'to_dict'):
            member = member.to_dict()
        if isinstance(member, basestring):
            member_username = member
        if isinstance(member, dict):
            member_username = member.get('username')
        return member_username
%>

##${widget_code.get_widget_code(c.widget_user_preview)}

${widget_preview(c.widget_user_preview)}

##------------------------------------------------------------------------------
## Widget IFRAME code
##------------------------------------------------------------------------------
## The defaults here should match the defaults in the HTML javascript generator to ensure the IFRAME here is the same an the initial settings
<%def name="widget_iframe(member=None, protocol='http', iframe_url=None)">\
<% member_username = get_member_username(member) %>\
<iframe \
 name='${_("_site_name")}'\
 id='CivicboomWidget'\
 title='${_("_site_name Widget")}'\
% if iframe_url:
 src='${iframe_url}'\
% elif c.widget['base_list'] and member_username:
 src='${h.url('member_action', id=member_username, action=c.widget['base_list'], subdomain='widget', protocol=protocol)}'\
% elif member_username:
 src='${h.url('member'       , id=member_username,                               subdomain='widget', protocol=protocol)}'\
% else:
 src='${h.url('contents'     ,                                                   subdomain='widget', protocol=protocol)}'\
% endif
 width='${c.widget['width']}'\
 height='${c.widget['height']}'\
 scrolling='no'\
 frameborder='0'\
>\
<a href='${h.url('member', id=member_username, subdomain='')}'>${_('%s on _site_name' % member_username)}</a>\
</iframe>\
</%def>


##------------------------------------------------------------------------------
## Widget Preview and Editor
##------------------------------------------------------------------------------

<%def name="widget_preview(member=None)">
  <% member_username = get_member_username(member or c.widget_user_preview) %>\
  ## AllanC: I wanted to get this done, used tabled, fix it if you want ...
  <table class="get_widget"><tr>

    <td style="width: 600px;">
        
        
        <h1>${_('Grab your widget and get your community to respond to your requests! ')}</h1>
        <p>${_('Through the widget, your community and audience can:')}</p>
        <ul style="padding-top: 6px; padding-bottom: 6px;">
            <li>${_('Read your requests')}</li>
            <li>${_('Respond to them immediately')}</li>
            <li>${_('Accept to complete at a later date')}</li>
        </ul>
        <p>${_('Anyone who is not Following you on the _site_name system, but clicks on "Accept" or "Respond" via your widget will automatically become a Follower of you. This means every time you send out a request, they will get alerted.')}</p>
        <p style="padding-top: 6px; padding-bottom: 6px;">${_("Others can also copy and paste this widget's code into their own website's HTML and show it on their site. This can help amplify your reach to a wider audience.")}</p>


        <table><tr>
        <td style="width: 300px; padding-right: 10px; vertical-align: top;">
    
            ## Custimisation controls
            ## The default values of this form must generate the same string as the sub "widget_iframe" above
            ## this is because the IFRAME can work without javascript and so "should" (sigh) the main site.
            
            <form name="widget_customisation" action="" style="padding: 0.5em;">
              <h2>${_('Customise this widget')}</h2>
              <fieldset><legend>${_("Title")}</legend>
                <input type="text"    name="title"     value="${c.widget['title']    }" size="30"/><br/>
                <%
                    base_lists = [
                        ('assignments_active'   , _('my active _assignments')                ),
                        ('assignments_accepted' , _('_assignments I have accepted')          ),
                        ('content_and_boomed'   , _('my _content and _content I have boomed')),
                        ('boomed'               , _('_content I have boomed')                ),
                        ('content'              , _('all my _content')                       ),
                    ]
                %>
                <select name="base_list">
                    % for list_name, list_description in base_lists:
                    <%
                        selected = ''
                        if c.widget['base_list'] == list_name:
                            selected = 'selected'
                    %>
                    <option value="${list_name}" ${selected}>${list_description.capitalize()}</option>
                    % endfor
                </select>
                ##<input type="hidden"  name="base_list" value="${c.widget['base_list']}" size="30"/><!-- should be a drop down box -->
              </fieldset>
              
              <table><tr>
              <td style="vertical-align: top; padding-right: 0.5em;">
                
                <fieldset><legend>${_("Size")}</legend>
                  <label style="width: 50pt">${_('Width')} </label><input type="text" name="width"  value="${c.widget['width' ]}" size="3" /><br/>
                  <label style="width: 50pt">${_('Height')}</label><input type="text" name="height" value="${c.widget['height']}" size="3" />
                </fieldset>
              </td>
              <td style="padding-left: 6px;">
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
                  <table>
                  % for color_name, color_field in colors:
                  <tr><td><label style="width: 50pt">${color_name}</label></td><td><input type="text" id="${color_field}" name="${color_field}" value="${c.widget[color_field]}" size="6" /></td></tr>
                  % endfor
                  </table>
                </fieldset>
              </td>
              </tr></table>
            <input type="button" value="Preview Widget" onClick="generate_widget_link();" />
            </form>
        </td>
        <td style="width:300px">
            <p style="font-weight: bold;" class="link_widget_instructions">${_("Copy and paste this code into your website's HTML:")}</p>
            <form name="widget_creator" action="">
                <textarea name="widget_link" class="link_widget_form_field" style="width: 300px; height: 200px;">${widget_iframe(member)}</textarea>
            </form>      
        </td>
        </tr></table>

          

        
        <%
            # generate the URL used for the IFRAME but dicard everything pased the "?"
            # the first bit of the url is needed for the javascript to generate the IFRAME settings
            # remeber this is duplicated in the widget_iframe
            widget_url = h.url('contents', subdomain='widget', protocol='http')
            if member_username:
                widget_url = h.url('member', id=member_username, subdomain='widget', protocol='http')
                widget_url = widget_url.split('?')[0]
            
        %>
        ##<script src="/javascript/jquery.simple-color-picker.js"></script>
        <script language="javascript" type="text/javascript">
            function generate_widget_link() {
                var link = ""
                link += "<iframe name='${_("_site_name")}' ";
                link += "title='${_("_site_name Widget")}' ";
                link += "src='${widget_url}";
                if (document.widget_customisation.base_list.value!='') {
                  link += "/" + Url.encode(document.widget_customisation.base_list.value);
                }
                link += "?";
                % if member_username:
                link += "${var_prefix}owner="     + Url.encode("${member_username}")                          +"&";
                link += "${var_prefix}base_list=" + Url.encode(document.widget_customisation.base_list.value) +"&";
                % endif
                link += "${var_prefix}title="     + Url.encode(document.widget_customisation.title.value)     +"&";
                % for color_name, color_field in colors:
                link += "${var_prefix}${color_field}=" + Url.encode( document.widget_customisation.${color_field}.value) + "&";
                % endfor
                var width  = document.widget_customisation.width.value
                var height = document.widget_customisation.height.value
                link += "${var_prefix}width="  + width + "&";
                link += "${var_prefix}height=" + height;
                link += "' width='"+width+"' height='"+height+"' scrolling='no' frameborder='0'>";
                % if member_username:
                link += "<a href='${h.url('member', id=member_username, subdomain='')}'>${_('%s on _site_name' % member_username)}</a>";
                % endif
                link += "</iframe>";
                
                document.widget_creator.widget_link.value = link
                
                % if current_protocol() != 'http':
                link = link.replace('http://','${current_protocol()}://');
                % endif
                
                document.getElementById("widget_container").innerHTML = link
            }
            
            $(document).ready(function() {
                % for color_name, color_field in colors:
                $('#${color_field}').simpleColorPicker();
                % endfor
            });

        </script>

    </td>
  
    <td id="widget_container" style="width: 300px; vertical-align: middle; text-align: center;">
        ${widget_iframe(member_username, protocol=None)}
    </td>

  </tr></table>
</%def>
