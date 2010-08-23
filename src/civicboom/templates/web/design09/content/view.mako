<%inherit file="/web/layout_3cols.mako"/>
<%namespace name="loc"             file="../includes/location.mako"/>
<%namespace name="member_includes" file="../includes/member.mako"  />

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
    ${member_includes.avatar(c.content.creator, show_name=True, show_follow_button=True)}
  
  
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

    % if c.content.__type__ == "assignment" and c.content.acceptable_by(c.logged_in_user):
        <% status = c.content.previously_accepted_by(c.logged_in_user) %>
        %if not status:
            <a class="button_small button_small_style_2" href="${h.url(controller='assignment',action='accept',  id=c.content.id)}">
              Accept
            </a>
        % elif status != "withdrawn":
            <a class="button_small button_small_style_2" href="${h.url(controller='assignment',action='withdraw',id=c.content.id)}">
              Withdraw
            </a>
        % endif
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
      )}</p>
    % endif
  
    % if c.content.parent:
    <p>parent content</p>
    <p><a href="${h.url(controller="content", action="view", id=c.content.parent.id)}">${c.content.parent.title}</a></p>
    % endif
    
    <p>sub content/reponses</p>
    <ul>
      % for response in c.content.responses:
          <li><a href="${h.url(controller="content", action="view", id=response.id)}">${response.title}</a>${response.__type__}</li>
      % endfor
    </ul>
    
    
    % if hasattr(c.content, "assigned_to"):
    <h2>Assignment</h2>
        <%
            accepted  = [a.member for a in c.content.assigned_to if a.status=="accepted" ]
            invited   = [a.member for a in c.content.assigned_to if a.status=="pending"  ]
            withdrawn = [a.member for a in c.content.assigned_to if a.status=="withdrawn"]
        %>
    
        <h3>accepted by: ${len(accepted)}</h3>
        ${member_includes.member_list(accepted , show_avatar=True, class_="avatar_thumbnail_list")}
        
        <h3>awaiting reply: ${len(invited)}</h3>
        ${member_includes.member_list(invited  , show_avatar=True, class_="avatar_thumbnail_list")}
        
        <h3>withdrawn members: ${len(withdrawn)}</h3>
        ${member_includes.member_list(withdrawn, show_avatar=True, class_="avatar_thumbnail_list")}
    % endif
    
  
    <%doc>
    % if hasattr(c.content, "accepted_by"):
        <p>accepted by</p>
        <ul>
        % for member in c.content.accepted_by:
            <li>${member.username}</li>
        % endfor
        </ul>
    % endif
    </%doc>


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
    % if media.type == "image":
      <a href="${media.original_url}"><img src="${media.media_url}" alt="${media.caption}"/></a>
    % elif media.type == "audio":
		<object type="application/x-shockwave-flash" data="http://flv-player.net/medias/player_flv_maxi.swf" width="320" height="30">
			<param name="movie" value="/flash/player_flv_maxi.swf" />
			<param name="allowFullScreen" value="true" />
			<param name="FlashVars" value="flv=${media.media_url}&amp;title=${media.caption}\n${media.credit}&amp;showvolume=1&amp;showplayer=always&amp;showloading=always" />
		</object>
    % elif media.type == "video":
		<object type="application/x-shockwave-flash" data="http://flv-player.net/medias/player_flv_maxi.swf" width="320" height="240">
			<param name="movie" value="/flash/player_flv_maxi.swf" />
			<param name="allowFullScreen" value="true" />
			<param name="FlashVars" value="flv=${media.media_url}&amp;title=${media.caption}\n${media.credit}&amp;startimage=${media.thumbnail_url}&amp;showvolume=1&amp;showfullscreen=1" />
		</object>
	% else:
		unrecognised media type ${media.type}
    % endif
  % endfor
  
  ##----Temp Respond----
  <a href="${h.url(controller="content",action="edit",form_parent_id=c.content.id)}">Respond to this</a>
  
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
<%
from civicboom.model.meta import Session
from civicboom.model import CommentContent
%>
	<table>
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
