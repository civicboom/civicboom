## Methods for shareing/aggregating links
## 2 alternate companys are implemnted here should we need to swich.

<%!
    import json
    import time
    import base64
    import hmac
    import hashlib
    
    def clean_string(s):
        if isinstance(s, basestring):
            return s.replace("'", "\\\'")
        return ''
    
    def __(s):
        return s
        
share_data = {
        'user' : {
           'new': {
               'type': {
                    'assignment': "I just posted a request for _content: %(title)s on _site_name. Respond now!",
                    'response'  : "I just responded to a request for _content by %(parent_owner)s on _site_name. Get involved & add your story too!",
                    'group'     : "I just created the %(name)s Hub on _site_name. Follow it now and get involved!",
                    'user'      : "I just signed up to _site_name to get my _content published - you can too!",
                    'article'   : "I just created the content %(title)s on _site_name, check it out here!",
                },
                'tag': {
                    'assignment': "Share _assignment with your friends and followers:",
                    'response'  : "Share your _content with your friends and followers:",
                    'group'     : "Share _group with your friends and followers:",
                    'user'      : "Share your news _content with your friends and followers:",
                    'article'   : "Share _article with your friends and followers:",
                },
                'desc': {
                    'assignment': 'New _assignment on _site_name',
                    'response'  : 'New _article on _site_name',
                    'group'     : 'New _group on _site_name',
                    'user'      : "I'm on _site_name",
                    'article'   : 'New _article on _site_name',
                },
            },
            'existing': {
               'type': {
                    'assignment': "Check out my request for _content: %(title)s on _site_name. Share your _content now!",
                    'response'  : "Check out my _content - %(owner)s on _site_name. Get involved & add your _content!",
                    'group'     : "Check out my %(name)s Hub on _site_name. Follow it now and get involved!",
                    'user'      : "Check out my profile on _site_name. You can sign up too and get your _articles published!",
                    'article'   : "Check out my content %(title)s on _site_name!",
                },
                'tag': {
                    'assignment': "Share _assignment with your friends and followers:",
                    'response'  : "Share this story response with your friends and followers:",
                    'group'     : "Share _group with your friends and followers:",
                    'user'      : "Share your profile with your friends and followers:",
                    'article'   : "Share _article with your friends and followers:",
                },
                'desc': {
                    'assignment': 'My _assignment on _site_name',
                    'response'  : 'My _article on _site_name',
                    'group'     : 'My _group on _site_name',
                    'user'      : "I'm on _site_name",
                    'article'   : 'My _article on _site_name',
                },
            },
            'other': {
               'type': {
                    'assignment': "Check out %(title)s on _site_name and share your _content now!",
                    'response'  : "Check out this response to a request for a _content by %(owner)s on _site_name. Get involved & add your story!",
                    'group'     : "Check out %(name)s Hub on _site_name. Follow it now and get involved!",
                    'user'      : "Check out %(name)s on _site_name. They're getting their news published - and you can too!",
                    'article'   : "Check out %(title)s on _site_name!",
                },
                'tag': {
                    'assignment': "Share this _assignment with your friends and followers:",
                    'response'  : "Share this response with your friends and followers:",
                    'group'     : "Share this _group with your friends and followers:",
                    'user'      : "Share this news with your friends and followers:",
                    'article'   : "Share this _article with your friends and followers:",
                },
                'desc': {
                    'assignment': '_Assignment on _site_name',
                    'response'  : '_Article on _site_name',
                    'group'     : '_Group on _site_name',
                    'user'      : "Profile on _site_name",
                    'article'   : '_Article on _site_name',
                },
            },
        },
        'group' : {
           'new': {
               'type': {
                    'assignment': "We want your _content! Check out %(title)s on _site_name. Respond now for your chance to get published!",
                    'response'  : "We just shared our _content in response to %(owner)s on _site_name. Get involved & add your _content!",
                    'group'     : "We just created the %(name)s Hub on _site_name. Follow it now to share your _articles!",
                    'user'      : "We just signed up to _site_name to get _content from source - and you can too!",
                    'article'   : "We just created the content %(title)s on _site_name, check it out here!",
                },
                'tag': {
                    'assignment': "Share your _assignment with your friends and followers:",
                    'response'  : "Share your response with your friends and followers:",
                    'group'     : "Share your _group with your friends and followers:",
                    'user'      : "Share your news with your friends and followers:",
                    'article'   : "Share your _article with your friends and followers:",
                },
                'desc': {
                    'assignment': 'New _assignment on _site_name',
                    'response'  : 'New _article on _site_name',
                    'group'     : 'New _group on _site_name',
                    'user'      : "We're on _site_name",
                    'article'   : 'New _article on _site_name',
                },
            },
            'existing': {
               'type': {
                    'assignment': "Check out our request %(title)s on _site_name and share your _content!",
                    'response'  : "Check out our response to a request by %(owner)s on _site_name. Get involved & add your _content!",
                    'group'     : "Check out our %(name)s Hub on _site_name. Follow it now to share your _articles!",
                    'user'      : "Check out our profile on _site_name, join to get your news published!",
                    'article'   : "Check out our content %(title)s on _site_name!",
                },
                'tag': {
                    'assignment': "Share your _assignment with your friends and followers:",
                    'response'  : "Share your response with your friends and followers:",
                    'group'     : "Share your _group with your friends and followers:",
                    'user'      : "Share your profile with your friends and followers:",
                    'article'   : "Share your _article with your friends and followers:",
                },
                'desc': {
                    'assignment': 'Our _assignment on _site_name',
                    'response'  : 'Our _article on _site_name',
                    'group'     : 'Our _group on _site_name',
                    'user'      : "We're on _site_name",
                    'article'   : 'Our _article on _site_name',
                },
            },
            'other': {
               'type': {
                    'assignment': "Check out this _content request %(title)s on _site_name. Take a look and respond now!",
                    'response'  : "Check out this response to a request by %(owner)s on _site_name. Get involved & add your _content!",
                    'group'     : "Check out %(name)s Hub on _site_name. Get involved and follow it now!",
                    'user'      : "Check out %(name)s on _site_name. You too can sign up and get your news published!",
                    'article'   : "Check out %(title)s on _site_name!",
                },
                'tag': {
                    'assignment': "Share this _assignment with your friends and followers:",
                    'response'  : "Share this response with your friends and followers:",
                    'group'     : "Share this _group with your friends and followers:",
                    'user'      : "Share this news with your friends and followers:",
                    'article'   : "Share this _article with your friends and followers:",
                },
                'desc': {
                    'assignment': '_Assignment on _site_name',
                    'response'  : '_Article on _site_name',
                    'group'     : '_Group on _site_name',
                    'user'      : "Profile on _site_name",
                    'article'   : '_Article on _site_name',
                },
            },
        }
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
      var addthis_config = {
          ui_click: true,
          ui_cobrand: 'Civicboom'
      }
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

<%def name="AddThisLine(*args, **kwargs)">
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
    
    ## <h2>${_('Share this profile')}</h2>
    ## <div class="frag_list_contents">
        <div class="social_sharing content note addthis_toolbox" style="padding-bottom: 0px;">
        ## Boombox link generation moved to show.mako (using custom_share directly)
        <ul class="share_this">
            % for name in ['email', 'facebook', 'twitter', 'linkedin', 'compact']:
            ${sharebutton(name, **kwargs)}
            % endfor
            
        ## Janrain moved directly to show.mako too
        ## Possibly don't want to do these individually for both member and content
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
        <script>
            $(function(){
            addthis.toolbox('.addthis_toolbox');
            });
        </script>
        
        ## AllanC - had to add this back in. Why was it missing?
        ##          what a hideious hideous copy paste botch .. this needs refactoring
        % if custom_share_line:
            <div style="height: 24px">
                ${custom_share_line()}
            </div>
        % endif
        
        </div>
    ## </div>
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
##	set the ID using inline JS so that the RPX library can find it
##	whenever it eventually gets loaded (the load time is variable,
##	as it is bundled inside foot.js, which is loaded in async mode)
	<script>var janrain_app_id = '${config['app_id.janrain']}';</script>
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
    ${json.dumps(options).replace('\\\"', '&quot;').replace("'", "\\\'").replace('"', "'") | n}
</%def>
<%def name="janrain_options_noparse()">
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
    %>${json.dumps(options)}</%def>

<%def name="janrain_social_data_content(content, share_type, share_object_type)">
    <%
        persona_type = c.logged_in_persona.__type__ if c.logged_in_persona else 'user'
        share_data_type = share_data[persona_type][share_type]['type'][share_object_type]
        share_data_tag  = share_data[persona_type][share_type]['tag' ][share_object_type]
        share_data_desc = share_data[persona_type][share_type]['desc'][share_object_type]
        
        from civicboom.lib.aggregation import aggregation_dict
        cd = aggregation_dict(content, safe_strings=True)
        cd['url'] = h.url('content', id=content['id'], qualified=True)
        
        share_usergen_default = _(share_data_type) % {'title': cd.get('title'), 'owner': content['creator'].get('name'), 'parent_owner': content.get('parent',{}).get('creator',{}).get('name') }
        
        variables = {
            'share_display':              clean_string(_(share_data_tag)),
            'action_share_description':   clean_string(_(share_data_desc)),
            'share_usergen_default':      clean_string(_(share_usergen_default)),
            'action_page_title':          cd['title'],
            'action_page_description':    cd['user_generated_content'],
            'action_links':               cd['action_links'],
            'action':                     cd['action'],
            'media':                      cd['media'],
        }
    %>
    data-janrain-options="${janrain_options_noparse()}"
    data-janrain-url="${cd['url']}"
    data-janrain-variables="${json.dumps(variables)}"
</%def>

<%def name="janrain_social_data_member(member, share_type, share_object_type)">
    <%
        persona_type = c.logged_in_persona.__type__ if c.logged_in_persona else 'user'
        share_data_type = share_data[persona_type][share_type]['type'][share_object_type]
        share_data_tag  = share_data[persona_type][share_type]['tag' ][share_object_type]
        share_data_desc = share_data[persona_type][share_type]['desc'][share_object_type]
        cd = {
                'url':                      h.url('member', id=member['username'], qualified=True),
                'title':                    member['name'],
                'user_generated_content':   member['description'],
                'media':                    [ {
                                                'type': 'image',
                                                'src':  member['avatar_url'],
                                                'href': h.url('member', id=member['username'], qualified=True),
                                            }, ],
        }
        share_usergen_default = _(share_data_type) % {'name': cd['title']}
        
        variables = {
            'share_display':              clean_string(_(share_data_tag)),
            'action_share_description':   clean_string(_(share_data_desc)),
            'share_usergen_default':      clean_string(_(share_usergen_default)),
            'action_page_title':          cd['title'],
            'action_page_description':    cd['user_generated_content'],
            'action_links':               '',
            'action':                     '',
            'media':                      cd['media'],
        }
    %>
    data-janrain-options="${janrain_options_noparse()}"
    data-janrain-url="${cd['url']}"
    data-janrain-variables="${json.dumps(variables)}"
</%def>





<%doc>
<%def name="janrain_social_call_content(content, share_type, share_object_type)">
    ## Variables: share_display, share_usergen_default, action_share_description, action_page_title, action_page_description, action_links, properties, images, audio, video
    <%
        persona_type = c.logged_in_persona.__type__ if c.logged_in_persona else 'user'
        share_data_type = share_data[persona_type][share_type]['type'][share_object_type]
        share_data_tag  = share_data[persona_type][share_type]['tag' ][share_object_type]
        share_data_desc = share_data[persona_type][share_type]['desc'][share_object_type]
        
        from civicboom.lib.aggregation import aggregation_dict
        cd = aggregation_dict(content, safe_strings=True)
        cd['url'] = h.url('content', id=content['id'], qualified=True)
        
        share_usergen_default = _(share_data_type) % {'title': cd.get('title'), 'owner': content['creator'].get('name')}
    %>
    $(function() {
        var content   = ${json.dumps(cd).replace('\\\"', '&quot;').replace("'", "\\\'").replace('"', "'") | n};
        var url       = content.url;
        var variables = {
            share_display:                '${clean_string(_(share_data_tag)) | n}',
            action_share_description:     '${clean_string(_(share_data_desc)) | n}',
            share_usergen_default:        '${clean_string(_(share_usergen_default)) | n}',
            action_page_title:           content.title,
            action_page_description:     content.user_generated_content,
            action_links:                 content.action_links,
            action:                        content.action,
            media:                        content.media,
        };
        janrain_popup_share(url, ${janrain_options() | n}, variables);
    });
</%def>


<%def name="janrain_social_call_member(member, share_type, share_object_type)">
    ## Variables: share_display, share_usergen_default, action_share_description, action_page_title, action_page_description, action_links, properties, images, audio, video
    <%
        persona_type = c.logged_in_persona.__type__ if c.logged_in_persona else 'user'
        share_data_type = share_data[persona_type][share_type]['type'][share_object_type]
        share_data_tag  = share_data[persona_type][share_type]['tag' ][share_object_type]
        share_data_desc = share_data[persona_type][share_type]['desc'][share_object_type]
        cd = {
                'url':                      h.url('member', id=member['username'], qualified=True),
                'title':                    member['name'],
                'user_generated_content':   member['description'],
                'media':                    [ {
                                                'type': 'image',
                                                'src':  member['avatar_url'],
                                                'href': h.url('member', id=member['username'], qualified=True),
                                            }, ],
        }
        share_usergen_default = _(share_data_type) % {'name': cd['title']}
    %>
    $(function() {
        var content   = ${json.dumps(cd).replace('\\\"', '&quot;').replace("'", "\\\'").replace('"', "'") | n};
        var url       = content.url;
        var variables = {
            share_display:              '${clean_string(_(share_data_tag)) | n}',
            action_share_description:   '${clean_string(_(share_data_desc)) | n}',
            share_usergen_default:      '${clean_string(_(share_usergen_default)) | n}',
            action_page_title:          content.title,
            action_page_description:    content.user_generated_content,
            action_links:               content.action_links,
            action:                     content.action,
            media:                      content.media,
        };
        janrain_popup_share(url, ${janrain_options() | n}, variables);
    });
    </%def>

</%doc>

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
