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
<%def name="AddThis(url=None, title=None, description=None)">
    <!-- AddThis Button BEGIN -->
    <div class="addthis_toolbox addthis_default_style " style="display: inline-block;"
    % if url:
        addthis:url         = "${url}"
    % endif
    % if title:
        addthis:title       = "${title}"
    % endif
    % if description:
        addthis:description = "${description}"
    % endif
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
<%def name="ShareThis(url=None, title=None, description=None)">
    
    ##<span class="st_email"></span>
    ##<span class="st_facebook"></span>
    ##<span class="st_twitter"></span>
    
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
            % if url:
            st_url     : '${url}' ,
            % endif
            % if title:
            st_title   : '${title}' ,
            % endif
            % if description:
            displayText: '${description}',
            % endif
        });
    </script>
    
    ## http://forums.sharethis.com/topic.php?id=261
</%def>