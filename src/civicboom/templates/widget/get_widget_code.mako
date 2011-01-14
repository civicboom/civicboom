
##------------------------------------------------------------------------------
## Widget Code
##------------------------------------------------------------------------------
## The defaults here should match the defaults in the HTML javascript generator to ensure the IFRAME here is the same an the initial settings
<%def name="widget_code(member=None)">
<%
    if hasattr(member, 'username'):
        member = member.username
    
    def c_(key):
      if hasattr(c,key):
        return getattr(c,key)
      return None
    
    width  = c_('widget_width')  or 240
    height = c_('widget_height') or 320
    theme  = c_('widget_theme')  or 'light'
    title  = c_('widget_title')  or member
%>
<iframe name ='${_("_site_name")}'
        title='${_("_site_name Widget")}'
        src  ='${h.url(
            host=app_globals.site_host, protocol='http',
            controller='widget', action='main',
            widget_username = c_('widget_username') or member,
            widget_theme    = theme ,
            widget_title    = title ,
            widget_width    = width ,
            widget_height   = height,
        )}'
        width='${width}' height='${height}' scrolling='no' frameborder='0'>'
    <a href='${h.url(host=app_globals.site_host, controller='members', action='show', id=member)}'>
        ${_('%ss _assigments on _site_name' % member)}
    </a>
</iframe>
</%def>

## Old notes for Javascript import that never took off because we went with the IFRAME method
##%if reporter:
##<script type='text/javascript'>civicboom_username='${reporter}';</script>
##%endif
##<script src='/static/widget/widget.js' type='text/javascript'></script>
##<div style='width: 300px; background-color: #eee; border: 1px solid black; padding: 0.25em;'>
##${reporter}
##<div style='clear: both;'>
##get involved <a href='#'>mobile reporting app</a><a href='#'>gadget</a>powered by ${c.site_name}
##</div>
##</div>



<%def name="get_widget_code(member=None, preview=True, instructions=True, customisation_controls=True)">
  <%
    if hasattr(member, 'username'):
      member = member.username
  %>

  ## AllanC: I wanted to get this done, used tabled, fix it if you want ...
  <table><tr>

    <td style="width: 400px;">
      
      <h1>${_('Widget test drive')}</h1>
      <p>${_('This widget is a preview of the widget for %s' % c.widget_user_preview.username)}</p>
      
      % if instructions:
        <p>${_('Embed the widget on your own website.')}</p>
      % endif
      
      <form name="widget_creator" action="">
        <textarea name="widget_link" class="link_widget_form_field" rows="5" cols="60">${widget_code(member)}</textarea>
      </form>
    
      % if instructions:
        <p class="link_widget_instructions">${_('Copy and paste this code onto your HTML')}</p>
      % endif
    
      ## Custimisation controls
      ## The default values of this form must generate the same string as the sub "get_widget_code" above
      ## this is because the IFRAME can work without javascript and so "should" (sigh) the main site.
      % if preview and customisation_controls:
        <h2>${_('Customise this widget')}</h2>
        
        <form name="widget_customisation" action="">
          <fieldset><legend>${_("Title")}</legend>
            <input type="text"   name="title" value="${_('%s insight: Share your news and opinion' % member)}" size="60"/><br/>
          </fieldset>
          <fieldset><legend>${_("Theme")}</legend>
            <label>${_('Light')}</label><input type="radio" name="theme" value="light" checked/><br/>
            <label>${_('Dark')} </label><input type="radio" name="theme" value="dark"         />
          </fieldset>
          
          <fieldset><legend>${_("Size")}</legend>
            <label>${_('Width')} </label><input type="text" name="width"  value="240" size="3" /><br/>
            <label>${_('Height')}</label><input type="text" name="height" value="300" size="3" />
          </fieldset>
          
          <input type="button" value="Preview Widget" onClick="generate_widget_link();" />
        </form>
        
        <script language="javascript" type="text/javascript">
          function generate_widget_link() {
            var link = ""
            link += "<iframe name='${_("_site_name")}' title='${_("_site_name Widget")}' src='http://${app_globals.site_host}/widget/main?";
            link += "widget_username="+Url.encode("${member}")+"&";
            if (document.widget_customisation.theme[0].checked) {link += "widget_theme=light&";}
            if (document.widget_customisation.theme[1].checked) {link += "widget_theme=dark&" ;}
            link += "widget_title="+Url.encode(document.widget_customisation.title.value)+"&";
            var width  = document.widget_customisation.width.value
            var height = document.widget_customisation.height.value
            link += "widget_width="+width+"&";
            link += "widget_height="+height;
            link += "' width='"+width+"' height='"+height+"' scrolling='no' frameborder='0'><a href='${h.url(host=app_globals.site_host, controller='members', action='show', id=member)}'>${_('%ss _assigments on _site_name' % member)}</a></iframe>";
            document.widget_creator.widget_link.value = link
            
            document.getElementById("widget_container").innerHTML = link
          }
        </script>
      % endif
    </td>
  
    % if preview:
      <td id="widget_container" style="width: 400px; vertical-align: middle; text-align: center;">
        ${widget_code(member)}
      </td>
    % endif

  </tr></table>

</%def>
