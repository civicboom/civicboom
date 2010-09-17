<!-- Navigation -->
<div class="navigation_side_graphic"></div>
<div id="navigation" class="yui-ge">
  ##role="navigation", lardmark for screenreaders, but breaks XHTML spec ... need to maybe re-instate this later

  <div class="yui-u first navigation_items">
    <ul>
      <li>
        ${h.secure_link(url('new_content'), _("Create _content"))}
        <div class="tooltip tooltip_icon"><span>${_("Uploading an _article allows you express your ideas, opinions and news to a wider community")}</span></div>
      </li>
      <li>
        <a href="${h.url(controller='search', action='content', type='assignment')}">${_("Find _assignments")}</a>
        <div class="tooltip tooltip_icon"><span>${_("Find open _assignments to respond to")}</span></div>
      </li>
    </ul>
  </div>

  <div class="yui-u unit_b">
    <form action="${h.url(controller='search', action='content')}" method='GET'>
      ${_("Find")}:
      <input type="text"   class="search_input"  name="query" value="News, opinions" onfocus="if(this.value==this.defaultValue)this.value='';" onblur="if(this.value=='')this.value=this.defaultValue;" />
      <input type="submit" class="search_submit" value="" />
    </form>
  </div>
</div>
