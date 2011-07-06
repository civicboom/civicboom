## Methods for shareing/aggregating links
## 2 alternate companys are implemnted here should we need to swich.

<%!
    import json
    import time
    import base64
    import hmac
    import hashlib
	
    def __(s):
        return s
		
    share_data = {
        'user' : {
	       'new': {
	           'type': {
                    'assignment': "I just created the request %(title)s on _site_name. Respond now!",
                    'response'  : "I just responded to a request by %(owner)s on _site_name. Get involved & add your voice too!",
                    'group'     : "I just created the %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "I just signed up to _site_name to get my news published, you can too!",
                    'article'   : "I just created the content %(title)s on _site_name, check it out here!",
                },
                'tag': {
                    'new_assignment': "Share your _assignment with your friends and followers:",
                    'new_response'  : "Share your response with your friends and followers:",
                    'new_group'     : "Share your _group with your friends and followers:",
                    'new_user'      : "Share your news with your friends and followers:",
                    'new_article'   : "Share your _article with your friends and followers:",
                },
                'desc': {
                    'new_assignment': 'New _assignment on _site_name',
                    'new_response'  : 'New _article on _site_name',
                    'new_group'     : 'New _hub on _site_name',
                    'new_user'      : "I'm on _site_name",
                    'new_article'   : 'New _article on _site_name',
                },
            },
            'existing': {
               'type': {
                    'assignment': "Take a look at my request %(title)s on _site_name. Respond now!",
                    'response'  : "Take a look at my response to a request by %(owner)s on _site_name. Get involved & add your voice too!",
                    'group'     : "Take a look at my %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "Take a look at my profile on _site_name, join to get your news published!",
                    'article'   : "Take a look at my content %(title)s on _site_name!",
                },
                'tag': {
                    'new_assignment': "Share your _assignment with your friends and followers:",
                    'new_response'  : "Share your response with your friends and followers:",
                    'new_group'     : "Share your _group with your friends and followers:",
                    'new_user'      : "Share your profile with your friends and followers:",
                    'new_article'   : "Share your _article with your friends and followers:",
                },
                'desc': {
                    'new_assignment': 'My _assignment on _site_name',
                    'new_response'  : 'My _article on _site_name',
                    'new_group'     : 'My _hub on _site_name',
                    'new_user'      : "I'm on _site_name",
                    'new_article'   : 'My _article on _site_name',
                },
            },
            'other': {
               'type': {
                    'assignment': "I just found the request %(title)s on _site_name. Take a look and respond now!",
                    'response'  : "I just found a response to a request by %(owner)s on _site_name. Get involved & add your voice too!",
                    'group'     : "I just found the %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "I just found %(title) on _site_name to getting their news published, you can too!",
                    'article'   : "I just found the content %(title)s on _site_name, check it out here!",
                },
                'tag': {
                    'new_assignment': "Share this _assignment with your friends and followers:",
                    'new_response'  : "Share this response with your friends and followers:",
                    'new_group'     : "Share this _group with your friends and followers:",
                    'new_user'      : "Share this news with your friends and followers:",
                    'new_article'   : "Share this _article with your friends and followers:",
                },
                'desc': {
                    'new_assignment': '_Assignment on _site_name',
                    'new_response'  : '_Article on _site_name',
                    'new_group'     : '_Hub on _site_name',
                    'new_user'      : "Profile on _site_name",
                    'new_article'   : '_Article on _site_name',
                },
            },
        },
        'group' : {
           'new': {
               'type': {
                    'assignment': "We just created the request %(title)s on _site_name. Respond now!",
                    'response'  : "We just responded to a request by %(owner)s on _site_name. Get involved & add your voice too!",
                    'group'     : "We just created the %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "We just signed up to _site_name to get my news published, you can too!",
                    'article'   : "We just created the content %(title)s on _site_name, check it out here!",
                },
                'tag': {
                    'new_assignment': "Share your _assignment with your friends and followers:",
                    'new_response'  : "Share your response with your friends and followers:",
                    'new_group'     : "Share your _group with your friends and followers:",
                    'new_user'      : "Share your news with your friends and followers:",
                    'new_article'   : "Share your _article with your friends and followers:",
                },
                'desc': {
                    'new_assignment': 'New _assignment on _site_name',
                    'new_response'  : 'New _article on _site_name',
                    'new_group'     : 'New _hub on _site_name',
                    'new_user'      : "I'm on _site_name",
                    'new_article'   : 'New _article on _site_name',
                },
            },
            'existing': {
               'type': {
                    'assignment': "Take a look at our request %(title)s on _site_name. Respond now!",
                    'response'  : "Take a look at our response to a request by %(owner)s on _site_name. Get involved & add your voice too!",
                    'group'     : "Take a look at our %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "Take a look at our profile on _site_name, join to get your news published!",
                    'article'   : "Take a look at our content %(title)s on _site_name!",
                },
                'tag': {
                    'new_assignment': "Share your _assignment with your friends and followers:",
                    'new_response'  : "Share your response with your friends and followers:",
                    'new_group'     : "Share your _group with your friends and followers:",
                    'new_user'      : "Share your profile with your friends and followers:",
                    'new_article'   : "Share your _article with your friends and followers:",
                },
                'desc': {
                    'new_assignment': 'Our _assignment on _site_name',
                    'new_response'  : 'Our _article on _site_name',
                    'new_group'     : 'Our _hub on _site_name',
                    'new_user'      : "We're on _site_name",
                    'new_article'   : 'Our _article on _site_name',
                },
            },
            'other': {
               'type': {
                    'assignment': "We just found the request %(title)s on _site_name. Take a look and respond now!",
                    'response'  : "We just found a response to a request by %(owner)s on _site_name. Get involved & add your voice too!",
                    'group'     : "We just found the %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "We just found %(title) on _site_name to getting their news published, you can too!",
                    'article'   : "We just found the content %(title)s on _site_name, check it out here!",
                },
                'tag': {
                    'new_assignment': "Share this _assignment with your friends and followers:",
                    'new_response'  : "Share this response with your friends and followers:",
                    'new_group'     : "Share this _group with your friends and followers:",
                    'new_user'      : "Share this news with your friends and followers:",
                    'new_article'   : "Share this _article with your friends and followers:",
                },
                'desc': {
                    'new_assignment': '_Assignment on _site_name',
                    'new_response'  : '_Article on _site_name',
                    'new_group'     : '_Hub on _site_name',
                    'new_user'      : "Profile on _site_name",
                    'new_article'   : '_Article on _site_name',
                },
            },
        }
    }
        
	
    share_types = {
        'new_assignment': "I just created the request %(title)s on _site_name. Respond now!",
        'new_response'  : "I just responded to a request by %(owner)s on _site_name. Get involved & add your voice too!",
        'new_group'     : "I just created the %(name)s Hub on _site_name. Get involved and follow it now!",
        'new_user'		: "I just signed up to _site_name to get my news published, you can too!",
        'new_article'   : "I just created the content %(title)s on _site_name, check it out here!",
    }
    share_taglines = {
        'new_assignment': "Share your _assignment with your friends and followers:",
        'new_response'  : "Share your response with your friends and followers:",
        'new_group'     : "Share your _group with your friends and followers:",
        'new_user'		: "Share your news with your friends and followers:",
        'new_article'   : "Share your _article with your friends and followers:",
    }
    share_descs = {
        'new_assignment': 'New _assignment on _site_name',
        'new_response'  : 'New _article on _site_name',
        'new_group'     : 'New _hub on _site_name',
        'new_user'      : "I'm on _site_name",
        'new_article'   : 'New _article on _site_name',
    }
