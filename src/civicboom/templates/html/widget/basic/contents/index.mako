<%inherit file="../common/widget_border.mako"/>

<%namespace name="member_includes" file="../common/member.mako"/>

## Include caousel javascripts in header
<%def name="scripts_head()">
    ##<script type='text/javascript' src='/javascript/jquery-1.5.1.js'        ></script>
    ##<script type='text/javascript' src='/javascript/jquery.jcarousel.js'></script>
</%def>

% if d['list']['count'] == 0:
    ${_('No content')}
% else:
    ${content_list(d['list']['items'])}
% endif


<%def name="content_list(contents)">
    <%doc>
    <style type="text/css">
        <%
            width  = c.widget['width'] - 12
            height = self.size_content-10
        %>
        .jcarousel-container
        
        .jcarousel-skin-tango .jcarousel-container-horizontal {
            width  : ${width}px;
        }
        .jcarousel-skin-tango .jcarousel-clip {
            overflow: hidden;
        }
        .jcarousel-skin-tango .jcarousel-clip-horizontal {
            width:  ${width}px;
            height: ${height}px;
        }
        .jcarousel-skin-tango .jcarousel-item {
            width : ${width}px;
            height: ${height}px;
        }
        
        .jcarousel-skin-tango .jcarousel-next-horizontal {
            position: absolute;
            bottom: 0px;
            right: 5px;
            width: 16px;
            height: 16px;
            cursor: pointer;
            background: transparent url(next-horizontal.png) no-repeat 0 0;
        }
        .jcarousel-skin-tango .jcarousel-next-horizontal:before {
            content: "B";
        }
        
        .jcarousel-skin-tango .jcarousel-prev-horizontal {
            position: absolute;
            bottom: 0px;
            left: 5px;
            width: 16px;
            height: 16px;
            cursor: pointer;
            background: transparent url(prev-horizontal.png) no-repeat 0 0;
        }
        .jcarousel-skin-tango .jcarousel-prev-horizontal:before {
            content: "P";
        }
    </style>
    </%doc>

    ##<div class="widget_content_assignment_list">
    ##<ul class="content_list jcarousel-skin-tango" id="widget_carousel">
    ## AllanC - buggy peice of crap!! .. UL can only have ONE class or the courasel breaks .. ***ing great
    <div id="widget_carousel_fallback_container" class="content_list">
    ##<ul id="widget_carousel" class="jcarousel-skin-tango">
    ## AllanC - WTF!!! with the ID present the js scripts bleed between iframes .. WTF WTF WTF!!!!
    <ul class="jcarousel-skin-tango">
    % for content in contents:
        ${content_item(content)}
    % endfor
    </ul>
    </div>
    ##</div>
    
    <%doc>
    <script type="text/javascript">
        ## http://sorgalla.com/projects/jcarousel/
        
        function widget_carousel_initCallback(carousel) {
            // Disable autoscrolling if the user clicks the prev or next button.
            carousel.buttonNext.bind('click', function() {carousel.startAuto(0);});
            carousel.buttonPrev.bind('click', function() {carousel.startAuto(0);});
            // Pause autoscrolling if the user moves with the cursor over the clip.
            carousel.clip.hover(
                function() {carousel.stopAuto(); },
                function() {carousel.startAuto();}
            );
        };
        
        jQuery(document).ready(function() {
            jQuery('#widget_carousel').jcarousel({
                auto: 2,
                wrap: 'last',
                scroll: 1,
                visible: 1,
                initCallback: widget_carousel_initCallback,
            });
            
        });
        jQuery('#widget_carousel_fallback_container').removeClass('content_list');
    </script>
    </%doc>
</%def>

<%def name="content_item(content)">
    ##<a href="${url('content', id=content['id'])}">${content['id']}</a>
    ##${content['title']}
    <li style="border-bottom: 1px solid #${c.widget['color_border']};">
            <a href="${h.url('content', id=content['id'])}">
        ##<td>
                <img class="thumbnail" src="${content['thumbnail_url']}" style="border: 1px solid #${c.widget['color_border']};"/>
        ##</td>
        ##<td>
            
                <div class="details">
                    <p class="title">${content['title']}</p>
                    ##<div style="clear: both;"></div>
                    % if 'creator' in content and c.widget['owner']['username'] != content['creator']['username']:
                    <p class="creator">${member_includes.by_member(content['creator'], link=False)}</p>
                    % endif
                    <p class="content">${content['content_short']}</p>
                </div>
            </a>
        ##</td>
        <div style="clear:both;"></div>
    </li>
</%def>