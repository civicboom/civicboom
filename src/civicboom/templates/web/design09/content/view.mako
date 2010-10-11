<%inherit file="/web/common/html_base.mako"/>

<%namespace name="loc"              file="/web/common/location.mako"     />
<%namespace name="member_includes"  file="/web/common/member.mako"       />
<%namespace name="content_includes" file="/web/common/content_list.mako" />



##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------

<%def name="rss()">${self.rss_header_link()}</%def>
<%def name="rss_url()">${url(controller='search', action='content', response_to=c.result['data']['content']['id'], format='xml')}</%def>
<%def name="rss_title()">Responses to ${c.result['data']['content']['title']}</%def>
## FIXME: extra RSS for "more by this author"?


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${d['content']['title']}</%def>


##------------------------------------------------------------------------------
## Left Col - Actions
##------------------------------------------------------------------------------


<%def name="col_left()">
  
    
    ##-------- By ----------
    <h2>${_("Content by")}</h2>
    ${member_includes.avatar(d['content']['creator'], show_name=True, show_follow_button=True)}
  
  
    ##-------Actions-------
    <h2>${_("Actions")}</h2>
  
  
  
    ## Content Owner Actions
    % if 'editable' in d['content']['actions']:
        <a class="button_small button_small_style_2" href="${h.url('edit_content', id=d['content']['id'])}">
          Edit
        </a>
        ##<a class="button_small button_small_style_2" href="${h.url(controller='content',action='delete',id=content.id)}"
        ##   onclick="confirm_before_follow_link(this,'${_("Are your sure you want to delete this _article?")}'); return false;">
        ##  Delete
        ##</a>
        ${h.secure_link(
          href=url('content', id=d['content']['id'], format='redirect'), method="DELETE",
          value=_("Delete"),
          css_class="button_small button_small_style_2",
          confirm_text=_("Are your sure you want to delete this content?")
        )}
    % endif

    ## Assignment Accept and Withdraw
    % if 'accept' in d['content']['actions']:
        ${h.secure_link(h.url(controller='content_actions',action='accept'  , id=d['content']['id'], format='redirect'), _('Accept')  , css_class="button_small button_small_style_2")}
    % endif
    % if 'withdraw' in d['content']['actions']:
        ${h.secure_link(h.url(controller='content_actions',action='withdraw', id=d['content']['id'], format='redirect'), _('Withdraw'), css_class="button_small button_small_style_2")}
    % endif

    ## Parent Content Owner Actions
    ## TODO needs to be some check to see if user is an organisation and has paid for the power to do this
    ##% if content.actions:
    ##    <a href="" class="button_small button_small_style_2">
    ##        Email Resorces
    ##    </a>
    % if 'approve' in d['content']['actions']:
        ${h.secure_link(h.url(controller='content_actions',action='approve'    , id=d['content']['id'], format='redirect'), _('Approve & Lock'), title=_("Approve and lock this content so no further editing is possible"), css_class="button_small button_small_style_2", confirm_text=_('Once approved this article will be locked and no further changes can be made') )}
    % endif
    % if 'disasociate' in d['content']['actions']:
        ${h.secure_link(h.url(controller='content_actions',action='disasociate', id=d['content']['id'], format='redirect'), _('Disasociate')   , title=_("Dissacociate your content from this response"),                    css_class="button_small button_small_style_2", confirm_text=_('This content with no longer be associated with your content, are you sure?')   )}
    % endif
    
    
    

    % if 'rating' in d['content']:
<%
def selif(r, n):
	if round(r) == n:
		return " selected"
	else:
		return ""