%>

##------------------------------------------------------------------------------
## Share (using default method)
##------------------------------------------------------------------------------
<%def name="share(*args, **kwargs)">
    ${AddThis(*args,**kwargs)}

</%def>

## TODO: need to support mutiple share buttons

##------------------------------------------------------------------------------
## AddThis
##------------------------------------------------------------------------------
## http://www.addthis.com/help/api-overview - registered to admin@civicboom.com
<%def name="AddThisScript(*args, **kwargs)">
    <!-- AddThis Button BEGIN -->
    <script type="text/javascript">
      var addthis_share = {
        "data_track_clickback":true,
        email_template: 'Check out {{url}} on Civicboom',
        templates: {
			twitter: 'Check out {{url}} (from @civicboom)'
		},
		url_transforms : {
			shorten: {      
			    twitter: 'bitly'
			},
		},
	    shorteners : {
	        bitly : { 
	            username: 'civicboom',
	            apiKey: 'R_0bcb2a604c8a101cacff1fa70bbf19c8'
	        }
		},
      };
    </script>
    <script type="text/javascript" src="//s7.addthis.com/js/250/addthis_widget.js#username=civicboom"></script>
</%def>
    <%doc>
<%def name="AddThis(*args, **kwargs)">
    <%
    area_id = h.uniqueish_id("addthis_tb")
    %>
    <div class="addthis_toolbox addthis_cb_style ${area_id}" style="display: inline-block;"
        % for k,v in kwargs.iteritems():
            addthis:${k}="${v.replace('\"','') if v else ""}"
        % endfor
    >
    <a class="addthis_button_email"></a>
    <a class="addthis_button_facebook"></a>
    <a class="addthis_button_twitter"></a>
    <a class="addthis_button_linkedin"></a>
    <a class="addthis_button_compact"></a>
    </div>
    ## Initialise toolbox on fragment load (Greg)
    <script type="text/javascript">
      addthis.toolbox('.addthis_toolbox');
    </script>
    <!-- AddThis Button END -->
    </%def>
