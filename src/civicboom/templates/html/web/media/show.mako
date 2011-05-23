<%inherit file="/html/web/common/html_base.mako"/>


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


<%def name="body()">
    ##<div style="position: fixed; top: 52px; left: 10px;">
    <div style="padding: 1em;">
    ${full(d['media'])}
    </div>
    ##</div>
</%def>
