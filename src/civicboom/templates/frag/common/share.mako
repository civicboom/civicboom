## Methods for shareing/aggregating links
## 2 alternate companys are implemnted here should we need to swich.

##------------------------------------------------------------------------------
## Share (using default method)
##------------------------------------------------------------------------------
<%def name="share(*args, **kwargs)">
    ${ShareThis(*args,**kwargs)}

</%def>

## TODO: need to support mutiple share buttons

##------------------------------------------------------------------------------
## AddThis
##------------------------------------------------------------------------------
## http://www.addthis.com/help/api-overview - registered to admin@civicboom.com
<%def name="AddThis(*args, **kwargs)">
    <!-- AddThis Button BEGIN -->
    <div class="addthis_toolbox addthis_default_style " style="display: inline-block;"
        % for k,v in kwargs.iteritems():
            addthis:${k}="${v.replace('"','')}"
        % endfor
    >
    <a class="addthis_button_preferred_1"></a>
    <a class="addthis_button_preferred_2"></a>
    ##<a class="addthis_button_preferred_3"></a>
    ##<a class="addthis_button_preferred_4"></a>
    <a class="addthis_button_compact"></a>
    </div>
    <script type="text/javascript">var addthis_config = {"data_track_clickback":true};</script>
    <script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#username=civicboom"></script>
    <!-- AddThis Button END -->
</%def>

##------------------------------------------------------------------------------
## Share This
##------------------------------------------------------------------------------
## http://help.sharethis.com/customization/customization-overview - registered to admin@civicboom.com


<%def name="share_this_js()">
	<!-- ShareThis -->
	<script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
	<script type="text/javascript">
		stLight.options({
			publisher:'${config['api_key.sharethis']}' ,
			onhover  : false ,
			embeds   : true ,
		});
	</script>
</%def>


<%def name="ShareThis(*args, **kwargs)">
    
    <%def name="share_this_icon(service)">
        <span class="st_${service}_custom icon icon_${service}" title="${_('Share This via ')}${service}"><span>${service}</span></span>
    </%def>
    
    % for service in ['email', 'facebook', 'twitter', 'linkedin']:
        ${share_this_icon(service)}
    % endfor
    <span class="st_sharethis_custom icon icon_share" title="ShareThis"
        % for k,v in kwargs.iteritems():
            st_${k}='${v.replace("'","")}'
        % endfor
    ></span>
    <script type="text/javascript">
        stButtons.locateElements();
        ##stButtons.makeButtons();
        ##stWidget.init();
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
    <span class="st_sharethis_custom icon icon_share" title="ShareThis"></span>
    ##<img src="/styles/web/icons16/share-icon.png"> 

    <script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script>
    <script type="text/javascript">
        stLight.options({
            publisher  : '${config['api_key.sharethis']}' ,
            onhover    : false ,
            st_url     : '${url}' ,
            ## the .replace is to stop ' in javascript breaking things, can be depricated when validator removes ' from names
            st_title   : '${title.replace("'","")}' ,
            displayText: '${description.replace("'","")}',
        });
    </script>
    </%doc>
    
    <%doc>
    ## Old depricated ShareThis API - waste of my time!
    ## http://sharethis.com/developers/api - hidden API examples
    ## http://forums.sharethis.com/topic.php?id=147
    ## http://forums.sharethis.com/topic.php?id=261
    <span id="share2" class="icon icon_share" title="ShareThis"></span>
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
      var rpxJsHost = (("https:" == document.location.protocol) ? "https://" : "http://static.");
      document.write(unescape("%3Cscript src='" + rpxJsHost + "rpxnow.com/js/lib/rpx.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
      RPXNOW.init({appId: '${config['app_id.janrain']}',
        xdReceiver: '/rpx_xdcomm.html'});
    </script>
</%def>


<%def name="janrain_social(content, value='Janrain Social', class_='')">
    <a href='' class='${class_}' onclick="${janrain_social_js(content)} return false;"><span>${value}</span></a>
</%def>


<%def name="janrain_social_js(content, share_display='Share this _content', action_description='')">
    RPXNOW.loadAndRun(['Social'], function () {
        
        ## Get a summary python dictionary of this content
        ## This uses the same JSON generation as the Janrain API but contructs the data for the Jainrain social widget
        <%
            from civicboom.lib.civicboom_lib import aggregation_dict
            cd = aggregation_dict(content, safe_strings=True)
            
            def clean(s):
                if isinstance(s, basestring):
                    return s.replace("'", "\'")
                return ''
        %>
        
        var activity = new RPXNOW.Social.Activity('${clean(share_display      or cd.get('action')      )}',
                                                  '${clean(action_description or cd.get('description') )}',
                                                  '${clean(cd.get('url'))}'
                                                  );
        
        activity.setTitle               ('${clean(cd.get('title')                 )}');
        activity.setDescription         ('${clean(cd.get('description')           )}');
        activity.setUserGeneratedContent('${clean(cd.get('user_generated_content'))}');
        
        % for action_link in cd['action_links']:
            activity.addActionLink('${clean(action_link.get('text'))}', '${clean(action_link.get('href'))}');
        % endfor
        
        % for property in cd['properties'].keys():
            activity.addTextProperty('${clean(property)}', '${clean(cd['properties'][property])}');
        % endfor
        
        <% images = [image for image in cd['media'] if image['type']=='image'] %>
        % if images:
        var images = new RPXNOW.Social.ImageMediaCollection();
        % for image in images:
            images.addImage('${clean(image['src'])}', '${clean(image['href'])}');
        % endfor
        activity.setMediaItem(images);
        % endif
        
        % for media in cd['media']:
            % if media['type'] == 'mp3':
                activity.setMediaItem(new RPXNOW.Social.Mp3MediaItem('${clean(media['src'])}')); //title, artist, album
            % endif
        % endfor
        
        ## ?? the auto aggregate JSON does not have support for video? but the widget does? hu?
        ## AllanC - because the janrain social widget and the janrain json aggregator dont agree, I have added video here directly form the content obj
        %for video in [media for media in content.get('attachments',dict()) if media.get('type')=='video']:
            var video_item = new RPXNOW.Social.VideoMediaItem(
                '${clean(video.get('original_url') )}' ,
                '${clean(video.get('thumbnail_url'))}'
            );
            video_item.setVideoTitle('${clean(video.get('caption'))}');
            activity.setMediaItem(video_item);
        % endfor
        
        
        ##addLinkProperty(name, text, url)
        ##addProviderUrl('${_('_site_name')}', '${content_dict['url']}');
        
        
        var finished = function(results) {
          // Process results of publishing.
        }
        <%! import hashlib, hmac, base64, time %>        
        <%
            # Generate signiture
            # Reference - https://rpxnow.com/docs/social_publish_activity#OptionsParameter
            #           - http://stackoverflow.com/questions/1306550/calculating-a-sha-hash-with-a-string-secret-key-in-python
            if c.logged_in_persona:
                apiKey     = config['api_key.janrain']
                timestamp  = int(time.time())
                primaryKey = c.logged_in_persona.id
                message    = '%s|%s' % (timestamp,primaryKey)
                signature  = base64.b64encode(hmac.new(apiKey, msg=message, digestmod=hashlib.sha256).digest()).decode()
        %>
        
        var options = {
                        finishCallback: finished,
                        ##exclusionList: ["facebook", "yahoo"],
                        urlShortening: true,
                        % if c.logged_in_persona:
                        primaryKey: '${primaryKey}',
                        timestamp :  ${timestamp}  ,
                        signature : '${signature}'
                        % endif
                       }
        
        RPXNOW.Social.publishActivity(activity, options);

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