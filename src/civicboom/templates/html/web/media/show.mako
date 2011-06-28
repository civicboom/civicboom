<%inherit file="/html/web/common/html_base.mako"/>

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
        <img src="${media['original_url']}" alt="${media['caption']}"/>
    % elif type == "audio" or type == "video":
        ${preview(media)}
        <p>Download ${type} <a href="${media['original_url']}">${media['caption']}</a> (${filesize}MB)</p>
    % else:
        ${_("unrecognised media type: %s") % type}
    % endif
    <p>${media['caption']}<p>
    <p>Credited to ${media['credit']}</p>
</%def>
    
## ---
## Media carousel
## ---
<%def name="media_carousel(contents)">
    <ul id="media_carousel" class="jcarousel-skin-content-media">
        % for content in contents:
            ${carousel_item(content)}
        % endfor
    </ul>
    <div class="preview_details"></div>
    
    <script type="text/javascript">
        jQuery(document).ready(function() {
            jQuery('#media_carousel').jcarousel({
                scroll  :   1,
                visible :   1,
                auto    :   3,
                wrap    :   'circular',
                initCallback    :   media_carousel_initCallback,
                buttonNextHTML  :   "<div>NEXT</div>",
                buttonPrevHTML  :   "<div>LAST</div>",
            });
        });
        
        function media_carousel_initCallback(carousel) {
            // Disable autoscrolling if the user clicks the prev or next button.
            carousel.buttonNext.bind('click', function() {carousel.startAuto(0);});
            carousel.buttonPrev.bind('click', function() {carousel.startAuto(0);});
            // Pause autoscrolling if the user moves with the cursor over the clip.
            carousel.clip.hover(
                function() {carousel.stopAuto(); },
                function() {carousel.startAuto();}
            );
            jQuery('.jcarousel-control').hover(
                function() {carousel.stopAuto(); },
                function() {carousel.startAuto();}
            );
            
            jQuery('.jcarousel-control a').bind('click', function() {
                carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
                return false;
            });
        };
        
        function get_preview_details_itemVisibleInCallback(carousel, item, idx, state) {
            
        }
    </script>
</%def>

<%def name="carousel_item(content)">
    <li class="preview_item">
        <a href="${content['original_url']}" target="_blank">
            <img src="${content['thumbnail_url']}" />
        </a>
        <div class="item_details">
            <%
                caption = content['caption']
                credit = content['credit']
            %>
            % if not caption == "":
                <p class="caption">"${content['caption']}"</p>
            % endif
            % if not credit == "":
                <p class="credit">Credited to ${content['credit']}</p>
            % endif
        </div>
    </li>
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
