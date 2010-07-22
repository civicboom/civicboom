<h2>${_("Share this")}</h2>

${share_link()}
${boom_button()}

<%def name="share_link()">
    <%doc>
    <ul class="bulleted_list">
      <li><a class="icon icon_diggit"       href="http://digg.com/submit?phase=2?url=${c.current_URL}"              >Diggit      </a></li>
      <li><a class="icon icon_delicious"    href="http://del.icio.us/post?url=${c.current_URL}"                     >Delicious   </a></li>
      <li><a class="icon icon_reddit"       href="http://reddit.com/submit?url=${c.current_URL}"                    >Reddit      </a></li>
      <li><a class="icon icon_stumble_upon" href="http://www.stumbleupon.com/submit?url=${c.current_URL}"           >Stumble Upon</a></li>
      <li><a class="icon icon_facebook"     href="http://www.facebook.com/share.php?u=${c.current_URL}"             >Facebook    </a></li>
      ##<li><a class="icon icon_twitter"      href="http://twitter.com/home?status=Currently reading ${c.current_URL}">Twitter     </a></li>
    </ul>
    </%doc>  
    <!-- AddThis Button BEGIN http://addthis.com/ -->
    <a class="addthis_button" href="http://addthis.com/bookmark.php?v=250&amp;username=xa-4b7acd5429c82acd"><img src="http://s7.addthis.com/static/btn/v2/lg-share-en.gif" width="125" height="16" alt="Bookmark and Share" style="border:0"/></a><script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#username=xa-4b7acd5429c82acd"></script>
    <!-- AddThis Button END -->
</%def>

<%def name="boom_button()">
    <div class="yui-g">
        
      ## Retweet button
      <div class="yui-u first">
        <script type="text/javascript" src="http://tweetmeme.com/i/scripts/button.js"></script>
      </div>
      
      ## Boom button
      <div class="yui-u">
        <% boom_count = 0 %>
        % if hasattr(c.content,"boom_count"):
          <% boom_count = c.content.boom_count %>
        % endif
        <a href="${h.url(controller='content' ,action='boom',id=c.content.id)}" title="${_("Boom this! Share this with all your Followers")}">
        <div class="boom_this">
          <span class="boom_count">${boom_count}</span>
          <p>${_("Boom this")}</p>
        </div>
        </a>
      </div>
    </div>
</%def>
