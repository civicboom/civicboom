<%inherit file="/web/layout_3cols.mako"/>

<%namespace name="loc"              file="/web/design09/includes/location.mako"     />
<%namespace name="sl"               file="/web/design09/includes/secure_link.mako"  />
<%namespace name="member_includes"  file="/web/design09/includes/member.mako"       />
<%namespace name="content_includes" file="/web/design09/includes/content_list.mako" />


##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------

<%def name="rss()">${self.rss_header_link()}</%def>
<%def name="rss_url()">${url(controller='search', action='content', response_to=c.content.id, format='xml')}</%def>
<%def name="rss_title()">Responses to ${c.content.title}</%def>
## FIXME: extra RSS for "more by this author"?


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
  
  
  
    ## Content Owner Actions
    % if c.content.editable_by(c.logged_in_user):
        
        <a class="button_small button_small_style_2" href="${h.url(controller='content',action='edit',id=c.content.id)}">
          Edit
        </a>

        ${sl.secure_link(h.url(controller='content', action='delete', id=c.content.id), _('Delete')  , css_class="button_small button_small_style_2", title="Delete this content", confirm_text=_('Are your sure you want to delete this content?'))}      
    % endif

    ## Assignment Accept and Withdraw
    % if c.content.__type__ == "assignment" and c.content.acceptable_by(c.logged_in_user):
        <% status = c.content.previously_accepted_by(c.logged_in_user) %>
        %if not status:
            ${sl.secure_link(h.url(controller='content_actions',action='accept'  , id=c.content.id), _('Accept')  , css_class="button_small button_small_style_2")}
        % elif status != "withdrawn":
            ${sl.secure_link(h.url(controller='content_actions',action='withdraw', id=c.content.id), _('Withdraw'), css_class="button_small button_small_style_2")}
        % endif
    % endif

    ## Parent Content Owner Actions
    % if c.content.parent and c.content.is_parent_owner(c.logged_in_user):
        ## TODO needs to be some check to see if user is an organisation and has paid for the power to do this
        % if c.content.status == "locked":
            <a href="" class="button_small button_small_style_2">
                Email Resorces
            </a>
        % else:
            ${sl.secure_link(h.url(controller='content_actions',action='approve'    , id=c.content.id), _('Approve & Lock'), title=_("Approve and lock this content so no further editing is possible"), css_class="button_small button_small_style_2", confirm_text=_('Once approved this article will be locked and no further changes can be made') )}
            ${sl.secure_link(h.url(controller='content_actions',action='disasociate', id=c.content.id), _('Disasociate')   , title=_("Dissacociate your content from this response"),                    css_class="button_small button_small_style_2", confirm_text=_('This content with no longer be associated with your content, are you sure?')   )}
        % endif
        
    % endif
    

    % if hasattr(c.content, "rating"):
<%
def selif(r, n):
	if round(r) == n:
		return " selected"
	else:
		return ""