</%doc>
<%def name="AddThisFragList(*args, **kwargs)">
    <%
        custom_share_line = kwargs.get('custom_share_line')
        custom_share      = kwargs.get('custom_share')
        if custom_share_line:   del kwargs['custom_share_line']
        if custom_share:        del kwargs['custom_share']
    %>
    <%def name="sharebutton(type, **kwargs)">
        <li><div class="thumbnail thumbnail_small"><a class="at addthis_button_${type} ${kwargs.get('extraclass','')}"
            % for k,v in kwargs.iteritems():
                addthis:${k}="${v.replace('\"','') if v else ""}"
            % endfor
        ></a></div></li>
    </%def>
	
    <div class="frag_list">
        <h2>${_('Social sharing')}</h2>
        <div class="frag_list_contents">
            <div class="content note addthis_toolbox" style="padding-bottom: 0px;">
                % if custom_share_line:
                    <div style="height: 24px">
                        ${custom_share_line()}
                    </div>
                % endif
                <ul class="member">
                    % for name in ['email', 'facebook', 'twitter', 'linkedin']:
                        ${sharebutton(name, **kwargs)}
                    % endfor
                    % if custom_share:
                        ${custom_share() | n}
                    % endif
                </ul>
                <style>
                    .link_more_hide span {
                        width:0; height:0;
                    }
                    .atclear {
                        clear: none;
                        display: none;
                    }
                </style>
                <a class="at addthis_button_compact link_more link_more_hide">more</a>
                <script>
                    $(function(){
                        addthis.toolbox('.addthis_toolbox');
                    });
                </script>
            </div>
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Share This
##------------------------------------------------------------------------------
## http://help.sharethis.com/customization/customization-overview - registered to admin@civicboom.com


<%def name="share_this_js()">
	<!-- ShareThis -->
	<script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
	<script type="text/javascript">
	$(function() {
		stLight.options({
			publisher:'${config['api_key.sharethis']}' ,
			onhover  : false ,
			embeds   : true ,
		});
	});
	</script>
</%def>