r = (d['content']['rating'] * 5)
%>
		<form id="rating" action="${url('content_action', action='rate', id=d['content']['id'])}" method="POST">
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
						url: "${url(controller='content_actions', action='rate', id=d['content']['id'], format='json')}",
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

    ##<% from civicboom.model.content import UserVisibleContent %>
    ##% if issubclass(content_obj.__class__, UserVisibleContent):
    % if d['content']['type'] == 'article' or d['content']['type'] == 'assignment':
    <h2>${_("Share this")}</h2>
        ${share_links()}
    % endif
  

    ##-------- Licence----------
    <h2>${_("Licence")}</h2>
        dont use obj ref
        ##<a href="${content.license.url}" target="_blank" title="${_(content.license.name)}">
        ##  <img src="/images/licenses/${content.license.code}.png" alt="${_(content.license.name)}" />
        ##</a>
  
    ##-----Copyright/Inapropriate?-------
    <h2>${_("Content issues?")}</h2>
      <a href="" class="button_small button_small_style_1" onclick="swap('flag_content'); return false;">Inappropriate Content?</a>
    
      <div id="flag_content" class="hideable">
        <p class="form_instructions">${_('Flag this _content as inappropriate')}</p>
        ${h.form(url(controller='content_actions', action='flag', id=d['content']['id'], format='redirect'))}
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
        ${h.end_form()}
      </div>
</%def>

##------------------------------------------------------------------------------
## Right Col - Related Content
##------------------------------------------------------------------------------


<%def name="col_right()">
    % if d['content'].get('location'):
      <p>${loc.minimap(
          width="100%", height="200px",
          lat = d['content']['location'].split(' ')[0],
          lon = d['content']['location'].split(' ')[1],
      )}</p>
    % endif
  
    % if d['content']['parent']:
    <h2>Parent content</h2>
    ${content_includes.content_list([d['content']['parent']], mode="mini", class_="content_list_mini")}
    ##<p><a href="${h.url(controller="content", action="view", id=content.parent.id)}">${content.parent.title}</a></p>
    % endif
    
    <h2>Reponses</h2>
    
    ${content_includes.content_list(d['content']['responses'], mode="mini", class_="content_list_mini")}
    
    % if d['content']['type'] == 'assignment':
        <h2>Assignment</h2>
        % if 'accepted' in d['content']:
            <h3>accepted by: ${len(d['content']['accepted'])}</h3>
            ${member_includes.member_list(d['content']['accepted'] , show_avatar=True, class_="avatar_thumbnail_list")}
        % endif
        
        % if 'invited' in d['content']:
            <h3>awaiting reply: ${len(d['content']['invited'])}</h3>
            ${member_includes.member_list(d['content']['invited']  , show_avatar=True, class_="avatar_thumbnail_list")}
        % endif
        
        % if 'withdrawn' in d['content']:
            <h3>withdrawn members: ${len(d['content']['withdrawn'])}</h3>
            ${member_includes.member_list(d['content']['withdrawn'], show_avatar=True, class_="avatar_thumbnail_list")}
        % endif
    % endif    
  
    <%doc>
    % if hasattr(content, "accepted_by"):
        <p>accepted by</p>
        <ul>
        % for member in content.accepted_by:
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


  ##----Title----
  <h1>${d['content']['title']}</h1>

  ##----Type----
  <p>Type: ${d['content']['type']}</p>

  ##----Details----
  % if hasattr(d['content'],'views'):
  <p>views: ${d['content']['views']}</p>
  % endif

  ##----Content----
  <div class="content_text">
    ${h.literal(h.scan_for_embedable_view_and_autolink(d['content']['content']))}
  </div>

  ##----Media-----
  % for media in d['content']['attachments']:
    % if media['type'] == "image":
      <a href="${media['original_url']}"><img src="${media['media_url']}" alt="${media['caption']}"/></a>
    % elif media['type'] == "audio":
		<object type="application/x-shockwave-flash" data="http://flv-player.net/medias/player_flv_maxi.swf" width="320" height="30">
			<param name="movie" value="/flash/player_flv_maxi.swf" />
			<param name="allowFullScreen" value="true" />
			<param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;showvolume=1&amp;showplayer=always&amp;showloading=always" />
		</object>
    % elif media['type'] == "video":
		<object type="application/x-shockwave-flash" data="http://flv-player.net/medias/player_flv_maxi.swf" width="320" height="240">
			<param name="movie" value="/flash/player_flv_maxi.swf" />
			<param name="allowFullScreen" value="true" />
			<param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;startimage=${media['thumbnail_url']}&amp;showvolume=1&amp;showfullscreen=1" />
		</object>
	% else:
		unrecognised media type ${media['type']}
    % endif
  % endfor
  
  ##----Temp Respond----
  <a href="${h.url('new_content', form_parent_id=d['content']['id'])}">Respond to this</a>
  
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
			<tr class="comment self_comment">
		% endif
	% elif author == original:
		% if format == "text":
			(Article Author)
		% elif format == "tr":
			<tr class="comment author_comment">
		% endif
	% else:
		% if format == "text":
			<!-- just a comment -->
		% elif format == "tr":
			<tr class="comment other_comment">
		% endif
	% endif
