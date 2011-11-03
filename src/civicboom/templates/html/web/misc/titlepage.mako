<%inherit file="/html/web/common/html_base.mako"/>

##<%namespace name="get_widget" file="/frag/misc/get_widget.mako"/>
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

<%def name="html_class_additions()">blank_background</%def>

<%def name="title()">${_("Welcome")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    % if config['development_mode']:
        ${new_frontpage()}
    % else:
    	<div class="wrapper">
    			${front_headline()}
    			${front_windows()}
    			${front_tagline()}
    			${start_button()}
    			${social_media()}
    	</div>
    	<br />
	% endif
</%def>

##------------------------------------------------------------------------------
## New frontpage
##------------------------------------------------------------------------------

<%def name="new_frontpage()">
    <div class="content_wrapper">
        ${title()}
        ${banner()}
        ${bars()}
    </div>
    ${footer()}
</%def>

<%def name="title()">
    <div class="header">
        ## logo image
        <a href='/'>
            <img  class='logo_img'     src='${h.wh_url("public", "images/logo-v3-411x90.png")}'    alt='${_("_site_name")}'/>
        </a>
        
        ## header links
        <span class="links">
            <a>${_("About _site_name")}</a>
            <a>${_("FAQ")}</a>
            <a>${_("Blog")}</a>
            <a>${_("Contact")}</a>
            <a>${_("Log in")}</a>
        </span>
    </div>
</%def>

<%def name="banner()">
    <div class="banner">
        <img src="images/misc/titlepage/banner_graphic.png" class="graphic"/>
        <div class="text">
            <p class="headline">Connecting people that need stories with people that have them</p>
            <p class="tagline">
                This is the first line!<br />
                Oh look it's another line<br />
                There's so many lines!<br />
                What is this I don't even<br />
            </p>
        </div>
    </div>
</%def>

<%def name="bars()">
    <div class="bars">
        <div class="signup_btn">
            <div class="link_wrapper">
                <a class="main">Sign up now!</a>
                <a class="tag">What have you got to lose?</a>
            </div>
        </div>
        <div class="bar">
            <h1>Individuals</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sed dui velit, et placerat purus. Nam rhoncus metus et risus dignissim vel malesuada lectus viverra. Proin commodo laoreet elit, in iaculis ante egestas in. Sed rhoncus vehicula nulla, et dictum velit viverra a. Aliquam molestie libero id justo bibendum id auctor erat feugiat. Nulla suscipit arcu non magna sagittis vehicula. Proin tempor nisi nec ligula ornare ac fringilla ligula porta. Duis vel dolor mi, in pharetra lorem. Cras condimentum neque et sapien lobortis vel elementum odio eleifend. Quisque iaculis convallis dapibus. Etiam viverra nunc vitae nulla dictum sit amet convallis leo imperdiet. Nulla imperdiet feugiat dapibus. Nunc et urna neque, in vestibulum nunc. Aenean eu fringilla magna.</p>
        </div>
        <div class="bar">
            <h1>Organisations</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sed dui velit, et placerat purus. Nam rhoncus metus et risus dignissim vel malesuada lectus viverra. Proin commodo laoreet elit, in iaculis ante egestas in. Sed rhoncus vehicula nulla, et dictum velit viverra a. Aliquam molestie libero id justo bibendum id auctor erat feugiat. Nulla suscipit arcu non magna sagittis vehicula. Proin tempor nisi nec ligula ornare ac fringilla ligula porta. Duis vel dolor mi, in pharetra lorem. Cras condimentum neque et sapien lobortis vel elementum odio eleifend. Quisque iaculis convallis dapibus. Etiam viverra nunc vitae nulla dictum sit amet convallis leo imperdiet. Nulla imperdiet feugiat dapibus. Nunc et urna neque, in vestibulum nunc. Aenean eu fringilla magna.</p>
        </div>
        <div class="bar" style="position: absolute; top: 4em; right: 0;">
            <h1>Other</h1>
            <p>Other things can go here, still needs discussion of what~</p>
        </div>
    </div>
</%def>

<%def name="footer()">
    <div class="footer">
        <div class="footer_wrapper">
            <div class="bar">
                <h2>Sign up</h2>
                ${_('Not a member of _site_name? ')}<br /><a>${_('Sign up now for free')}</a>
            </div>
            <div class="bar">
                <h2>Explore</h2>
                Yay <a>links</a>
            </div>
            <div class="bar">
                <h2>About us</h2>
                Yay <a>links</a>
            </div>
        </div>
    </div>
</%def>
	
##------------------------------------------------------------------------------
## Start button
##------------------------------------------------------------------------------
<%def name="social_media()">
    <style type="text/css">
        #social_media {
            position: absolute;
            left: 14px;
            bottom: 10px;
        }
    </style>
    <div id="social_media">
    
        ## Facebook (Oh holy god)
        <div id="fb-root"></div>
        <script>(function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) {return;}
          js = d.createElement(s); js.id = id;
          js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));</script>
        <div class="fb-like" data-href="http://www.facebook.com/pages/Civicboom/170296206384428" data-send="false" data-layout="button_count" data-width="350" data-show-faces="true" data-font="arial"></div>
        <div style="clear: both; height: 6px;"></div>
        
        ## Google +1
        <!-- Place this tag where you want the +1 button to render -->
        <g:plusone size="medium" annotation="inline" width="350" href="https://www.civicboom.com/"></g:plusone>
        
        <!-- Place this render call where appropriate -->
        <script type="text/javascript">
          (function() {
            var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
            po.src = 'https://apis.google.com/js/plusone.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
          })();
        </script>
        <div style="clear: both; height: 2px;"></div>
    
        ## Twitter
        <a href="https://twitter.com/Civicboom" class="twitter-follow-button">Follow @Civicboom</a>
        <script src="//platform.twitter.com/widgets.js" type="text/javascript"></script>
        
    </div>