<%def name="ShareThis(*args, **kwargs)">
    
    <%def name="share_this_icon(service)">
        <span class="st_${service}_custom icon16 i_${service} link_pointer" title="${_('Share This via ')}${service}"><span>${service}</span></span>
    </%def>
    
    % for service in ['email', 'facebook', 'twitter', 'linkedin']:
        ${share_this_icon(service)}
    % endfor
    <span class="st_sharethis_custom icon16 i_share link_pointer" title="ShareThis"
        % for k,v in kwargs.iteritems():
            st_${k}='${v.replace("'","").replace('"','')}'
        % endfor
    ></span>
    <script type="text/javascript">
		$(function() {
		  for (var stt in $(
			stButtons.locateElements();
			##stButtons.makeButtons();
			##stWidget.init();
		});
    </script>
    ##http://forums.sharethis.com/topic.php?id=3277&replies=1#post-6679
    

    <%doc>
    ## Single share this link
    
    <span class="st_email"></span>
    <span class="st_facebook"></span>
    <span class="st_twitter"></span>
    
    ##<span class="st_facebook_custom"></span>
    ##<span class="st_twitter_custom"></span>

    ##<span class="st_sharethis" displayText="ShareThis"></span>
    <span class="st_sharethis_custom icon16 i_share" title="ShareThis"></span>
    ##<img src="/styles/web/icons16/share-icon.png"> 

    <script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
    <script type="text/javascript">
	$(function() {
        stLight.options({
            publisher  : '${config['api_key.sharethis']}' ,
            onhover    : false ,
            st_url     : '${url}' ,
            ## the .replace is to stop ' in javascript breaking things, can be depricated when validator removes ' from names
            st_title   : '${title.replace("'","")}' ,
            displayText: '${description.replace("'","")}',
        });
	});
    </script>
    </%doc>
    
    <%doc>
    ## Old depricated ShareThis API - waste of my time!
    ## http://sharethis.com/developers/api - hidden API examples
    ## http://forums.sharethis.com/topic.php?id=147
    ## http://forums.sharethis.com/topic.php?id=261
    <span id="share2" class="icon16 i_share" title="ShareThis"></span>
    <script language="javascript" type="text/javascript">
        var st_entry = SHARETHIS.addEntry({
                % for k,v in kwargs.iteritems():
                ${k}:'${v.replace("'","")}',
                % endfor
            } ,
            {button:false}
        );
        st_entry.attachButton(document.getElementByID("share2"));
    </script>
    </%doc>


</%def>



##------------------------------------------------------------------------------
## Janrain Social Widget - User prompt to aggregate this content
##------------------------------------------------------------------------------


## https://rpxnow.com/docs/social_publish_activity
## https://rpxnow.com/relying_parties/civicboom/social_publishing_1

<%def name="init_janrain_social()">
    <!-- Janrain Social Publish Widget -->
    <script type="text/javascript">
      var rpxJsHost = (("https:" == document.location.protocol) ? "https://s3.amazonaws.com/static." : "http://static.");
      document.write(unescape("%3Cscript src='" + rpxJsHost + "rpxnow.com/js/lib/rpx.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
      RPXNOW.init({appId: '${config['app_id.janrain']}',
        xdReceiver: '/rpx_xdcomm.html'});
      
		## Variables: share_display, share_usergen_default, action_share_description, action_page_title, action_page_description, action_links, properties, images, audio, video
		function janrain_popup_share(url, options, variables) {
			RPXNOW.loadAndRun(['Social'], function () {
				if (typeof options != 'object') options = {};
		        var activity = new RPXNOW.Social.Activity(variables.share_display,
		                                                  variables.action_share_description,
		                                                  url
		                                                  );
		        
		        activity.setTitle               (variables.action_page_title);
		        activity.setDescription         (variables.action_page_description);
		        activity.setUserGeneratedContent(variables.share_usergen_default);
		        
		        if (typeof variables.action_links == 'object') {
		        	for (i=0; i<variables.action_links.length; i++) {
			            activity.addActionLink(variables.action_links[i].text, variables.action_links[i].href);
			        }
			    }
			    
		        ##if (typeof variables.properties == 'object') {
		        ##	for (i=0; i<variables.properties.length; i++) {
			    ##        activity.addTextProperty(variables.properties[i].text, variables.properties[i].value);
			    ##    }
			    ##}
			    
			    if (typeof variables.media == 'object') {
			    	var rpx_images;
			    	for (i=0; i<variables.media.length; i++) {
			    		var media = variables.media[i];
			    		if (media.type=='image') {
			    			if (typeof rpx_images == 'undefined')
			    				rpx_images = new RPXNOW.Social.ImageMediaCollection();
			    			rpx_images.addImage(media.src, media.href);
			    		} else if (media.type=='audio') {
			    			activity.setMediaItem(new RPXNOW.Social.Mp3MediaItem(media.src));
			    		} else if (media.type=='video') {
			        		var rpx_video = new RPXNOW.Social.VideoMediaItem(
			        			media.original_url,
			        			media.thumbnail_url
			        		);
			        		rpx_video.setVideoTitle(variables.video[i].caption);
			        		activity.setMediaItem(rpx_video);
			        	}
			        }
			        if (typeof rpx_images != 'undefined')
			        	activity.setMediaItem(rpx_images); 
			    }
		        
		        var finished = function(results) {
		          // Process results of publishing.
		        }
		        
		        options.finishCallback = finished;
		        options.urlShortening = true;
		        
		        RPXNOW.Social.publishActivity(activity, options);
		
		    });
		}
	</script>
</%def>

<%def name="janrain_social(content, value='Janrain Social', class_='')">
    <a href='' class='${class_}' onclick="${janrain_social_js(content)} return false;"><span>${value}</span></a>
</%def>

<%def name="janrain_options()">
    <%
        # Generate signiture
        # Reference - https://rpxnow.com/docs/social_publish_activity#OptionsParameter
        #           - http://stackoverflow.com/questions/1306550/calculating-a-sha-hash-with-a-string-secret-key-in-python
        options = {}
        if c.logged_in_persona:
            apiKey     = config['api_key.janrain']
            options['timestamp']  = int(time.time())
            options['primaryKey'] = str(c.logged_in_persona.id)
            message    = '%s|%s' % (options['timestamp'],options['primaryKey'])
            options['signature']  = base64.b64encode(hmac.new(apiKey, msg=message, digestmod=hashlib.sha256).digest()).decode()
    %>
    ${json.dumps(options).replace('\\\"', "\\\'").replace('"', "'")}
</%def>

<%def name="janrain_social_call_content(content, share_type)">
	## Variables: share_display, share_usergen_default, action_share_description, action_page_title, action_page_description, action_links, properties, images, audio, video
    <%
from civicboom.lib.aggregation import aggregation_dict
cd = aggregation_dict(content, safe_strings=True)
cd['url'] = h.url('content', id=content['id'], qualified=True)
def clean(s):
	if isinstance(s, basestring):
		return s.replace("'", "\\'")
	return ''
share_usergen_default = clean(_(share_types[share_type]) % {'title': cd.get('title'), 'owner': content['creator'].get('name')})
    %>
	$(function() {
		var content   = ${json.dumps(cd).replace("'", "\\\'").replace('\\\"', "\\\'").replace('"', "'")};
		var url       = content.url;
		var variables = {
			share_display:				'${_(share_taglines[share_type])}',
			action_share_description:   '${_(share_descs[share_type])}',
			share_usergen_default:		'${share_usergen_default | n}',
			action_page_title:       	content.title,
			action_page_description: 	content.user_generated_content,
			action_links: 				content.action_links,
			action:						content.action,
			media:						content.media,
		};
		janrain_popup_share(url, ${janrain_options()}, variables);
	});
</%def>

<%def name="janrain_social_call_member(member, share_type)">
	## Variables: share_display, share_usergen_default, action_share_description, action_page_title, action_page_description, action_links, properties, images, audio, video
    <%
cd = {
		'url':						h.url('member', id=member['username'], qualified=True),
		'title':					member['name'],
		'user_generated_content': 	member['description'],
		'media':					[ {
										'type': 'image',
										'src':  member['avatar_url'],
										'href': h.url('member', id=member['username'], qualified=True),
									}, ],
}
def clean(s):
	if isinstance(s, basestring):
		return s.replace("'", "\\'")
	return ''
share_usergen_default = clean(_(share_types[share_type]) % {'name': cd['title']})
    %>
	$(function() {
		var content   = ${json.dumps(cd).replace("'", "\\\'").replace('\\\"', "\\\'").replace('"', "'")};
		var url       = content.url;
		var variables = {
			share_display:				'${clean(_(share_taglines[share_type]))}',
			action_share_description:   '${clean(_(share_descs[share_type]))}',
			share_usergen_default:		'${clean(share_usergen_default) | n}',
			action_page_title:       	content.title,
			action_page_description: 	content.user_generated_content,
			action_links: 				content.action_links,
			action:						content.action,
			media:						content.media,
		};
		janrain_popup_share(url, ${janrain_options() | n}, variables);
	});
</%def>

<%doc>
    % if request.params.get('prompt_aggregate')=='True':
        publish_janrain_activity();
    % endif

<script type="text/javascript">
    function publish_janrain_activity() {
        
    }
    
</script>
<!-- End - Janrain Social Publish Widget -->


##<span class="button_small button_small_style_2" href="" onclick="publish_janrain_activity(); return false;">Aggregate</span>
</%doc>