</%def>
<%def name="comments()">
<h1>${_("Comments")}</h1>
<%
from civicboom.model.meta import Session
from civicboom.model import CommentContent
%>
<style>
.comment TD {
	border-top: 1px solid gray;
	border-bottom: 1px solid gray;
	padding: 8px;
}
.other_comment TD {
	background: #FDF;
}
.self_comment TD {
	background: #FFD;
}
.author_comment TD {
	background: #DFD;
}
</style>
	<table>

    % for comment in d['content']['comments']:
	##${relation(comment['creator']['username'], c.logged_in_user.username, content['creator']['username'], 'tr')}
    <tr>
		<td class="avatar">
			${member_includes.avatar(comment['creator'])}
		</td>
		<td class="comment">
			${comment['content']}
			<b style="float: right;">
				${comment['creator']['name']}
				${relation(comment['creator'], c.logged_in_user, d['content']['creator'], 'text')} --
				${str(comment['creation_date'])[0:19]}
			</b>
		</td>
	</tr>
	% endfor
	<tr class="self_comment" style="background: #FFA;">
		<td class="avatar">
			% if c.logged_in_user:
			<img class='avatar' src="${c.logged_in_user.avatar_url}"><br>
			% endif
		</td>
		<td class="comment">
			${h.form(url('contents'))}
				<input type="hidden" name="form_parent_id" value="${d['content']['id']}">
				<input type="hidden" name="form_title" value="Re: ${d['content']['title']}">
				<input type="hidden" name="form_type" value="comment">
				<textarea name="form_content" style="width: 100%; height: 100px;"></textarea>
				<br><!--<input type="submit" name="submit_preview" value="Preview">--><input type="submit" name="submit_response" value="Post">
			${h.end_form()}
  		</td>
  	</tr>
	</table>
</%def>



##------------------------------------------------------------------------------
## Share This Links
##------------------------------------------------------------------------------

<%def name="share_links()">

    % if 'editable' in d['content']['actions']:
        ##AllanC - temp dissabled until we can create a janrain object based on API output rather than python SQLAlchemy objects
        ##${janrain_aggregate_button()}
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
            % if hasattr(d['content'],'boom_count'):
                <% boom_count = d['content']['boom_count'] %>
            % endif
            <a href="${h.url(controller='content' ,action='boom', id=d['content']['id'], format='redirect')}" title="${_("Boom this! Share this with all your Followers")}">
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
                  content_dict = aggregation_dict(d['content'], safe_strings=True)
                %>
                
                var activity = new RPXNOW.Social.Activity('${content_dict['action']}',
                                                          '${content_dict['description']}',
                                                          '${content_dict['url']}'
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
                
                <%
                    # Generate signiture
                    # Reference - https://rpxnow.com/docs/social_publish_activity#OptionsParameter
                    #           - http://stackoverflow.com/questions/1306550/calculating-a-sha-hash-with-a-string-secret-key-in-python
                    import hashlib, hmac, base64, time
                    apiKey     = config['api_key.janrain']
                    timestamp  = int(time.time())
                    primaryKey = c.logged_in_user.id
                    message    = "%s|%s" % (timestamp,primaryKey)
                    signature  = base64.b64encode(hmac.new(apiKey, msg=message, digestmod=hashlib.sha256).digest()).decode()
                %>
                
                var options = {
                                finishCallback: finished,
                                ##exclusionList: ["facebook", "yahoo"],
                                urlShortening: true,
                                primaryKey: '${primaryKey}',
                                timestamp :  ${timestamp}  ,
                                signature : '${signature}'
                               }
                
                RPXNOW.Social.publishActivity(activity, options);
            });
        }
        
        % if request.params.get('prompt_aggregate')=='True':
            publish_janrain_activity();
        % endif
    </script>
    <!-- End - Janrain Social Publish Widget -->


    <span class="button_small button_small_style_2" href="" onclick="publish_janrain_activity(); return false;">Aggregate</span>
</%def>