</%def>

##------------------------------------------------------------------------------
## Start button
##------------------------------------------------------------------------------
<%def name="start_button()">
	
	<div class="special_button">
		<a href="${url(controller='account', action='signin')}">
			<span class="button">
				${_("START")}
			</span>
		</a>
	</div>
</%def>
	

##------------------------------------------------------------------------------
## Download / Mobile App
##------------------------------------------------------------------------------
<%def name="downloads()">
	<div class="downloads">
		<div class="downloads-android">
			<h3>Mobile App</h3>
			<a class="button" href="/about/mobile">
				Download now
			</a>
			(Android OS)
		</div>
	</div>
</%def>

##------------------------------------------------------------------------------
## Partners
##------------------------------------------------------------------------------

<%def name="partners()">
	<div class="using-us">
		<h2>Who's using us?</h2>
		<div class="partners">
			<div class="partner" style="width: 10em; padding-right: 1em;">
				<a href="http://www.kentonline.co.uk"><img style="width:100%" src="/images/client-logo/km.png" alt="Kent Messenger" /></a>
			</div>
			<div class="partner" style="width: 18em; padding-right: 1em;">
				##<h3>Media</h3>
				<a href="http://www.kentuni.com/news/"><img style="width:100%" src="/images/client-logo/gradvine.png" alt="Gradvine" /></a>
			</div>
			<div class="partner" style="width: 18em; padding-right: 1em;">
				##<h3>Business</h3>
				<a href="http://www.fxcompared.com/civic-boom.php"><img style="width:100%" src="/images/client-logo/fx-compared.jpg" alt="FX Compared" /></a>
			</div>
		</div>
	</div>
</%def>

##------------------------------------------------------------------------------
## New Front Title
##------------------------------------------------------------------------------

<%def name="front_headline()">
	<div class="title-box">
		<%doc><h2 class="headline">
			${_("_site_name")}
		</h2></%doc>
		<img
            style="width: 684px; height: 150px; max-width: 100%;"
            src="${h.wh_url("public", "images/logo-v3-684x150.png")}"
            ## try to load the image really fast from the CDN, but for double
            ## reliability (because the logo is really important), fall back
            ## to the local copy
            onerror='this.onerror=null;this.src="/images/logo-v3-684x150.png"'
            alt="Civicboom"
        />
	</div>
</%def>

<%def name="front_windows()">
	<div class="windows">
        ${make_window("left", "/images/misc/titlepage/first_panel", "Request",
            content="Journalists, news organisations, media outlets and publishers: Need stories? Sign up and ask.")}
        <span class="symbol">+</span>
        ${make_window("center", "/images/misc/titlepage/middle_panel", "Respond",
            content="Got stories? Sign up and respond to requests for your stories - or send directly to journalists, news organisations, media outlets and publishers.")}
        <span class="symbol">=</span>
        ${make_window("right", "/images/misc/titlepage/last_panel", "Result",
            content="Publish and get published: Get news stories from source. Get closer to your audience. Work together.")}
		<div style="clear: both;"></div>
	</div>
</%def>
		
<%def name="front_tagline()">
	<div class="title-box">
		<h2 class="tagline">
			${_("Connecting people that need _articles with people that have them")}
		</h2>
	</div>
</%def>
	
## Window popups
<%def name="make_window(id, img, alt, content)">
	${popup.popup_static('', window_popup, 'title_window_'+id)}
	<a href="#" class="title_link_${id} window" id="${id}"><!--
        --><img src="${img}_s.png" alt="${alt}" align="center" /><!--
	--></a>
	<script>
	    $(".title_link_${id}").click(function() {
    		$("#title_window_${id}").modal();
            $("#title_img_${id}").attr("src", "${img}_l.png");
    		return false;
	    });
	</script>
	
	<%def name="window_popup()">
		<div style="text-align: center; font-size: 125%;">
			<div class="image_wrapper">
			    <img id="title_img_${id}" src="${img}_s.png" width="600" height="400" style="display: block; margin: auto;"/>
			    <div class="text_wrapper">${content}</div>
			</div>
			<div class="image_footer">Don't just read it. Feed it</div>
		</div>
	</%def>
</%def>
