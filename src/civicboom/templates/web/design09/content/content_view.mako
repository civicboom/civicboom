<%inherit file="/web/layout_3cols.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${c.content.title}</%def>


##------------------------------------------------------------------------------
## Left Col
##------------------------------------------------------------------------------

<%def name="col_left()">

  ##-------- By ----------
  <h2>${_("Content by")}</h2>
    ${c.content.creator.username}
  
  
  ##-------Actions-------
  <h2>${_("Actions")}</h2>
  
    % if c.content.editable_by(c.logged_in_user):
      <a class="button_small button_small_style_2" href="${h.url(controller='content',action='edit',id=c.content.id)}">
        Edit
      </a>
      <a class="button_small button_small_style_2" href="${h.url(controller='content',action='delete',id=c.content.id)}"
         onclick="confirm_before_follow_link(this,'${_("Are your sure you want to delete this _article?")}'); return false;">
        Delete
      </a>
    % endif



  ##-----Share Article Links--------
  <%include file="/web/design09/includes/share_links.mako"/>
  

  ##-------- Licence----------
  <h2>${_("Licence")}</h2>
    <a href="${c.content.license.url}" target="_blank">
      <img src="/images/licenses/${c.content.license.code}.png" alt="${_(c.content.license.name)}" />
    </a>

  ##-----Copyright/Inapropriate?-------
  <h2>${_("Content issues?")}</h2>

</%def>

##------------------------------------------------------------------------------
## Right Col
##------------------------------------------------------------------------------

<%def name="col_right()">
  parent content
  sub content/reponses
  accepted reporters
</%def>



##------------------------------------------------------------------------------
## Center Body
##------------------------------------------------------------------------------

<%def name="body()">

  ##----Title----
  <h1>${c.content.title}</h1>

  ##----Content----
  <div class="content_text">
    ${h.literal(h.scan_for_embedable_view_and_autolink(c.content.content))}
  </div>
  
</%def>
