<%namespace name="components" file="/html/web/common/components.mako" />

##------------------------------------------------------------------------------
## Imports
##------------------------------------------------------------------------------
<%!

%>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <div id="contact_us">
        <h1>${_("Contact _site_name")}</h1>
        <p>${_("Looking to get in touch with _site_name? Fill out the contact form and we'll be back in contact with you as soon as we can!")}</p>
        ##<form name="" action="" method="post">
        ${h.form(h.args_to_tuple(controller='misc', action='contact_us', format='redirect'), method='POST', data=dict(json_complete="[['modal_close']]"))}
            <label for="name">${_("Your name: ")}</label>
            <input name="name" type="text" value="" required="true" placeholder="e.g. John Smith" />
            
            <label for="organisation">${_("Organisation: ")}</label>
            <input name="organisation" type="text" value="" required="true" placeholder="e.g. Civicboom" />
            
            <label for="email">${_("Email: ")}</label>
            <input name="email" type="email" value="" required="true" placeholder="e.g. j.smith@civicboom.com" />
            
            <label for="tel">${_("Telephone (optional): ")}</label>
            <input name="tel" type="text" value="" />
            
            <label for="message">${_("Message: ")}</label>
            <textarea name="message" type="text" rows="8" required="true"></textarea>
            
            <input name="submit" type="submit" value="Send" class="button"/>
        </form>
    </div>
</%def>