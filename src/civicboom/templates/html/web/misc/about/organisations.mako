<%inherit file="base.mako"/>
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%def name="title()">${_("Using _site_name for your organisation")}</%def>

<%def name="contact_us()">
    <%
        popup.link(
            h.args_to_tuple(controller='misc', action='contact_us'),
            title = _('Contact us'),
            text  = h.literal("<span class='learn_more button'>%s</span>") % _('Contact us'),
        )
    %>
</%def>

<div id="organisations">

    <h1>${_('Using _site_name for your organisation')}</h1>
    <ol>
        <li>${_("You have a content-hungry organisation: you need need video, audio or images.")}</li>
        <li>${_("You have an audience that has or can provide the content, but you don't have the systems or resources to manage the work-flow process.")}</li>
        <li>${_("You use our technology to manage the process, enabling you to ask for and get back content directly from your audience simply and quickly.")}</li>
    </ol>
    
    <img src="/images/misc/about/organisations/flow.png" class="flow" />
    
    <h1>You can use _site_name in two ways:</h1>
    <ol>
        <li>
            <strong>${_("Our browser-based solution: ")}</strong>
            ${_("simply sign up, create your organisational Hub, pop your exclusive widget in your website and start asking for content.")}
            <p><em>Ideal for: </em><strong>magazines, local news, small publications</strong></p>
        </li>
        <li>
            <strong>${_("Via our Platform/API Services Custom Solution: ")}</strong>
            ${_("Everything on our platform is built on our own API. This means whatever we have can be bolted onto existing communications platforms or systems improving work-flow both internally and externally.")}
            <p><em>Ideal for: </em><strong>large media organisations, global brands</strong></p>
        </li>
    </ol>
    
    <div class="short">
        <h1>${_("Want to learn more?")}</h1>
        <p>
            ${_("We're working with some really innovative companies who understand the power and reach of our technology. If you want to be one of them, just hit the Contact us button.")}
        </p>
    </div>
    ${contact_us()}
    
    <h1>${_("The system in more detail")}</h1>
    <p>${_("Civicboom is a flexible audience engagement platform with a range of features for content management - a Software as a Service solution [SaaS]. This platform is powered by its own API. It is designed make the process of asking for and getting back rich media content between the content-hungry organisations and their audience or established contributors more efficient, and more manageable.")}</p>
    <p>${_("In other words, our system can save time through not only having content sent directly to an organisation, but also down to the right person - editor of the UK business desk for example - in a manageable way.")}</p>
    
    <h1>${_("Instances of how _site_name can be used")}</h1>
    <p>${_("The Civicboom platform can be exploited by organisations in a number of ways, but the primary function is to enable them to request for rich-media content this being videos, images and audio (text can also be added). Individuals with access to that specific content - as wide or narrow audience as the organisation requires - then respond to that request via mobile or computer. The content can then be validated, approved, locked and used by the organisation.")}</p>
    <p>${_("We have created this system to not only to bring the audience into the content creation process, but in turn enable organisations to have a better knowledge of who is responding, what content is coming in, from where (all content is Geolocated) and when: we have a scheduler so deadlines can be set with automatic nudges. We are also able to integrate to iCal, making the work flow even more fluid. ")}</p>
    <p>${_("Together our platform creates an overall deeper level of engagement and knowledge. It also manages all the content in one place [known as Hubs] that can be accessed by Together our platform creates an overall deeper level of engagement and knowledge. It also manages all the content in one place [known as Hubs] that can be accessed by authorised individuals in the organisation requesting content. ")}</p>
    
    <h1>${_("Apps and plugins")}</h1>
    <p>${_("Our platform lends itself exceptionally well to the development of Apps and Plugins. At the moment we have released a free Android Mobile App, with another two for Blackberry and iPhone currently in development. ")}</p>
    <p>${_("These existing free mobile Apps could be used as they are, or adapted according to an organisation's specifications. ")}</p>
    
    <h1>${_("Cloud based")}</h1>
    <p>${_("Because we host in the cloud, there is no additional strain on organisation servers. ")}</p>
    
    <h1>${_("QR codes")}</h1>
    <p>${_("We have also created a way for organisations to use QR codes, generated by our system, in print (posters, magazines, newspapers etc) to generate direct audience engagement and news submission. In other words - the offline world meets the online. ")}</p>
    
    <div class="short">
        <h2>${_("Interested to learn more? ")}</h2>
        <span>
            ${_("Then get in touch: ")}
        </span>
    </div>
    ${contact_us()}

</div>