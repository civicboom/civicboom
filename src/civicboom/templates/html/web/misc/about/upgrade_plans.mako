<%inherit file="base.mako"/>
<%def name="title()">${_("Payment Plans")}</%def>

<%def name="body()">
    <h1>Get more from Civicboom</h1>
    ${upgrade_details()}
</%def>


<%def name="popup()">
    <h1>Hold up!</h1>
    <p>You're trying to perform an action that is a paid-for service as part of the Premium account</p>
    ${upgrade_details()}
</%def>


<%def name="upgrade_details()">
    <p>£50.00 per month (no lengthy contracts - pay as you go).</p>
    <p>Why upgrade? In addition to the basic system, Premium account gives you: </p>
    <ul>
        <li>Unlimited requests - ask what you want, whenever you want.</li>
        <li>Create open or closed requests - these are your call-to-actions for a community, audience or customer on any topic, issue or event.</p>
        <li>Create open or closed Hubs - they are your "brand" identity</li>
        <li>Filter out weak content - disassociate from "off brand" copy...</li>
        <li>Schedule requests - plan multiple requests for campaigns, set deadlines and event dates with automated alerts</li>
    </ul>
    
    % if not c.logged_in_user:
    <p>Please sign in to upgrade you account.</p>
    % else:
    <p>If you want to upgrade, simply fill in the form below and one of our team will be in touch asap!</p>
    
    ${h.form(h.args_to_tuple(controller='misc', action='upgrade_request', format='redirect'), method='post', json_form_complete_actions="cb_frag_remove(current_element);")}
        <%
        upgrade_form_meta = (
            ('name'    , _('Name')    , ''),
            ('company' , _('Company') , '(optional)'),
            ('phone'   , _('Phone')   , ''),
            ('email'   , _('email')   , ''),
            ('industry', _('Industry'), '(optional)'),
        )
        %>
        <table>
        % for name, title, extra in upgrade_form_meta:
        <tr>
            <td>
                <label for="upgrade_${name}">${title}:</label>
            </td>
            <td>
                <input type="text" id="upgrade_${name}" name="${name}"/>${extra}<br/>
            </td>
        </tr>
        % endfor
        </table>
    ${h.end_form()}
    <input type="submit" value="Request Upgrade"/>
    % endif
    
    ##<p>We promise we'll be in touch within 24 hours - or you get a free Premium upgrade!</p>
    ##<p>Civicboom Team</p>
</%def>





<%doc>
<%
  c.upgrade_plans_title = None
  c.upgrade_plans_subtitle = None
  %>


<%def name="init_vars()">
    <%
        self.attr.title     = _('Upgrade Account')
        self.attr.icon_type = 'dialog'
    %>
</%def>

${payplans()}

<%def name="old_payplans()">
  % if c.upgrade_plans_title:
    <h1 style="font-size: 200%; text-align: center">${c.upgrade_plans_title}</h1>
  % endif
    % if c.upgrade_plans_subtitle:
    <h1 style="text-align: center">${c.upgrade_plans_subtitle}</h1>
  % endif


  <div style="text-align: left;">
  <h1>Organisations, get the Premium plan:</h1>
  <h1>&pound;50 per month</h1>
  <style>
  	ul.circle li {
  		font-size: 1.25em;
  		list-style: outside circle;
  		margin-left: 1.5em;
  		padding-bottom: 0.25em;
  	}
  </style>
  <ul class="circle">
  <li>
  	<b>Unlimited requests</b> - ask what you want, whenever you want.
  </li>
  <li>
  	<b>Create open or closed requests</b> - these are your call-to-actions for a
  	community, audience or customer on any topic, issue or event.
  </li>
  <li>
	<b>Create open or closed Hubs</b> - they are your "brand" identity
  </li>
  <li>
	<b>Collaborate</b> - with other Hubs/organisations
  </li>
  <li>
	<b>Monitor uptake</b> - know who has accepted a request prior to responding
  </li>
  <li>
	<b>Schedule requests</b> - plan multiple requests for campaigns, set deadlines and event dates with automated alerts 
  </li>
  <li>
	<b>Add audio to requests and responses</b> - both from your PC and out in the field via your mobile.
  </li>
  <li>
	<b>Filter out weak content</b> - disassociate from "off brand" copy
  </li>
  <li>
	<b>Connect directly</b> - message you Hubs and followers for cross-referencing 
  </li>
  <li>
	<b>Geolocate content</b> - view requests and responses on an interactive map 
  </li>
  <li>
	<b>Go mobile</b> - push out requests and gather content from your audience on the move
  </li>
  <li>
	<b>Build on the Civicboom API</b>	 - create your own hyperlocal pages, 
	community engagement/mapping, live feeds into multiple sites.
  </li>
  </ul>
  <div style="padding-top: 3.5em;text-align:center;" class="front_center">
  	<a class="button" style="width: 15em; font-size: 2em;" href="mailto:sales@civicboom.com">Email to register your interest</a>
  </div>
  </div>
</%def>
  
  


    ##    c.upgrade_plans_title = 'You have reached your Basic account limit for this month.'
    ##    c.upgrade_plans_subtitle = 'If you want to get more from Civicboom you can choose premium or above:'



  
</%doc>


<div class="hide_if_js">
	<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
		<a href="${h.url(controller='misc', action='about', id='civicboom')}" itemprop="url">
			<span itemprop="title">About</span>
		</a>
	</span>
	&rarr;
	<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
		<a href="${h.url(controller='misc', action='about', id='civicboom')}" itemprop="url">
			<span itemprop="title">Company</span>
		</a>
	</span>
</div>
