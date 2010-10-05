<%inherit file="/web/common/html_base.mako"/>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">Widget Preview</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
  <div class="misc_page_border widget_preview">
    <h1>${_('Widget test drive')}</h1>
    <p>${_('This widget is a preview of the widget for %s' % c.widget_user_preview.username)}</p>
    ${get_widget_code(c.widget_user_preview)}
  </div>
</%def>



##------------------------------------------------------------------------------
## Widget Code
##------------------------------------------------------------------------------

<%def name="widget_code(member=None)">
<%
    if hasattr(member, 'username'):
        member = member.username
    
    # Todo - if c.widget_variables are setup then use these as defaults for the code base so the widget can be cloned
%>
<iframe name ='${_("_site_name")}'
        title='${_("_site_name Widget")}'
        src  ='${h.url(
            host=app_globals.site_host, protocol='http',
            controller='widget', action='main',
            widget_username = member,
            widget_theame   ='light',
            widget_title    = _('%s insight: Share your news and opinion' % member),
            widget_width    = '240', widget_height='370'
        )}'
        width='240' height='370' scrolling='no' frameborder='0'>'
    <a href='${h.url(host=app_globals.site_host, controller='reporter', action='profile', id=member)}'>
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

  % if preview:
    <div class="yui-g">
      <div class="yui-u first">
        <div id="widget_container" style="float:right;">
          ${widget_code(member)}
        </div>
      </div>
      <div class="yui-u">
  % endif
  
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
      <fieldset><legend>Title</legend>
        <input type="text"   name="title" value="${_('%s insight: Share your news and opinion' % member)}" size="60"/><br/>
      </fieldset>
      <fieldset><legend>Theme</legend>
        <label>${_('Light')}</label><input type="radio" name="theme" value="light" checked/><br/>
        <label>${_('Dark')} </label><input type="radio" name="theme" value="dark"         />
      </fieldset>
      
      <fieldset><legend>Size</legend>
        <label>${_('Width')} </label><input type="text" name="width"  value="240" size="3" /><br/>
        <label>${_('Height')}</label><input type="text" name="height" value="370" size="3" />
      </fieldset>
  
      <input type="button" value="Preview Widget" onClick="generate_widget_link();" />
    </form>
    
    <script language="javascript" type="text/javascript">
      function generate_widget_link() {
        var link = ""
        link += "<iframe name='${_("_site_name")}' title='${_("_site_name Widget")}' src='http://${app_globals.site_host}/widget/main?";
        link += "widget_username="+Url.encode("${member}")+"&";
        if (document.widget_customisation.theme[0].checked) {link += "widget_theame=light&";}
        if (document.widget_customisation.theme[1].checked) {link += "widget_theame=dark&" ;}
        link += "widget_title="+Url.encode(document.widget_customisation.title.value)+"&";
        var width  = document.widget_customisation.width.value
        var height = document.widget_customisation.height.value
        link += "widget_width="+width+"&";
        link += "widget_height="+height;
        link += "' width='"+width+"' height='"+height+"' scrolling='no' frameborder='0'><a href='${h.url(host=app_globals.site_host, controller='reporter', action='profile', id=member)}'>${_('%ss _assigments on _site_name' % member)}</a></iframe>";
        document.widget_creator.widget_link.value = link
        
        document.getElementById("widget_container").innerHTML = link
      }
    </script>
  % endif
  
  % if preview:
      </div>
    </div>
  % endif
</%def>
