<%inherit file="../common/widget_border.mako"/>

% if d['list']['count'] == 0:
    ${_('No content')}
% else:
    ${content_list(d['list']['items'])}
% endif


<%def name="content_list(contents)">
    <div id="widget_carousel" class="jcarousel-skin-widget-gradient">
        <div class="jcarousel-control">
            % for i in range(len(contents)):
            <a href="#" class="icon16 i_item_unselec jcarousel-control-item_${i+1}"><span>${i+1}</span></a>
            % endfor
        </div>
        <ul>
            % for content in contents:
                ${content_item(content)}
            % endfor
        </ul>
        <a href="" class="more_link">See more requests >></a>
    </div>
    
    <script type="text/javascript">
        ## http://sorgalla.com/projects/jcarousel/
        
        ## AllanC - I wanted a control item selector that would work for multiple similtainious carousels
        ##          It looks inside it's own jcoursel to find the control items
        ##          This is used to style the items
        function get_jcarousel_control_item(item, idx) {
            return $(item).parents('.jcarousel-container').find('.jcarousel-control-item_'+idx);
        }
        
        function widget_carousel_initCallback(carousel) {
            // Disable autoscrolling if the user clicks the prev or next button.
            carousel.buttonNext.bind('click', function() {carousel.startAuto(0);});
            carousel.buttonPrev.bind('click', function() {carousel.startAuto(0);});
            // Pause autoscrolling if the user moves with the cursor over the clip.
            carousel.clip.hover(
                function() {carousel.stopAuto(); },
                function() {carousel.startAuto();}
            );
            
            jQuery('.jcarousel-control a').bind('click', function() {
                carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
                return false;
            });
        };
        
        function widget_carousel_itemVisibleInCallbackAfterAnimation(carousel, item, idx, state) {
            console.log('Item #' + idx + ' is now visible');
            get_jcarousel_control_item(item, idx).addClass('i_item_selec').removeClass('i_item_unselec');
        };
        
        function widget_carousel_itemVisibleOutCallbackAfterAnimation(carousel, item, idx, state) {
            console.log('Item #' + idx + ' is no longer visible');
            get_jcarousel_control_item(item, idx).removeClass('i_item_selec').addClass('i_item_unselec');
        };
        
        jQuery(document).ready(function() {
            jQuery('#widget_carousel').jcarousel({
                auto   : 2 ,
                wrap   : 'last' ,
                scroll : 1 ,
                visible: 1 ,
                initCallback: widget_carousel_initCallback ,
                itemVisibleInCallback: {
                    onAfterAnimation:  widget_carousel_itemVisibleInCallbackAfterAnimation
                },
                itemVisibleOutCallback: {
                    onAfterAnimation:  widget_carousel_itemVisibleOutCallbackAfterAnimation
                }
            });
            
        });
        $(".jcarousel-skin-widget-gradient LI").css({ display: "block" });
    </script>

</%def>


<%def name="content_item(content)">
    <li>
        <a href="${h.url('content', id=content['id'])}">
            <img class="thumbnail" src="${content['thumbnail_url']}" />
            <div class="details">
                <p class="title">${content['title']}</p>
                ##% if 'creator' in content and c.widget['owner']['username'] != content['creator']['username']:
                ##<p class="creator">${member_includes.by_member(content['creator'], link=False)}</p>
                ##% endif
                <p class="content">${content['content_short']}</p>
            </div>
            <p class="respond"><a href="" class="button">Click to share your story</a></p>
        </a>
        <div style="clear:both;"></div>
    </li>
</%def>


<%doc>

</%doc>