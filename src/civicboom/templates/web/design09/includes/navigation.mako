<!-- Navigation -->
<div class="navigation_side_graphic"></div>
<div id="navigation" class="yui-ge">
  ##role="navigation", lardmark for screenreaders, but breaks XHTML spec ... need to maybe re-instate this later

  <div class="yui-u first navigation_items">
    <ul>
      <li>
        <a href="${h.url(controller='content',action='edit'      )}">${_("Create _assignment")}</a>
        <div class="tooltip tooltip_icon"><span>${_("Posting an _assignment allows you to ask questions and make call to actions")}</span></div>
      </li>
      <li>
        <a href="${h.url(controller='content'   ,action='edit'         )}">${_("Upload _article")}</a>
        <div class="tooltip tooltip_icon"><span>${_("Uploading an _article allows you express your ideas, opinions and news to a wider community")}</span></div>
      </li>
    </ul>
  </div>

  <div class="yui-u unit_b">
    <form action="${h.url(controller='search', action='article')}" method='post'>
      ${_("Find")}:
      <input type="text"   class="search_input"  name="description" value="News, opinions" maxlength='50' onfocus="if(this.value==this.defaultValue)this.value='';" onblur="if(this.value=='')this.value=this.defaultValue;" />
      <input type="submit" class="search_submit" name="submit"      value=""   />
      <input type="hidden"                       name="status"      value="up" />
    </form>
  </div>
</div>
