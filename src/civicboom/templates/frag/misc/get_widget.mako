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
  <table><tr>

    <td style="width: 400px;">
      
        <h1>${_('Widget test drive')}</h1>
        <p>${_('This widget is a preview of the widget for %s' % member['username'])}</p>
        
        
        <p>${_('Embed the widget on your own website.')}</p>
        
        
        <form name="widget_creator" action="">
          <textarea name="widget_link" class="link_widget_form_field" rows="5" cols="60">${widget_iframe(member)}</textarea>
        </form>
      
        <p class="link_widget_instructions">${_('Copy and paste this code onto your HTML')}</p>
    
    
      ## Custimisation controls
      ## The default values of this form must generate the same string as the sub "widget_iframe" above
      ## this is because the IFRAME can work without javascript and so "should" (sigh) the main site.

        <h2>${_('Customise this widget')}</h2>
        
        <form name="widget_customisation" action="">
          <fieldset><legend>${_("Title")}</legend>
            <input type="text"    name="title"     value="${c.widget['title']    }" size="60"/><br/>
            <input type="hidden"  name="base_list" value="${c.widget['base_list']}" size="60"/><!-- should be a drop down box -->
          </fieldset>
          <fieldset><legend>${_("Theme")}</legend>
            <label>${_('Light')}</label><input type="radio" name="theme" value="light" checked/><br/>
            <label>${_('Dark')} </label><input type="radio" name="theme" value="dark"         />
          </fieldset>
          
          <fieldset><legend>${_("Size")}</legend>
            <label>${_('Width')} </label><input type="text" name="width"  value="${c.widget['width' ]}" size="3" /><br/>
            <label>${_('Height')}</label><input type="text" name="height" value="${c.widget['height']}" size="3" />
          </fieldset>

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
            <label>${color_name}</label><input type="text" id="${color_field}" name="${color_field}" value="${c.widget[color_field]}" size="6" /><br/>
            % endfor
          </fieldset>

          
          <input type="button" value="Preview Widget" onClick="generate_widget_link();" />
        </form>
        
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
                if (document.widget_customisation.theme[0].checked) {link += "w_theme=light&";}
                if (document.widget_customisation.theme[1].checked) {link += "w_theme=dark&" ;}
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
  
    <td id="widget_container" style="width: 400px; vertical-align: middle; text-align: center;">
        ${widget_iframe(member)}
    </td>

  </tr></table>
</%def>
