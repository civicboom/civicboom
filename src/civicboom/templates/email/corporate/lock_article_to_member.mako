<%inherit file="/base_email.mako"/>

<%namespace name="reporter_includes"   file="/design09/includes/reporter_thumbnail.mako"/>
<%namespace name="article_includes"    file="/design09/includes/article.mako"/>
<%namespace name="assignment_includes" file="/design09/includes/assignments.mako"/>

<%def name="subject()">Your ${c.terminology['article']} has been approved</%def>

<h1>Congratulations!</h1>
<p>Your ${c.terminology['article']} ${article_includes.article_link(c.article)} in response to ${assignment_includes.assignment_link(c.article.assignment)} has been requested for potential use by ${reporter_includes.reporter_link(c.article.assignment.creatorReporter)}</p>
<h2>What next?</h2>
<p>The content you created in response to the ${c.terminology['assignment']} is now locked and no further edits can be done on ${c.host_name}.</p>
<p>The assigner will be able to use this content under the <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported</a></p>
<h2>How you will be credited:</h2>
<p>If the assignee chooses to use part of or all content, they will attribute your work in one of the following ways:</p>
<ol>
  <li>Name of creator as "Source: creator's name/${c.site_name}" (on your final content - image, video or text).</li>
  <li>Link to assignee's article on ${c.site_name} (using above link).</li>
  <li>If multiple sources, link to the ${c.terminology['assignment']} page (with all responses listed - including your approved content).</li>
</ol>
<p>You will also have "approved" tick against your associated published ${c.terminology['assignment']}, meaning you are a credible source of information for others and improving your profile on ${c.site_name}.</p>

${self.footer()}