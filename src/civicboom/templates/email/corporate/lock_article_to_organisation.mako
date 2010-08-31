<%inherit file="/base_email.mako"/>

<%namespace name="article_content" file="/design09/email/includes/article_content_and_links.mako"/>

##<%def name="subject()">Your article content request</%def>

##<p>${c.logged_in_reporter.ReporterName},</p>
<h1>Your ${c.terminology['article']} request</h1>

You have locked and approved the following ${c.terminology['article']}.

<h2>Requested content</h2>
${article_content.email_article_content(c.article)}


<h2>Use of this content</h2>

<p>This content is now locked and no further edits can be made by the original creator on ${c.host_name}.</p>
<p>The creator has been notified that you have requested this content for potential use - commercial or non-commercial.</p>
<p>You may now use this content for your needs under the following license:</p>

<h3>License</h3>
<p>This content has been created under <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported</a>. This means you are free to copy, distribute and transmit the work. You are also free to adapt the work according to your needs.</p>
<p>The above is permissible under the following conditions:</p>
<p>You must attribute the work in one of the following manner:</p>
<p>Content credit: Three different ways:</p>
<ol>
  <li>Name of creator as "Source: creator's name/indiconews" (on your final content - image, video or text).</li>
  <li>Link to assignee's article on ${c.site_name} (using above link).</li>
  <li>If multiple sources, link to your assignment page (with all responses listed - including ones you have approved).</li>
</ol>
<p>Note: You can still disassociate your organisation from this ${c.terminology['article']} (should you at a later date need to do so, so long as it is prior to using it in any further way for your own needs eg: publish). If you to fully disassociate - ie: you revoke your decision to use the content and also wish to disassociate your brand from that content, it is on the understanding that your organisation or associated will not use any part of the content according to Creative Commons License. You can do this by clicking the "disassociate" button on the actual ${c.terminology['assignment']} response.</p>

${self.footer()}