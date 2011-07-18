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
		##<div class="content">
			${front_headline()}
			${front_windows()}
			${front_tagline()}
			${start_button()}
			
			## Who's using us and mobile download prompt
			<%doc>
			<div style="width:100%;left:0;bottom:17px;position:fixed;padding:1.5em 0 0 0;background-color:#cee2fa;">
				<div style="width:100%;height:10em;background-color:#adcef7;">
					<div style="width:61em;padding:1em 0 1em 0;margin: auto;">
						${partners()}
						${downloads()}
					</div>
				</div>
			</div>
			</%doc>
		##</div>
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
				START
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
		<img src="images/logo_new.png" alt="Civicboom.com"/>
	</div>
</%def>

<%def name="front_windows()">
	<div class="windows">
		${make_window("left", "/images/misc/titlepage/first_panel.png", "Request",
			content="Journalists, news organisations, media outlets and publishers: Need stories? Sign up and ask.")}
		
		<div class="window_wrapper">
			<span class="symbol">+</span>
			${make_window("center", "/images/misc/titlepage/middle_panel.png", "Respond",
				content="Got stories? Sign up and respond to requests for your stories - or send directly to journalists, news organisations, media outlets and publishers.")}
		</div>
		
		<div class="window_wrapper">
			<span class="symbol">=</span>
			${make_window("right", "/images/misc/titlepage/last_panel.png", "Get published",
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
			<img src="${img}" alt="${alt}" />
		</div>
	</a>
	<script>
	    $(".title_link_${id}").click(function() {
    		$("#title_window_${id}").modal();
    		return false;
	    });
	</script>
	
	<%def name="window_popup()">
		<div style="text-align: center; font-size: 125%;">
			<div class="image_wrapper">
			    <img src="${img}" style="width: 600px; display: block; margin: auto;"/>
			    <div>${content}</div>
			</div>
			<div class="image_footer">Don't just read it. Feed it</div>
		</div>
	</%def>
</%def>
	
##------------------------------------------------------------------------------
## New Front Title
##------------------------------------------------------------------------------

<%def name="new_front_headline()">
	<div class="title-box">
		<h1 class="headline">
			Sourcing and sharing news just got easier
		</h1>
		<h2 class="tagline">
			Respond to requests and generate news or feature content for your needs.
		</h2>
	</div>
</%def>

<%def name="new_front_about()">
	<script>
		$(function() {
			$('.tab-title').each(function (index, element) {
				$(element).css('top', (index * 2)+"em");
			});
			//$('#signupnow').css('top', (($('.tab-title').length+1)*5) + "em");
			$('.tab-title').mouseover(function () {
				$(this).addClass('hilite');
				$('.tab-title').not(this).removeClass('hilite');
				var tag = '#tab-page-' + $(this).attr('id').replace('tab-title-','');
				$(tag).find('.content').show();
				$('.tab-page').not(tag).find('.content').hide();
			});
			$('.tab-title:first').trigger('mouseover');
		});
	</script>

	<style>
		.tab-title {
			display: inline;
			font-size: 200%;
			position: absolute;
			left: 0;
			width: 6.75em;
			padding: 0.25em 0 0.25em 0.25em;
			font-weight: bold;
		}
		.tab-title.hilite {
			background-color: #cee2fa; /*adcef7 cee2fa*/
		}
		.tab-page {
			padding-left: 14em;
		}
		.tab-page .content {
			background-color: #cee2fa;
			padding: 1em 0 0 1em;
			height: 18em;
		}
		.tab-page .content .left {
			width: 18em;
			padding-left: 1em;
			float: left;
		}
		.tab-page .content .right {
			padding-left: 18em;
			width: 18em;
		}
		.tab-page .content ul li {
			padding-bottom: 1em;
		}
		.tab-page .content ol {
			list-style-position: outside;
			margin-left: -1.5em;
		}
		.tab-page .content .larger {
			font-size: 125%;
		}
		.tab-page .content .hilite {
			color: #c77b01;
			font-weight: bold;
		}
		
		.tab-page .content input {
			margin: 0.5em 0 0.5em 0;
		}
		
		.tab-page .content .indent {
			padding-left: 0em;
		}
		.tab-page .content iframe {
			border: 0;
			padding: 0;
			margin: 0;
			position: relative;
			top: -0.75em;
			left: -5.75em;
		}
	</style>

	<div style="margin: 1em auto 0 auto; width: 61em; text-align: left;">
		<div style="height:15em;">
			<div style="position: absolute">
				<div class="tab-page" id="tab-page-orgs">
					<a class="tab-title" id="tab-title-orgs">Organisations</a>
					<div class="content">
						<div class="left" style="width: 20em; float: left;">
							<ul style="font-size: 125%">
								<li>
									<span class="larger"><span class="hilite">Multi-media</span> interaction</span><br />
									<span class="indent">with your audience.</span>
								</li>
								<li>
									<span class="larger"><span class="hilite">Secure</span> communication</span><br />
									<span class="indent">from trusted followers.</span>
								</li>
								<li>
									<span class="larger"><span class="hilite">Real-time</span> contribution</span><br />
									<span class="indent">from your users.</span>
								</li>
							</ul>
						</div>
						<div class="right" style="font-size: 125%">
							<span class="hilite larger">Get started!</span><br/>
							<ol style="height: 10em; width: 100%;border-left: 2em;">
								<li>Sign up as a user.</li>
								<li>Create a Hub for your organisation, title, publication...</li>
								<li>Create a request.</li>
								<li>Embed the unique widget containing your requests on websites and blogs for your community to respond to!</li>
							</ol>
						</div>
					</div>
				</div>
				<div class="tab-page" id="tab-page-indvs">
					<a class="tab-title" id="tab-title-indvs">Individuals</a>
					<div class="content">
						<div class="left" style="width: 20em; float: left;">
							<ul style="font-size: 125%">
								<li>
									<span class="larger"><span class="hilite">Participate</span> and share</span><br />
									<span class="indent">your local news.</span>
								</li>
								<li>
									<span class="larger"><span class="hilite">Interact</span> and respond</span><br />
									<span class="indent">to breaking news requests.</span>
								</li>
								<li>
									<span class="larger"><span class="hilite">Gain</span> recognition</span><br />
									<span class="indent">from content publishers.</span>
								</li>
							</ul>
						</div>
						<div class="right" style="font-size: 125%">
							<span class="hilite larger">Get started!</span><br/>
							<ol style="height: 10em; width: 100%;border-left: 2em;">
								<li>Sign up as a user.</li>
								<li>Browse requests.</li>
								<li>Respond and share your news.</li>
								<li>Set requests for others to respond to & upload your news content to share.</li>
							</ol>
						</div>
					</div>
				</div>
				<div class="tab-page" id="tab-page-signup">
					<a class="tab-title" id="tab-title-signup" style="color:#c77b01">Sign up now!</a>
					<div class="content">
						<div class="left" style="width: 20em; float: left;">
							<form method="post" action="/register/email.redirect">
							<span style="font-size: 150%; font-weight: bold;">Username</span><br />
							<input id="username_register" type="text" placeholder="Your desired username" name="username"><br />
							<span style="font-size: 150%; font-weight: bold;">Email address</span><br />
							<input id="email_signup" type="email" placeholder="Your email address" name="email"><br />
							<input class="button" type="submit" value="Sign up" name="submit">
							</form>
						</div>
						<div class="right" style="font-size: 125%">
							% if 'api_key.janrain' in config:
								% if config['online']:
									${h.get_janrain(lang=c.lang, return_url=h.url(controller='account', host=c.host, protocol='https', action='signin'))}
								% else:
									<img src="/images/test/janrain.png">
								% endif
							% endif
						</div>
					</div>
				</div>
				<div style="text-align: right; font-size: 175%; font-weight: bold; margin-top: 0.5em;">
					Don't just read it. Feed it.
				</div>
			</div>
		</div>
	</div>
</%def>

##------------------------------------------------------------------------------
## New Front Title
##------------------------------------------------------------------------------

<%def name="who()">
    <li class="who">
        <div class="who_title">
        	<h3>
            	${caller.title()}
            </h3>
        </div>
        <div class="who_logo">
        	${caller.logo()}
        </div>
        <div class="who_description">
            ${caller.description()}
        </div>
    </li>
</%def>

<%def name="what()">
    <li class="who what">
        <div class="who_title">
        	<h3>
            	${caller.title()}
            </h3>
        </div>
        <div class="what_description">
            ${caller.description()}
        </div>
    </li>
</%def>

<%def name="new_front_who_is()">
	<div class="who_is">
		<h1>Who's using us...</h1>
		<ul>
			<%self:who>
		        <%def name="title()">
		            Media
		        </%def>
		        <%def name="logo()">
		            <a href="http://www.gradvine.com"><img src="/images/client-logo/gradvine.png" alt="Gradvine" /></a>
		        </%def>
		        <%def name="description()">
		            <h4>
		            	Jo Dennis<br />
		            	Gradvine Director:
		            </h4>
		            <p>
			            "Value for students is not only to publish or have their news or views heard, there are so many hot topics on a local level.
						We use Civicboom API to create and online portfolio and that will add value to our site - and to students employability."
					</p>
		        </%def>
		    </%self:who>
			<%self:who>
		        <%def name="title()">
		            Business
		        </%def>
		        <%def name="logo()">
		            <a href="http://www.fxcompared.com/civic-boom.php"><img src="/images/client-logo/fx-compared.jpg" alt="FX Compared" /></a>
		        </%def>
		        <%def name="description()">
		            <h4>
		            	Huw Jenkins<br />
		            	FX Compared Director:
		            </h4>
		            <p>
			            "Whilst still in its beta phase the Civicboom service is exceptional. It’s intuitive and I see potential in many areas."
					</p>
		        </%def>
		    </%self:who>
			<%self:who>
		        <%def name="title()">
		            Events
		        </%def>
		        <%def name="logo()">
		            <a href="http://www.kent2020.co.uk"><img src="/images/client-logo/kent2020.gif" alt="Kent 2020 Vision" /></a>
		        </%def>
		        <%def name="description()">
		            <h4>
		            	Kent 2020 Vision<br />
		            	The Place to do Business
		            </h4>
		            <p>
						Maximise YOUR business opportunities at the largest conference and business to business exhibition in the South East.
						A great day for learning, networking and reaching new customers.
					</p>
		        </%def>
		    </%self:who>
			<%self:what>
		        <%def name="title()">
		            Why Civicboom
		        </%def>
		        <%def name="description()">
		        	<ul>
		        		<li><b>Build</b> an interactive relationship with your audience</li>
		        		<li><b>Create</b> secure requests for trusted followers of your hub</li>
		        		<li><b>Encourage</b> a dynamic, creative workforce</li>
		        		<li><b>Tap into</b> the collaborative power, talent and knowledge of your community.</li>
		        	</ul>
		        </%def>
		    </%self:what>
		</ul>
		<div style="clear: both;"></div>
	</div>
</%def>

<%def name="new_front_price()">
	<div class="center">
		<a class="buttongreen price_banner" href="/about/plans">
			No long term contracts<br />Plug-and-go starts from &pound;50/month
		</a>
	</div>
</%def>

<%def name="new_front_tag()">
	<div class="center tag">
		<h2>Don't just read it. Feed it.</h2>
	</div>
</%def>

<%def name="new_front_key_elems()">
	<%def name="new_front_widget()">
		<iframe name='Civicboom' title='Civicboom Widget' src='https://widget.civicboom.com/contents?w_base_list=content_and_boomed&amp;w_color_font=000&amp;w_color_action_bar=ddd&amp;w_owner=&amp;w_title=Get+involved&amp;w_color_content=eee&amp;w_width=160&amp;w_height=300&amp;w_color_border=ccc&amp;w_color_header=ccc/content_and_boomed?w_title=Get%20involved&w_color_border=ccc&w_color_header=ccc&w_color_action_bar=ddd&w_color_content=ffffff&w_color_font=000&w_width=160&w_height=250' width='160' height='250' scrolling='no' frameborder='0'></iframe>
	</%def>
	<div style="width: 70em; margin: 0 auto 0 auto;">
		<div style="float: left;"><img src="/images/misc/mobile_android.png" /></div>
		<div style="text-align:left; width: 25em; margin: 1em auto 0 auto; font-size: 1.5em;">
			<h3>Mobile</h3>
			<p>
				With Civicboom’s mobile app you can respond to requests and notifications, plus set request straight from your phone.
				You can also respond with an audio recording * – a speedy alternative to text.
			</p>
		</div>
		<div style="clear: both; padding-top: 2em; border-bottom: 1px solid black; margin-bottom: 2em;"></div>
		<div style="padding-left: 2em; float: right;">${new_front_widget()}</div>
		<div style="text-align:left; width: 25em; margin: 0 auto 0 auto; font-size: 1.5em;">
			<h3>Widget</h3>
			<p>
				The Civicboom widget is designed to let you explore and display requests associated with your interests directly on your own site.
				This means your community is never more than a click away from sharing their news and insight with you.
			</p>
		</div>
		<div style="clear: both; padding-top: 2em; border-bottom: 1px solid black; margin-bottom: 2em;"></div>
		<div style="float: left;"><img src="/images/misc/hub-screen2.png" /></div>
		<div style="text-align:left; width: 25em; margin: 0 auto 0 auto; font-size: 1.5em;">
			<h3>Hub</h3>
			<p>
				Civicboom’s unique Hub system allows you to create a customised
				"group" for others to Follow – be it for news titles, business, local
				groups, sports clubs – whatever is relevant to you and your
				audience. Hubs can be subdivided so different levels of interaction
				can happen within the same "group". For example, if newspaper A
				creates a Hub, it can also create five Sub-Hubs for different teams to
				work in. All the content generated by those Hubs can then be fed back
				to the main Hub, allowing free discussion and contribution from multiple
				sources whilst retaining focus and order.
			</p>
			<p style="font-size: 0.5em; padding: 1em 0 4em 0">* May 2011.</p>
		</div>
		<div style="clear: both;"></div>
	</div>
</%def>

<%def name="new_front_how_title()">
	<div class="tag center">
		<h2>
			Civicboom is the innovative tool that allows
			creative, collaborative interaction between
			businesses, colleagues and communities. Here's how:
		</h2>
	</div>
</%def>

<%def name="how()">
	<div style="float: left; margin-right: 1em; width: 17em;">
		<div style="height: 5em">
			<h3>${caller.title()}</h3>
			<p>${caller.description()}</p>
		</div>
		<div class="border" style="height: 15.5em; overflow:hidden;">
			<img style="width: 90%;" src="${caller.image()}" />
		</div>
	</div>
</%def>

<%def name="new_front_how()">
	<div style="width: 54em; margin: 0 auto 0 auto; font-size: 1.25em;">
		<div style="width:54em; margin: 0 auto 0 auto;">
			<%self:how>
				<%def name="title()">Manage your account:</%def>
				<%def name="description()">
					All Hubs, content, responses, followers and requests in one place...
				</%def>
				<%def name="image()">/images/misc/screens/manage.png</%def>
			</%self:how>
			<%self:how>
				<%def name="title()">Create Hubs:</%def>
				<%def name="description()">
					Use preset suggestions to help choose the best Hub settings...
				</%def>
				<%def name="image()">/images/misc/screens/create.png</%def>
			</%self:how>
			<%self:how>
				<%def name="title()">Schedule requests:</%def>
				<%def name="description()">
					Plan your requests and set them according to dates...
				</%def>
				<%def name="image()">/images/misc/screens/schedule.png</%def>
			</%self:how>
		</div>
		<div style="clear: both; height: 1em;"></div>
		<div style="width:54em; margin: 0 auto 0 auto;">
			<%self:how>
				<%def name="title()">Use the RSS feed:</%def>
				<%def name="description()">
					View your feeds even when your not on Civicboom...
				</%def>
				<%def name="image()">/images/misc/screens/rss.png</%def>
			</%self:how>
			<%self:how>
				<%def name="title()">Create private requests:</%def>
				<%def name="description()">
					Set request for your trusted followers to respond to...
				</%def>
				<%def name="image()">/images/misc/screens/private.png</%def>
			</%self:how>
			<%self:how>
				<%def name="title()">We have an API:</%def>
				<%def name="description()">
					Developers can use our data to build new and exciting tools...
				</%def>
				<%def name="image()">/images/misc/screens/api.png</%def>
			</%self:how>
		</div>
		<div style="clear: both;"></div>
	</div>
</%def>

<%def name="new_front_you()">
	<div class="new_you" style="font-size: 1.25em; padding-top: 1em;">
		<h1>Civicboom for organisations</h1>
		<p>
			<b>Collaborate with your audience.</b> Engage colleagues, customers or your community in generating
			and organising relevant content; Civicboom enables your audience to be creators and contributors to the
			wider conversation, not just passive consumers.
		</p>
		<p>
			<b>Promote your business.</b> Get your message out there. Use Civicboom to keep your audience informed
			about all the latest offers, events and developments you have going on; think of it like an interactive
			newsletter.
		</p>
		<p>
			<b>Encourage a dynamic, creative workforce.</b> Civicboomʼs internal communications system allows
			colleagues to develop ideas interactively rather than through clunky emails or instant messaging.
			You can even invite your wider audience to participate. 
		</p>
		<p>
			<b>Divide workloads.</b> With it's capability to have Hubs within other Hubs, Civicboom makes it easy to
			manage and distribute requests and content.	Not only can your audience then share ideas between themselves
			but also with followers, members of	other Hubs, organisations and audiences.
		</p>
		<h1>Civicboom for individuals</h1>
		<p>
			<b>Get inspired.</b> Search our database to find the requests and responses you want to engage with.
		</p>
##		<p>
##			<b>Get talking.</b> Tired of not knowing anyone that shares your love of Norwegian folk music? Find others
##			that share your interests, engage in lively discussion or just engage with others on  about anything and
##			everything.
##		</p>
		<p>
			<b>Get viewing.</b> See what other people are requesting - via your mobile or online - and share your feedback,
			views or insight as rich media.
		</p>
		<p>
			<b>Get creating.</b> The Hub feature allows users to create communities dedicated to specific subjects and finding people
			who want to discuss your interests and opinions has never been easier.
		</p>
	</div>
</%def>

<%def name="new_front_plans()">
	<div style="text-align:center;" class="front_center">
		<a class="button" style="width: 15em; font-size: 2em;" href="/about/plans">See full plan and pricing</a>
	</div>
</%def>

<%def name="new_front_register()">
	<div style="text-align:center;" class="front_center">
		<a class="button" style="width: 15em; font-size: 2em;" href="mailto:sales@civicboom.com">Email to register your interest</a>
	</div>
</%def>

## Beyond this fair comment is the old front scroll


##------------------------------------------------------------------------------
## What is
##------------------------------------------------------------------------------

<%def name="assignments_active()">
<%
    c.widget['title' ] = _('Get involved with the latest _assignments on _site_name')
    c.widget['width' ] = 160
    c.widget['height'] = 250
%>
##<div style="padding: 1em;">
${get_widget.widget_iframe(protocol=None, iframe_url=h.url('contents', sub_domain='widget', list='assignments_active'))}
##</div>
</%def>

##------------------------------------------------------------------------------
## What is
##------------------------------------------------------------------------------

<%def name="what_is()">
    <section class='description'>
        <div style="float: right; padding-bottom: 1em;">
            <a class="button" href="${url(controller='account', action='signin')}">${_('Sign up')}</a>
        </div>
        
        <div class='description_container'>
            <h1>${_('What is _site_name?')}</h1>
            <div class="steps_container">
                <div id="step_container">
                    <ul>
                        ${steps()}
                    </ul>
                </div>
                
                <a class="step_nav step_back" onclick="step_back(); return false;">&lt;</a>
                <a class="step_nav step_next" onclick="step_next(); return false;">&gt;</a>
                
                <script type="text/javascript">
                    var class_current = 'current';
                    function step_remove_current() {
                        var container = $('#step_container');
                        var current = container.find('.'+class_current);
                        current.removeClass(class_current);
                        current.fadeOut();
                        return current;
                    }
                    function step_next() {
                        var current = step_remove_current();
                        var next    = current.next();
                        if (!next.length) {next = $('#step_container ul li:first-child');}
                        next.addClass(class_current);
                        next.fadeIn();
                    }
                    function step_back() {
                        var current = step_remove_current();
                        var prev    = current.prev();
                        if (!prev.length) {prev = $('#step_container ul li:last-child');}
                        prev.addClass(class_current);
                        prev.fadeIn();
                    }
                    $('.step_next').click();
                </script>
                
                ##<div style="clear:both"></div>
            </div>
        </div>
        
        <a style="float:right;" class="button" href="${url(controller='misc', action='about')}">${_('Learn more')}</a>
        <p style="font-size: x-large; font-weight: bold;">${_("Don't just read it. Feed it.")}</p>
        
        <div style="clear: both; padding: 0.5em;"></div>
        
        <a style="float:right; color: black; background: none;" class="button" href="mailto:contact@civicboom.com">${_('Get in touch')}</a>
        <p style="font-weight: bold;">${_('Are you an organisation? Do you want to know how _site_name can help you?')}</p>
    </section>
</%def>





##------------------------------------------------------------------------------
## Mobile
##------------------------------------------------------------------------------

<%def name="mobile()">
    <section class="mobile">
        
        <h2>${_('Grab the _site_name app')}</h2>
        <a href="${url(controller='misc', action='about', id='mobile')}">
            <img src="/images/misc/mobile_android.png" width="93" height="171">
        </a>
        <p>${_('Coming soon:')}</p>
        <ul>
            <li>Blackberry</li>
            <li>iPhone</li>
        </ul>
        
    </section>
</%def>


##------------------------------------------------------------------------------
## Steps
##------------------------------------------------------------------------------

<%def name="step()">
    ##% for s in range(3):
    <li class="step hideable">
        <div class="step_main">
            <div class="step_padding">
                ${caller.main()}
            </div>
        </div>
        <div class="step_description">
            <div class="step_padding">
                ${caller.description()}
            </div>
        </div>
    </li>
    ##% endfor
</%def>


<%def name="steps()">

    <%doc>
    <%self:step>
        <%def name="main()">
            <div style="text-align: center; margin-top: 3em;"><img src="/images/boom193.png" alt="${_("_site_name logo")}" width="193" height="193" /></div>
        </%def>
        <%def name="description()">
            <p style="font-weight: bold; font-size: 120%;">${_("_site_name empowers you to connect, create and collaborate on what matters to you.")}</p>
        </%def>
    </%self:step>
    </%doc>


    <%self:step>
        <%def name="main()">
            <img src="images/misc/titlepage/step1.png" alt="step 1"/>
        </%def>
        <%def name="description()">
            <h2>Civicboom empowers you to connect and collaborate with your community and audience on what matters...</h2>
        </%def>
    </%self:step>    

    <%self:step>
        <%def name="main()">
            <img src="images/misc/titlepage/step2.png" alt="step 2"/>
        </%def>
        <%def name="description()">
            <h2>Local news media: get closer to your community</h2>
            <p>Create Hubs for your titles, sections or issues.</p>
            <p>Send out breaking news requests, get coverage directly from the source and utilise the power of the crowd.</p>
            <p>Empower the community you serve to be part of news and its creation - then create relevant, timely and enhanced content.</p>
        </%def>
    </%self:step>    
    
</%def>

