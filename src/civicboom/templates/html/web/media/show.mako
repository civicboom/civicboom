<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

## Include caousel javascripts in header
<%def name="scripts_head()">
    <script type='text/javascript' src='/javascript/jquery-1.5.1.js'        ></script>
    <script type='text/javascript' src='/javascript/jquery.jcarousel.min.js'></script>
</%def>

<%def name="title()">${_("Media Viewer")}</%def>

<%def name="preview(media)">
    <%
        type =  media.get('type')
        
        media_width  = config['media.display.video.width' ]
        media_height = config['media.display.video.height']
    %>
    % if type == "image":
        <a href="${h.url('medium', id=media['hash'])}"><img src="${media['media_url']}" alt="${media['caption']}" style="max-width: ${media_width}px; max-height: ${media_height}px;"/></a>
    % elif type == "audio":
        <object type="application/x-shockwave-flash" data="/flash/player_flv_maxi.swf" width="${media_width}" height="30">
            <param name="movie" value="/flash/player_flv_maxi.swf" />
            <param name="allowFullScreen" value="true" />
            <param name="wmode" value="transparent" />
            <param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;showvolume=1&amp;showplayer=always&amp;showloading=always" />
        </object>
    % elif type == "video":
        <object type="application/x-shockwave-flash" data="/flash/player_flv_maxi.swf" width="${media_width}" height="${media_height}">
            <param name="movie" value="/flash/player_flv_maxi.swf" />
            <param name="allowFullScreen" value="true" />
            <param name="wmode" value="transparent" />
            <param name="FlashVars" value="flv=${media['media_url']}&amp;title=${media['caption']}\n${media['credit']}&amp;startimage=${media['thumbnail_url']}&amp;showvolume=1&amp;showfullscreen=1" />
        </object>
    % else:
        ${_("unrecognised media type: %s") % type}
    % endif
</%def>


<%def name="full(media)">
    <%
        type     = media.get('type')
        filesize = media.get('filesize')
        if filesize:
            filesize = float(filesize)/1024/1024
        else:
            filesize = "???"
    %>
    % if type == "image":
        <a href="${media['original_url']}"><img src="${media['original_url']}" alt="${media['caption']}"/></a>
    % elif type == "audio" or type == "video":
        ${preview(media)}
    % else:
        ${_("unrecognised media type: %s") % type}
    % endif
    ${media_details(media)}
</%def>

## ---
## Caption and credit to paragraph tags
## ---
<%def name="media_details(media, truncate=False)">
    <%
        if truncate:
            caption = h.truncate(media['caption'], length=40, indicator='...', whole_word=True)
            credit  = h.truncate(media['credit'], length=35, indicator='...', whole_word=True)
        else:
            caption = media['caption']
            credit  = media['credit']
    %>
    <table><tr>
    <td>
        % if caption:
            <p class="caption">${caption}</p>
        % endif
        % if credit:
            <p class="credit">Credited to <b>${credit}</b></p>
        % endif
    </td><td class="media_type">
        <img src="/images/misc/shareicons/carousel_${media['type']}_icon.png" class="type_icon" />
    </tr></table>
</%def>
    
## ---
## Media carousel
## ---
<%def name="media_carousel(contents, content_id)">
    % if len(contents):
        <% uid = h.uniqueish_id(content_id) %>
        <ul id="media_carousel-${uid}" class="jcarousel-skin-content-media">
            % for content in contents:
                ${carousel_item(content)}
            % endfor
        </ul>
        
        <script type="text/javascript">
            jQuery(document).ready(function() {
                jQuery('#media_carousel-${uid}').jcarousel({
                    animation   :   'slow',
                    scroll  :   1,
                    visible :   1,
                    auto    :   3,
                    wrap    :   'both',
                    initCallback    :   media_carousel_initCallback,
                    buttonNextHTML  :   "<img src='/images/misc/contenticons/carousel_next_32.png' alt='next' />",
                    buttonPrevHTML  :   "<img src='/images/misc/contenticons/carousel_prev_32.png' alt='prev' />",
                    itemVisibleInCallback   :   {
                        onAfterAnimation    :   show_preview_details_itemVisibleInCallback
                    },
                    itemVisibleOutCallback  :   {
                        onBeforeAnimation   :   hide_preview_details_itemVisibleInCallback
                    },
                    itemFallbackDimension	:	349,
                });
            });
            
            function media_carousel_initCallback(carousel) {
                // Pause autoscrolling if the user moves with the cursor over the clip.
                carousel.clip.hover(
                    function() {carousel.stopAuto();    },
                    function() {carousel.startAuto();   } 
                );
                
                $('.play_icon').fadeTo("fast", 0.5);
                $('.item_preview').hover(
                    function() { $(this).find('.play_icon').fadeTo(400, 1.0); },
                    function() { $(this).find('.play_icon').fadeTo(400, 0.5); }
                );
            };
            
            function get_item_details(item) {
                return $(item).find('.item_details');
            }
            
            function show_preview_details_itemVisibleInCallback(carousel, item, idx, state) {
                details = get_item_details(item);
                $(details).removeClass('hidden');
            }
            
            function hide_preview_details_itemVisibleInCallback(carousel, item, idx, state) {
                details = get_item_details(item);
                $(details).addClass('hidden');
            }
        </script>
    % endif
</%def>

<%def name="carousel_item(content)">
    <li class="preview_item">
        ## Media preview/link to full
        <a href="${h.url('medium', id=content['hash'])}" class="item-popup-link ${content['hash']}-popup">
            <div class="item_preview">
                % if content['type'] == "image":
                    <img src="${content['thumbnail_url']}" alt="${content['caption']}" />
                % elif content['type'] == "video":
                    <img src="${content['thumbnail_url']}" alt="${content['caption']}" />
                    <span class="play_icon"><img src="/images/misc/contenticons/play_icon.png" /></span>
                % elif content['type'] == "audio":
                    <img src="/images/misc/shareicons/audio_icon.png" alt="${content['caption']}" />
                    <span class="play_icon"><img src="/images/misc/contenticons/play_icon.png" /></span>
                % else:
                    ${_("unrecognised media type: %s") % type}
                % endif
            </div>
        </a>
        
        
        ## Popup
        <script>
            $('.${content['hash']}-popup').click(function() {
                $(this).parent().find('#view-media').modal({ onShow: function (dialog) {}});
                return false;
            });
        </script>
        ${media_popup()}
        
        ## Media details
        <div class="item_details hidden">
            ${media_details(content, truncate=1)}
        </div>
    </li>
    
    <%def name="media_popup()">
        <div id="view-media" class="hideable">
            <div class="title_bar">
                <div class="common_actions">
                    ## <a href='' title='${_('Close pop-up')}' class="icon16 i_close simplemodalClose"><span>${_("Close")}</span></a>
                    <a href='' title='${_('Close pop-up')}' class="simplemodalClose">Close</a>
                </div>
            </div>
            <div class="media_popup_content">
                ${full(content)}
            </div>
        </div>
    </%def>
</%def>

## ---
## Body
## ---
<%def name="body()">
    ##<div style="position: fixed; top: 52px; left: 10px;">
    <div style="padding: 1em;">
    ${full(d['media'])}
    </div>
    ##</div>
</%def>