r = (c.content.rating * 5)
%>
		<form id="rating" action="${url(controller='content_actions', action='rate', id=c.content.id)}" method="POST">
			<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
			<select name="rating" style="width: 120px">
				<option value="0">Unrated</option>
				<option value="1"${selif(r, 1)}>Very poor</option>
				<option value="2"${selif(r, 2)}>Not that bad</option>
				<option value="3"${selif(r, 3)}>Average</option>
				<option value="4"${selif(r, 4)}>Good</option>
				<option value="5"${selif(r, 5)}>Perfect</option>
			</select>
			<input type="submit" value="Rate!">
		</form>
		<script>
		$(function() {
			$("#rating").children().not("select").hide();
			$("#rating").stars({
				inputType: "select",
				callback: function(ui, type, value) {
					## $("#rating").submit();
					$.ajax({
						url: "${url(controller='content_actions', action='rate', id=c.content.id, format='json')}",
						type: "POST",
						data: {
							"_authentication_token": "${h.authentication_token()}",
							"rating": value
						},
						dataType: "json",
						success: function(data) {flash_message(data);},
						error: function(XMLHttpRequest, textStatus, errorThrown) {flash_message(textStatus);}
					});
				}
			});
		});
		</script>
    % endif


    ##-----Share Article Links--------

    <h2>${_("Share this")}</h2>
        ${share_links()}
  

    ##-------- Licence----------
    <h2>${_("Licence")}</h2>
      <a href="${c.content.license.url}" target="_blank" title="${_(c.content.license.name)}">
        <img src="/images/licenses/${c.content.license.code}.png" alt="${_(c.content.license.name)}" />
      </a>
  
    ##-----Copyright/Inapropriate?-------
    <h2>${_("Content issues?")}</h2>
      <a href="" class="button_small button_small_style_1" onclick="swap('flag_content'); return false;">Inappropriate Content?</a>
    
      <div id="flag_content" class="hideable">
          <p class="form_instructions">${_('Flag this _content as inappropriate')}</p>
          <form action="${url(controller='content', action='flag', id=c.content.id)}" method="post">
              <input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
              <select name="type">
                  <% from civicboom.model.content import FlaggedContent %>
                  % for type in [type for type in FlaggedContent._flag_type.enums if type!="automated"]:
                  <option value="${type}">${_(type.capitalize())}</option>
                  % endfor
              </select>
              <p class="form_instructions">${_('Comment (optional)')}</p>
              <textarea name="comment" style="width:90%; height:3em;"></textarea>
              <input type="submit" name="flagit" value="Flag it" class="button_small button_small_style_tiny "/>
              <span class="button_small button_small_style_tiny " onclick="swap('flag_content'); return false;">Cancel</span>
          </form>
      </div>
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
    <h2>Parent content</h2>
    ${content_includes.content_list([c.content.parent], mode="mini", class_="content_list_mini")}
    ##<p><a href="${h.url(controller="content", action="view", id=c.content.parent.id)}">${c.content.parent.title}</a></p>
    % endif
    
    <h2>Reponses</h2>
    
    ${content_includes.content_list(c.content.responses, mode="mini", class_="content_list_mini")}
    
    
    
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



##------------------------------------------------------------------------------
## Share This Links
##------------------------------------------------------------------------------

<%def name="share_links()">

    % if c.content.editable_by(c.logged_in_user):
        ${janrain_aggregate_button()}
    %endif
    
    
    <%doc>
    <ul class="bulleted_list">
      <li><a class="icon icon_diggit"       href="http://digg.com/submit?phase=2?url=${c.current_URL}"              >Diggit      </a></li>
      <li><a class="icon icon_delicious"    href="http://del.icio.us/post?url=${c.current_URL}"                     >Delicious   </a></li>
      <li><a class="icon icon_reddit"       href="http://reddit.com/submit?url=${c.current_URL}"                    >Reddit      </a></li>
      <li><a class="icon icon_stumble_upon" href="http://www.stumbleupon.com/submit?url=${c.current_URL}"           >Stumble Upon</a></li>
      <li><a class="icon icon_facebook"     href="http://www.facebook.com/share.php?u=${c.current_URL}"             >Facebook    </a></li>
      ##<li><a class="icon icon_twitter"      href="http://twitter.com/home?status=Currently reading ${c.current_URL}">Twitter     </a></li>
    </ul>
    </%doc>  
    <!-- AddThis Button BEGIN http://addthis.com/ -->
    <a class="addthis_button" href="http://addthis.com/bookmark.php?v=250&amp;username=xa-4b7acd5429c82acd"><img src="http://s7.addthis.com/static/btn/v2/lg-share-en.gif" width="125" height="16" alt="Bookmark and Share" style="border:0"/></a><script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#username=xa-4b7acd5429c82acd"></script>
    <!-- AddThis Button END -->
    
    
    <div class="yui-g">
        
        <!-- Retweet button -->
        <div class="yui-u first">
            <script type="text/javascript" src="http://tweetmeme.com/i/scripts/button.js"></script>
        </div>
        
        <!-- Boom button -->
        <div class="yui-u">
            <% boom_count = 0 %>
            % if hasattr(c.content,"boom_count"):
                <% boom_count = c.content.boom_count %>
            % endif
            <a href="${h.url(controller='content' ,action='boom',id=c.content.id)}" title="${_("Boom this! Share this with all your Followers")}">
            <div class="boom_this">
                <span class="boom_count">${boom_count}</span>
                <p>${_("Boom this")}</p>
            </div>
            </a>
        </div>
    </div>

