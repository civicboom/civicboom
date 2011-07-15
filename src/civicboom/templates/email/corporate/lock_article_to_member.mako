<%inherit file="../base_email.mako"/>

<%def name="subject()">${_("Your _article has been approved")}</%def>

<%def name="body()">
    <%
        formatted_links = h.objs_to_linked_formatted_dict(article=c.content, parent=c.content.parent, member=c.content.parent.creator)
    %>
    
    <h1>${_('Congratulations!')}</h1>
    <p >${_('Your _article %(article)s in response to %(parent)s has been requested for potential use by %(member)s') % formatted_links |n}</p>
    
    <h2>${_('What next?')}</h2>
    <p >${_('The content you created in response to the _assignment is now locked and no further edits can be made.')}</p>
    <p >${_('The assigner will be able to use this content under the')} <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported</a></p>
    
    <h2>${_('How you will be credited:')}</h2>
    <p >${_('If the assignee chooses to use part of or all content, they will attribute your work in one of the following ways:')}</p>
    <ol>
      <li>${_('Name of creator as "Source: creators name/_site_name" (on your final content - image, video or text).')}</li>
      <li>${_('Link to assignees article on _site_name (using above link).')}</li>
      <li>${_('If multiple sources, link to the _assignment page (with all responses listed - including your approved content).')}</li>
    </ol>
    <p >${_('You will also have "approved" tick against your associated published _assignment, meaning you are a credible source of information for others and improving your profile on _site_name.')}</p>
    
    ${self.footer()}
</%def>
