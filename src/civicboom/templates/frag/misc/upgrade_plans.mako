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
  <div class="payplanwrapper">
    <div class="payplanholder">
      <div class="payplan" id="planbasic">
        <div class="plantitle">
          Basic<br />
          <span class="subtitle">Free</span>
        </div>
        <div class="planpoints">
          <ul>
            <li>Up to 5 requests per month</li>
            <li>Audio requests and responses</li>
##            <li>Another here</li>
          </ul>
          <div class="buttons">
            <div class="buttongreen">Ideal for...</div>
          </div>
        </div>
      </div>
      <div class="payplan active" id="planprem">
        <div class="plantitle">
          Premium<br />
          <span class="subtitle">£50/month - includes Basic</span>
        </div>
        <div class="planpoints">
          <ul>
            <li>Unlimited requests per month</li>
            <li>Closed requests</li>
##            <li>Another here</li>
            <li>Unlimited hubs</li>
          </ul>
          <div class="buttons">
            <div class="buttongreen">Ideal for...</div>
            <div class="buttonpad"></div>
            <a href="mailto:payment@civicboom.com?Subject=Premium Upgrade" class="button">Choose</a>
          </div>
        </div>
      </div>
      <div class="payplan" id="plancorp">
        <div class="plantitle">
          Corporate<br />
          <span class="subtitle ital">Coming soon</span>
        </div>
        <div class="planpoints">
          <ul>
            <li>More details coming soon!</li>
          </ul>
          <div class="buttons">
            <div class="buttongreen">Ideal for...</div>
          </div>
        </div>
      </div>
      <div class="payplan"  id="plancorpplus">
        <div class="plantitle">
          Corporate plus<br />
          <span class="subtitle ital">Coming soon</span>
        </div>
        <div class="planpoints">
          <ul>
            <li>More details coming soon!</li>
          </ul>
          <div class="buttons">
            <div class="buttongreen">Ideal for...</div><br />
          </div>
        </div>
      </div>
    </div>
  </div>
</%def>