</%def>



##------------------------------------------------------------------------------
## Janrain Social Widget - User prompt to aggregate this content
##------------------------------------------------------------------------------

## https://rpxnow.com/docs/social_publish_activity
## https://rpxnow.com/relying_parties/civicboom/social_publishing_1

<%def name="janrain_aggregate_button()">

    <!-- Janrain Social Publish Widget -->
    <script type="text/javascript">
      var rpxJsHost = (("https:" == document.location.protocol) ? "https://" : "http://static.");
      document.write(unescape("%3Cscript src='" + rpxJsHost + "rpxnow.com/js/lib/rpx.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
      RPXNOW.init({appId: '${config['app_id.janrain']}',
        xdReceiver: '/rpx_xdcomm.html'});
    </script>
    
    <script type="text/javascript">
        function publish_janrain_activity() {
            RPXNOW.loadAndRun(['Social'], function () {
                
                ## Get a summary python dictionary of this content
                ## This uses the same JSON generation as the Janrain API but contructs the data for the Jainrain social widget
                <%
                  from civicboom.lib.civicboom_lib import aggregation_dict
                  content_dict = aggregation_dict(c.content, escape_chars=True)
                %>
                
                var activity = new RPXNOW.Social.Activity("${content_dict['title']}",
                                                          "${content_dict['action']}",
                                                          "${content_dict['url']}"
                                                          );
                
                activity.setTitle               ('${content_dict['title']}');
                activity.setDescription         ('${content_dict['description']}');
                activity.setUserGeneratedContent('${content_dict['user_generated_content']}');
                
                % for action_link in content_dict['action_links']:
                    activity.addActionLink('${action_link['text']}', '${action_link['href']}');
                % endfor
                
                % for property in content_dict['properties'].keys():
                    activity.addTextProperty('${property}', '${content_dict['properties'][property]}');
                % endfor
                
                var images = new RPXNOW.Social.ImageMediaCollection();
                % for image in [image for image in content_dict['media'] if image['type']=="image"]:
                    images.addImage('${image['src']}', '${image['href']}');
                % endfor
                activity.setMediaItem(images);
                
                % for media in content_dict['media']:
                    % if media['type'] == "mp3":
                        activity.setMediaItem(new RPXNOW.Social.Mp3MediaItem('${media['src']}')); //title, artist, album
                    % endif
                    % if media['type'] == "video":
                        ## ?? the auto aggregate JSON does not have support for video? but the widget does? hu?
                        activity.setMediaItem(new RPXNOW.Social.VideoMediaItem('${media['src']}', preview_img, video_link, video_title));
                    % endif
                % endfor
                ##addLinkProperty(name, text, url)
                ##addProviderUrl('${_('_site_name')}', '${content_dict['url']}');
                
                var finished = function(results) {
                  // Process results of publishing.
                }
                
                var options = {
                                finishCallback: finished,
                                ##exclusionList: ["facebook", "yahoo"],
                                urlShortening: true,
                                primaryKey: '1029384756',
                                timestamp: 1275987204,
                                signature: 'I5kckgc3v4JaxavG5QQ8+FTbBKgPrmu+2+zXZZ93124='
                               }
                
                RPXNOW.Social.publishActivity(activity, options);
            });
        }
        
        % if request.params.get('prompt_aggregate')=='True':
            publish_janrain_activity();
        % endif
    </script>
    <!-- End - Janrain Social Publish Widget -->


    <a class="button_small button_small_style_2" href="" onclick="publish_janrain_activity(); return false;">Aggregate</a>
</%def>



