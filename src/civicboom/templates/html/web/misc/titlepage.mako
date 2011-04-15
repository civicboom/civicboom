<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="get_widget" file="/frag/misc/get_widget.mako"/>

<%def name="title()">${_("Welcome")}</%def>




##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	<div class="new_front">
		${new_front_headline()}
		${new_front_who_is()}
		<div class="front_sub">
			${new_front_price()}
			${new_front_tag()}
		</div>
			${new_front_key_elems()}
		<div class="front_sub">
			${new_front_plans()}
			${new_front_how_title()}
		</div>
		${new_front_how()}
		<div class="front_sub">
			${new_front_tag()}
			${new_front_you()}
			${new_front_tag()}
			<div style="margin-top: 2em"></div>
			${new_front_register()}
		</div>
	</div>
</%def>

##------------------------------------------------------------------------------
## New Front Title
##------------------------------------------------------------------------------

<%def name="new_front_headline()">
	<h1 class="headline">
		Civicboom empowers organisations to collaborate with their audience in generating real-time news, content and insight
	</h1>
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
${get_widget.widget_iframe(protocol=None, iframe_url=h.url('contents', subdomain='widget', list='assignments_active'))}
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
            <p style="font-weight: bold; font-size: 120%;">${_("_site_name empowers you connect, create and collaborate on what matters to you.")}</p>
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

