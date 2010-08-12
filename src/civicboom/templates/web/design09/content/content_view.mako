<%inherit file="/web/layout_3cols.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${c.content.title}</%def>


##------------------------------------------------------------------------------
## Left Col - Actions
##------------------------------------------------------------------------------

<%def name="col_left()">

  ##-------- By ----------
  <h2>${_("Content by")}</h2>
    <img src="${c.content.creator.avatar_url}">
	<br>${c.content.creator.name} (${c.content.creator.username})
  
  
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
    <a href="${c.content.license.url}" target="_blank" title="${_(c.content.license.name)}">
      <img src="/images/licenses/${c.content.license.code}.png" alt="${_(c.content.license.name)}" />
    </a>

  ##-----Copyright/Inapropriate?-------
  <h2>${_("Content issues?")}</h2>

</%def>

##------------------------------------------------------------------------------
## Right Col - Related Content
##------------------------------------------------------------------------------

<%def name="col_right()">
<%
# we need to pass the session to GeoAlchemy functions
from civicboom.model.meta import Session
%>
  % if c.content.location:
	<p>${loc.minimap(
		width="100%", height="200px",
		lon=c.content.location.coords(Session)[0],
		lat=c.content.location.coords(Session)[1]
	)}
  % endif
  <p>parent content
  <p>sub content/reponses
  <P>accepted reporters
</%def>



##------------------------------------------------------------------------------
## Center Body
##------------------------------------------------------------------------------

<%def name="body()">

  ##----Details----
  % if hasattr(c.content,'views'):
  <p>views: ${c.content.views}</p>
  % endif

  ##----Title----
  <h1>${c.content.title}</h1>

  ##----Type----
  <p>Type: ${c.content.__type__}</p>


  ##----Content----
  <div class="content_text">
    ${h.literal(h.scan_for_embedable_view_and_autolink(c.content.content))}
  </div>

  ##----Media-----
  % for media in c.content.attachments:
    ##% if media.type == "image":
      <a href="${media.original_url}"><img src="${media.media_url}" alt="${media.caption}"/></a>
    ##% endif
  % endfor
  
  ##----Temp Respond----
  <a href="${h.url(controller="content",action="edit",parent_id=c.content.id)}">Respond to this</a>
  
  ##----Comments----
  ${comments()}
  
</%def>


##------------------------------------------------------------------------------
## Comments
##------------------------------------------------------------------------------
<%def name="relation(author, current, original, format='text')">
	% if author == current:
		% if format == "text":
			(You!)
		% elif format == "tr":
			<tr class="self_comment" style="background: #FFA;">
		% endif
	% elif author == original:
		% if format == "text":
			(Article Author)
		% elif format == "tr":
			<tr class="author_comment" style="background: #AFA;">
		% endif
	% else:
		% if format == "text":
			<!-- just a comment -->
		% elif format == "tr":
			<tr class="comment" style="background: #FAF;">
		% endif
	% endif
</%def>
<%def name="comments()">
	<table>
<%
from civicboom.model.meta import Session
from civicboom.model import CommentContent
%>
## this approach doesn't sort :/
##	% for r in [co for co in c.content.responses if co.__type__ == "comment"]:
##	% for r in Session.query(CommentContent).filter(CommentContent.parent_id==c.content.id).order_by(CommentContent.creation_date):

## AllanC - don't worry Shish my man, helps at hand :)
##          a sorted realtion doing the filtering at the database side 
    % for r in c.content.comments:
	${relation(r.creator, c.logged_in_user, c.content.creator, 'tr')}
		<td class="avatar">
			<a href="${url(controller='user', action='view', id=r.creator.username)}">
				<img class='avatar' src="${r.creator.avatar_url}">
			</a>
		</td>
		<td>
			${r.content}
			<b style="float: right;">
				${r.creator.name}
				${relation(r.creator, c.logged_in_user, c.content.creator, 'text')} --
				${str(r.creation_date)[0:19]}
			</b>
		</td>
	</tr>
	% endfor
	% if c.logged_in_user:
	<tr class="self_comment" style="background: #FFA;">
		<td class="avatar">
			<img class='avatar' src="${c.logged_in_user.avatar_url}"><br>
		</td>
		<td>
			<form action="/content/edit" method="POST">
				<input type="hidden" name="form_parent_id" value="${c.content.id}">
				<input type="hidden" name="form_title" value="Re: ${c.content.title}">
				<input type="hidden" name="form_type" value="comment">
				<textarea name="form_content" style="width: 100%; height: 100px;"></textarea>
				<br><input type="submit" name="submit_preview" value="Preview"><input type="submit" name="submit_response" value="Post">
			</form>
  		</td>
  	</tr>
	% endif
	</table>
</%def>
