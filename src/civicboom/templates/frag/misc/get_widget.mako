##<%namespace name="widget_code" file="/html/widget/get_widget_code.mako" />

##${widget_code.get_widget_code(c.widget_user_preview)}

${widget_preview(c.widget_user_preview)}

##------------------------------------------------------------------------------
## Widget IFRAME code
##------------------------------------------------------------------------------
## The defaults here should match the defaults in the HTML javascript generator to ensure the IFRAME here is the same an the initial settings
<%def name="widget_iframe(member=None)">\
<%
    if not member:
        member = c.logged_in_persona
    if hasattr(member, 'to_dict'):
        member = member.to_dict()
%>\
<iframe \
 name='${_("_site_name")}'\
 id='CivicboomWidget'\
 title='${_("_site_name Widget")}'\
% if c.widget['base_list']:
 src='${h.url('member_action', id=member['username'], action=c.widget['base_list'], subdomain='widget', protocol='http')}'\
% else:
 src='${h.url('member'       , id=member['username'],                               subdomain='widget', protocol='http')}'\
% endif
 width='${c.widget['width']}'\
 height='${c.widget['height']}'\
 scrolling='no'\
 frameborder='0'\
>\
<a href='${h.url('member', id=member['username'], subdomain='')}'>${_('%s on _site_name' % member['username'])}</a>\
</iframe>\
</%def>


##------------------------------------------------------------------------------
## Widget Preview and Editor
##------------------------------------------------------------------------------

<%def name="widget_preview(member=None)">
    <%
        if not member:
            member = c.logged_in_persona
        if hasattr(member, 'to_dict'):
            member = member.to_dict()
    %>

  ## AllanC: I wanted to get this done, used tabled, fix it if you want ...
  <table class="get_widget"><tr>

    <td style="width: 600px;">
        
        
        <h1>${_('Grab your widget and get your community to respond to your requests! ')}</h1>
        <p>${_('Through the widget, your community and audience can:')}</p>
        <ul>
            <li>${_('Read your requests')}</li>
            <li>${_('Respond to them immediately')}</li>
            <li>${_('Accept to complete at a later date')}</li>
        </ul>
        <p>${_('Anyone who isnt Following you on the Civicboom system, but clicks on "Accept" or "Respond" via your widget will automatically become a Follower of you. This means every time you send out a request, they will get alerted.')}</p>
        <p>${_('Others can also grab the code for this widget and post on their own web pages - amplifying your reach to a wider audience.')}</p>


        <table><tr>
        <td>
            <form name="widget_creator" action="">
                <textarea name="widget_link" class="link_widget_form_field" style="width: 250px; height: 200px;">${widget_iframe(member)}</textarea>
            </form>      
            <p class="link_widget_instructions">${_('Copy and paste this code onto your HTML')}</p>
        </td>
        <td>
    
            ## Custimisation controls
            ## The default values of this form must generate the same string as the sub "widget_iframe" above
            ## this is because the IFRAME can work without javascript and so "should" (sigh) the main site.
            
            <form name="widget_customisation" action="" style="padding: 0.5em;">
              <h2>${_('Customise this widget')}</h2>
              <fieldset><legend>${_("Title")}</legend>
                <input type="text"    name="title"     value="${c.widget['title']    }" size="30"/><br/>
                <input type="hidden"  name="base_list" value="${c.widget['base_list']}" size="30"/><!-- should be a drop down box -->
              </fieldset>
              
              <table><tr>
              <td style="vertical-align: top; padding-right: 0.5em;">
                
                <fieldset><legend>${_("Size")}</legend>
                  <label>${_('Width')} </label><input type="text" name="width"  value="${c.widget['width' ]}" size="3" /><br/>
                  <label>${_('Height')}</label><input type="text" name="height" value="${c.widget['height']}" size="3" />
                </fieldset>
              </td>
              <td style="vertical-align: top;">
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
                  <tr><td><label>${color_name}</label></td><td><input type="text" id="${color_field}" name="${color_field}" value="${c.widget[color_field]}" size="6" /></td></tr>
                  % endfor
                  </table>
                </fieldset>
              </td>
              </tr></table>
            <input type="button" value="Preview Widget" onClick="generate_widget_link();" />
            </form>
        </td>
        </tr></table>

          

        
        <%
            # generate the URL used for the IFRAME but dicard everything pased the "?"
            # the first bit of the url is needed for the javascript to generate the IFRAME settings
            widget_url = h.url('member', id=member['username'], subdomain='widget', protocol='http')
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
                link += "w_owner="     + Url.encode("${member['username']}")                       +"&";
                link += "w_base_list=" + Url.encode(document.widget_customisation.base_list.value) +"&";
                link += "w_title="     + Url.encode(document.widget_customisation.title.value)     +"&";
                % for color_name, color_field in colors:
                link += "w_${color_field}=" + Url.encode( document.widget_customisation.${color_field}.value) + "&";
                % endfor
                var width  = document.widget_customisation.width.value
                var height = document.widget_customisation.height.value
                link += "w_width="  + width + "&";
                link += "w_height=" + height;
                link += "' width='"+width+"' height='"+height+"' scrolling='no' frameborder='0'>";
                link += "<a href='${h.url('member', id=member['username'], subdomain='')}'>${_('%s on _site_name' % member['username'])}</a>";
                link += "</iframe>";
                document.widget_creator.widget_link.value = link
                
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
        ${widget_iframe(member)}
    </td>

  </tr></table>
</%def>
