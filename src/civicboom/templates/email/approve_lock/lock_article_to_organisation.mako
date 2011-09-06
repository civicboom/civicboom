<%inherit file="../base_email.mako"/>

<%def name="subject()">${_('Your _article request')}</%def>

<%def name="body()">
  <%
      formatted_links = h.objs_to_linked_formatted_dict(article=c.content, parent=c.content.parent, member=c.content.creator)
  %>

  <h1>${_('Your _article request')}</h1>
      <p>${_('You have locked and approved the following _article.')}</p>
  
      <h2>${_('Requested _article')}</h2>
          
          <h3>${'%(article)s' % formatted_links |n}</h3>
              <p>${_('Download media:')}</p>
              <ul>
                %for original_url in [media.original_url for media in c.content.attachments]:
                <li><a href="${original_url}">${original_url}</a></li>
                %endfor
              </ul>
              <p>${_('_member: %(member)s') % formatted_links |n}</p>
              
              ${c.content.content}
      
      
      <h2>${_('Use of this content')}</h2>
          <p>${_('This content is now locked and no further edits can be made by the original creator on _site_name.')}</p>
          <p>${_('The creator has been notified that you have requested this content for potential use - commercial or non-commercial.')}</p>
          <p>${_('You may now use this content for your needs under the following license:')}</p>
            
          <h3>${_('License')}</h3>
              <p>${_('This content has been created under')} <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported</a>. ${_('This means you are free to copy, distribute and transmit the work. You are also free to adapt the work according to your needs.')}</p>
              <p>${_('The above is permissible under the following conditions:')}</p>
              <p>${_('You must attribute the work in one of the following manner:')}</p>
              <p>${_('Content credit: Three different ways:')}</p>
              <ol>
                <li>${_('Name of creator as "Source: creators name/_site_name" (on your final content - image, video or text).')}</li>
                <li>${_('Link to assignees article on _site_name (using above link).')}</li>
                <li>${_('If multiple sources, link to your assignment page (with all responses listed - including ones you have approved).')}</li>
              </ol>
              ##<p>${_('Note: You can still disassociate your organisation from this _article (should you at a later date need to do so, so long as it is prior to using it in any further way for your own needs eg: publish). If you to fully disassociate - ie: you revoke your decision to use the content and also wish to disassociate your brand from that content, it is on the understanding that your organisation or associated will not use any part of the content according to Creative Commons License. You can do this by clicking the "disassociate" button on the actual _assignment response.')}</p>)
              
  ${self.footer()}
</%def>
