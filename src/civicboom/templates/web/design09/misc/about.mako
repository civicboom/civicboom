<%inherit file="base_misc.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("About")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<div class="misc_about misc_page_border">
  
  <div class="link_float"><a href="${h.url(controller='account', action='signin')}">${_("Start Now!")}</a></div>
  
  <h1>${_("About _site_name &amp; FAQ")}</h1>
  
  
  <h2>What is it?</h2>
  <ul class="bigger">
    <li>${_("_site_name is a tool that makes building a story easier.")}</li>
    <li>${_("It connects people with news and insight with people who need it.")}</li>
  </ul>
  
  
  <h2>How can it work for you?</h2>
  <div class="about_flow">
    <p class="step1"><span class="list_bullet_number">1</span><br/>${_("Add _site_name widget to your website. Request news &amp; insight from your community or wider public")}</p>
    <ul class="stepA">
      <li>${_("Get relevant content from your audience")}</li>
      <li>${_("Connect more deeply with your audience")}</li>
    </ul>  
    <p class="step2"><span class="list_bullet_number">2</span><br/>${_("Respond directly to _assignments by uploading relevant news and insight")}</p>
    <ul class="stepB">
      <li>${_("Participate directly in issues you care about")}</li>
      <li>${_("Get recognised as a credible news source")}</li>
    </ul>
    <a class="view_widget_link" href="${h.url(controller='misc', action='widget_details')}"><img src="/images/misc/view_widget_detail_button.png" alt="view widget in detail"/></a>
    <img class="about_flow_background" src="/images/misc/about_arrow_flow_background.png" alt="about flow background arrows"/>
  </div>
  
  
  
  
  <div class="yui-g">
    
    <div class="yui-u first">
      <div class="section_border">
        <h2>${_("_site_name for the individual")}</h2>
        <ul>
          <li>Provide insight on issues, ideas, news and opinion</li>
          <li>Become a trusted contributor and get recognition</li>
          <li>Participate in the news agenda at the local level.</li>
        </ul>
        <h3>How?</h3>
        <p>${_("_site_name works in 3 ways")}</p>
        <ol>
          <li>${_("You can search _site_name for call-to-action assignments from organisations and people that want your news, opinion and insight.")}</li>
          <li>${_("You can respond to specific _assignments for your news and insight wherever you see the _site_name widget on other websites that want to news and insight from you.")}</li>
          <li>${_("You can upload your news and insight directly, share with your Followers, and if appropriate even syndicate exclusive content that you have (photo's or video) and earn money.")}</li>
        </ol>
      </div>
    </div>
  
    <div class="yui-u">
      <div class="section_border">
        <h2>${_("_site_name for organisations")}</h2>
        
        <ul>
          <li>Directly request and capture news, insights and opinion from your communities</li>
          <li>Plan and create news features or research</li>
          <li>Improve your connection with and understanding of your community</li>
        </ul>
        
        <h3>How?</h3>
        <p>${_("_site_name works by enabling you to:")}</p>
        <ol>
          <li>${_("Set a call-to-action _assignment for news or insight directly from your community via the widget powered by _site_name as a public or \"closed\" _assignment.")}</li>
          <li>${_("\"Approve\" relevant content for use in your publishing, news and research - plus if you are a media organisation, sell images or video on* (with share of revenue going back to the original creator).")}</li>
          <li>${_("Establish a better connection and understanding of issues that matter to the community you serve.")}</li>
        </ol>
      </div>
    </div>
    
  </div>
  
  <div class="yui-g">
    
    <div class="yui-u first">
  
      <h2>What is "approved" content?</h2>
      
      <p>When responding to a call-to-action request, the content generated can be "approved" by the organisation or individual
      requesting it. If approved, the content will be used by that organisation or individual. For example, it could be published or
      used as part of research. Once this happens, the approved content is locked so no further editing can take place by the
      creator. The creator is automatically alerted of this and is given a badge of approval against that content (helping build their
      profile) and is credited by the organisation either by name where the content has been used, or by a link back to the request
      "package" on the organisation's ${_("_site_name")} profile. The organisation is also able to sell on images or content, with part of the
      revenue shared with the contributor (automated through PayPal*).</p>
      
      
      <h2>${_("What is a \"closed\" _assignment**?")}</h2>
      
      <p>An organisation or individual setting a call-to-action request has the choice to make a "closed" request. It means that if - as
      the requester - they want to specifically use approved content generated for a feature or research, they can keep that content
      visible only to themselves and the contributor until published. It might be a news report, or a case study - it is at the discretion
      of whoever has requested the content. An approved contributor of a "closed" request is given a specific badge against that
      content in their profile, improving rating and reliability. It also means other organisations can see they've been a reliable
      source for a request.</p>
      
      <p>If the content generated against a "closed" request is not used by the organisation, that content then becomes publicly visible
      on the creators ${_("_site_name")} profile but is also listed in the "responses" against the organisation's request, further building the
      profile of the creator.</p>
      
      <h2>What if I change my mind once I've agreed to contribute?</h2>
      
      <p>Anyone who "accepts" to respond to a request can retract their commitment, giving you flexibility. Likewise, and organisation
      or individual setting a call-to-action request can edit a request and deadline, or delete the request completely. Furthermore,
      content created against a request can also be disassociated from an individual responding by the organisation or individual
      requesting it. This necessary just in case the content is not appropriate for the organisation's audience - but so long as the
      content doesn't break our "4 Simple Rules", it can stay on ${_("_site_name")} and can be used in any way by the creator.</p>
  
    </div>
    
    <div class="yui-u">
      
      <h2>Why do I need a profile?</h2>
      <p>In order to build a portfolio, download the widget, set requests or ensure you are credited (and even financially rewarded) for
      the content you have uploaded via ${_("_site_name")}, you need a profile. It also means that other users of ${_("_site_name")} can find and
      Follow you - heightening your presence and gaining better recognition as a contributor.
      
      <h2>How can I protect my content?</h2>
      <p>You publish your news and insight, and ask for requests through the "Attribution" Creative Commons License. This means
      you let others copy, distribute, display, and perform your copyrighted work - and derivative works based upon it - but only if
      they give you credit. For more info click <a href="http://creativecommons.org/licenses/by/3.0/">HERE</a>.</p>
      <p>By using ${_("_site_name")}, media organisations may want to sell on your original content (images and video) with a share of the
      revenue going back to you. This licence allows that, but you do have the ability to waive this if you so wish by stating it in
      your content.</p>
      
      <h2>What about copyright?</h2>
      <p>${_("_site_name")} takes copyright very seriously. As a user, you are responsible for ensuring you have the adequate copyright
      to upload any image or video.</p>
      <p>If you do upload and you do not have the rights to the image, video or content then it is likely you will be liable for full
      payment to the copyright holder. See terms and conditions for full details.
      You can use Creative Commons on Flikr to help you find an image to support your upload (the link is on the upload page)
      - but make sure you credit the creator.</p>
  
      <p><br/>* &amp; ** rolling out May 2010.</p>
  
    </div>
  
  
  ##<div class="clearboth_hack"></div>
  </div>

</div>
