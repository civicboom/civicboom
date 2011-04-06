<%def name="init_vars()">
    <%
        self.attr.title     = _('Upgrade Account')
        self.attr.icon_type = 'dialog'
    %>
</%def>

${payplans()}

<%def name="payplans()">
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

<%def name="old()">

  <div class="payplanwrapper">
    
    <div class="payplanholder">
      <!---
      <div class="payplan" id="planbasic">
        <div class="plantitle">
          Basic<br />
          <span class="subtitle">Free</span>
        </div>
        <div class="planpoints">
          <ul class="points">
            <li>Up to 5 requests per month</li>
            <li>Audio requests and responses</li>
            <li>Unlimited Hubs</li>
          </ul>
          <div class="buttons">
            <div class="ideal">
              <div class="idealpop">
                <div class="pop">
                  <ul>
                    <li>Local events</li>
                    <li>Festivals</li>
                    <li>Societies / clubs</li>
                    <li>Amateur sports clubs</li>
                    <li>Hyperlocal news</li>
                    <li>Bloggers</li>
                    <li>Interest groups</li>
                    <li>Students</li>
                  </ul>
                </div>
              </div>
              <div class="buttongreen">Ideal for...</div>
            </div>
          </div>
        </div>
        --->
      </div>
      
      <div class="payplan active" id="planprem">
        <div class="plantitle">
          Premium<br />
          <span class="subtitle">£50/month - includes Basic</span>
        </div>
        <div class="planpoints">
          <ul class="points">
            <li>Unlimited requests per month</li>
            <li>Scheduled & Closed requests</li>
            <li>Sponsored requests</li>
            <li>Another here</li>
          </ul>
          <div class="buttons">
            <div class="ideal">
              <div class="idealpop">
                <div class="pop">
                  <ul>
                    <li>News and media orgs</li>
                    <li>Creative agencies</li>
                    <li>SMEs</li>
                    <li>Charities *</li>
                    <li>Local authorities</li>
                    <li>Professional sports orgs</li>
                    <li>Marketing / research orgs</li>
                    <li>Educational establishments</li>
                  </ul>
                  <br />
                  <span style="font-size: 80%">* Premium is free for charities</span>
                </div>
              </div>
              <div class="buttongreen">Ideal for...</div>
            </div>
            <div class="buttonpad"></div>
            <a href="mailto:payment@civicboom.com?Subject=Premium Upgrade" class="button">Choose</a>
          </div>
        </div>
      </div>
      <!---
      <div class="payplan" id="plancorp">
        <div class="plantitle">
          Corporate<br />
          <span class="subtitle ital">Coming soon</span>
        </div>
        <div class="planpoints">
          <ul class="points">
            <li>Flexible upload</li>
            <li>Sponsored assignments</li>
            <li>Intranet integration</li>
            <li>Deep analysis</li>
          </ul>
          <div class="buttons">
            <div class="ideal">
              <div class="idealpop">
                <div class="pop">
                  <ul>
                    <li>Large media orgs</li>
                    <li>Corporations</li>
                  </ul>
                </div>
              </div>
              <div class="buttongreen">Ideal for...</div>
            </div>
          </div>
        </div>
      </div>
      --->
##      <div class="payplan"  id="plancorpplus">
##        <div class="plantitle">
##          Corporate plus<br />
##          <span class="subtitle ital">Coming soon</span>
##        </div>
##        <div class="planpoints">
##          <ul class="points">
##            <li>More details coming soon...</li>
##          </ul>
##          <div class="buttons">
##            <div class="ideal">
##              <div class="idealpop">
##                <div class="pop">
##                  <ul>
##                    <li>Large media orgs</li>
##                    <li>Corporations</li>
##                  </ul>
##                </div>
##              </div>
##              <div class="buttongreen">Ideal for...</div>
##            </div>
##          </div>
##        </div>
##      </div>
    </div>
  </div>
  
</%def>