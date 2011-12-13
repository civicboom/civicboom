<%inherit file="base.mako"/>
<%def name="title()">${_("About _site_name & FAQ")}</%def>

<div id="about_civicboom">
    
    <h1>${_("_site_name enables content-hungry organisations to ask for and get back video, images and audio from their audience simply and directly via mobile or PC.")}</h1>
    
    <h2>${_("The How")}</h2>
    <p>${_("Our platform allows anyone to post Requests for specific items of content, to publicise those Requests and to manage content! We provide an altogether deeper level of engagement within communities.")}</p>
    <ol>
        <li>${_("An organisation can put out a request for video, images or audio via a simple widget on their site, plus our free mobile application and social networks.")}</li>
        <li>${_("The audience can then respond to the request directly via their mobile or web.")}</li>
        <li>${_("When the organisation gets the content back they can validate, approve and use.")}</li>
    </ol>
    <img src="/images/misc/about/organisations/flow.png" class="flow" />
    
    <h2>${_("The Smart Part")}</h2>
    <p>${_("Civicboom provides a suite of tools to facilitate and manage specific requests for rich media content. In effect, it is a customisable channel between audience-facing organisations, and the members of the audience itself.")}</p>
    <p>${_("This channel delivers content through the use of:")}</p>
    <ul>
        <li>${_("Plugins - designed to encourage engagement with requests and responses from website visitors.")}</li>
        <li>${_("Native Mobile Apps  - designed to allow responses to requests with geolocated content.")}</li>
        <li>${_("Our Mobile Website - for those without access to our Apps.")}</li>
    </ul>
    <p>${_("Content can also be suggested or pushed-to specific audience-facing organisations unprompted.")}</p>
    
    <h2>${_("An Open Documented Platform")}</h2>
    <p>
        ${_("We are an open platform, therefore the entire data-set of requests and responses are available through a public documented ")}<a href="http://www.programmableweb.com/api/civicboom">${_("API [Application Programing Interface]")}</a>${_(". Developers are able to integrate our technology into existing systems, to mashup with existing APIs.")}
    </p>
    <p>${_("The data is open for the public to see, use and interact with.")}</p>
    
    <h2>${_("Packages")}</h2>
    <p>${_("For organisations, we offer two packages to be tailored according to your requirements:")}</p>
    <ol>
        <li><b>${_("Browser-Based + Limited Services: ")}</b>${_("Access to the site as it is with the additional use of certain content management tools, extra privileges and features")}</li>
        <li><b>${_("API + Extensive Services: ")}</b>${_("Unlimited access to our API and the provision of a customised solution to your internal or external engagement inefficiencies.")}</li>
    </ol>
    
    <h2>${_('Want to learn more?')}</h2>
    <p>${_("Either sign up or contact us:")}</p>
    ${parent.sign_up()}
    ${parent.contact_us()}
    
    <h2>${_('Find us at:')}</h2>
    <p><a href="http://www.programmableweb.com/api/civicboom">${_('Programmable Web')}</a><br />
    <a href="http://civic.mit.edu/projects/community/civicboom">${_('MIT Centre For Civic Media')}</a></p>

</div>