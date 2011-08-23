<%inherit file="/html/web/common/html_base.mako"/>

##<%namespace name="get_widget" file="/frag/misc/get_widget.mako"/>
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

<%def name="html_class_additions()">blank_background</%def>

<%def name="title()">${_("Welcome")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	<div class="wrapper">
			${front_headline()}
			${front_windows()}
			${front_tagline()}
			${start_button()}
	</div>
	<br />
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
            width="684" height="150"
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
		
		<div class="window_wrapper">
			<span class="symbol">+</span>
			${make_window("center", "/images/misc/titlepage/middle_panel", "Respond",
				content="Got stories? Sign up and respond to requests for your stories - or send directly to journalists, news organisations, media outlets and publishers.")}
		</div>
		
		<div class="window_wrapper">
			<span class="symbol">=</span>
			${make_window("right", "/images/misc/titlepage/last_panel", "Result",
				content="Publish and get published: Get news stories from source. Get closer to your audience. Work together.")}
		</div>
	
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
	<a href="#" class="title_link_${id}">
		<div class="window" id="${id}">
			<img src="${img}_s.png" alt="${alt}" width="300" height="200" />
		</div>
	</a>
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
