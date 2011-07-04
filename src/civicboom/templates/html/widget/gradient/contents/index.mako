<%inherit file="../common/widget_border.mako"/>

## Include caousel javascripts in header
<%def name="scripts_head()">
    <script type='text/javascript' src='/javascript/jquery-1.5.1.js'        ></script>
    <script type='text/javascript' src='/javascript/jquery.jcarousel.min.js'></script>
</%def>

## AllanC - this isnt the best way to enforce a limit ... should be at API level .. short term fix only
<% limit = 8 %>
% if d['list']['count'] == 0:
    ${_('Check out all of our _assignments here! Coming soon.')}
% else:
    ${content_list(d['list']['items'][:limit])}
% endif


<%def name="content_list(contents)">
    <div id="widget_carousel" class="jcarousel-skin-widget-gradient">
        <div class="jcarousel-control">
            % for i in range(len(contents)):
            <a href="#" class="item_feedback item_unselected jcarousel-control-item_${i+1}"><span>${i+1}</span></a>
            % endfor
        </div>
        <ul>
            % for content in contents:
                ${content_item(content)}
            % endfor
        </ul>
        <a href="${h.url('member', id=c.widget['owner']['username'], sub_domain='www')}" target="_blank" class="more_link">See more requests >></a>
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
            jQuery('.jcarousel-control').hover(
                function() {carousel.stopAuto(); },
                function() {carousel.startAuto();}
            );
            
            jQuery('.jcarousel-control a').bind('click', function() {
                carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
                return false;
            });
        };
        
        function widget_carousel_itemVisibleInCallbackAfterAnimation(carousel, item, idx, state) {
            ##console.log('Item #' + idx + ' is now visible');
            ##console.log((idx % carousel.size())+1);
            get_jcarousel_control_item(item, idx).addClass('item_selected').removeClass('item_unselected');
        };
        
        function widget_carousel_itemVisibleOutCallbackAfterAnimation(carousel, item, idx, state) {
            ##console.log('Item #' + idx + ' is no longer visible');
            get_jcarousel_control_item(item, idx).removeClass('item_selected').addClass('item_unselected');
        };
        
        jQuery(document).ready(function() {
            jQuery('#widget_carousel').jcarousel({
                auto   : 3 ,
                wrap   : 'last' ,
                ##wrap   : 'circular',
                ## AllanC circular ****s up the numbering and scrolling after a number of cycles
                scroll : 1 ,
                visible: 1 ,
                initCallback: widget_carousel_initCallback ,
                itemVisibleInCallback: {
                    onAfterAnimation:  widget_carousel_itemVisibleInCallbackAfterAnimation
                },
                itemVisibleOutCallback: {
                    onAfterAnimation:  widget_carousel_itemVisibleOutCallbackAfterAnimation
                },
                itemFallbackDimension: 260,
            });
            ## itemFallbackDimension, it dosnt seem to ever be needed but it stops the following error
            ## http://stackoverflow.com/questions/3784925/jcarousel-no-width-height-set-for-items-this-will-cause-an-infinite-loop-abort
        });
        $(".jcarousel-skin-widget-gradient LI").css({ display: "block" });
    </script>
</%def>


<%def name="content_item(content)">
    <li>
        <a href="${h.url('content', id=content['id'], sub_domain='www')}" target="_blank">
            <div class="thumbnail_border"><div class="padding"><img class="thumbnail" src="${content['thumbnail_url']}" /></div></div>
            <div class="details">
                <p class="title">${h.truncate(content['title']  , length=60, indicator='...', whole_word=True)}</p>
                ##% if 'creator' in content and c.widget['owner']['username'] != content['creator']['username']:
                ##<p class="creator">${member_includes.by_member(content['creator'], link=False)}</p>
                ##% endif
                ##<p class="content">${content['content_short']}</p>
            </div>
            <p class="respond"><a href="${h.url('new_content', parent_id=content['id'], sub_domain='www')}" target="_blank" class="button">Click to share your story</a></p>
        </a>
        <div style="clear:both;"></div>
    </li>
</%def>