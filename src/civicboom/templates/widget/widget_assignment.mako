<%inherit file="./widget_content.mako"/>

<%def name="body()">
  % if c.assignment:
    ${widget_assignment(c.assignment)}
  % else:
    Error: Unable to find content
  % endif
</%def>

<%def name="widget_assignment(assignment)">
  
    <a href="${h.url(controller='content',action='view',id=assignment.id)}" target="_blank">
        <p class="content_title">${assignment.title}</p>
        <img src=${assignment.thumbnail_url} class="assignment_thumbnail"/>
        <p class="assignment_content">${h.truncate(assignment.content, length=180, indicator='...', whole_word=True)} <strong>more</strong></p>
    </a>
    
    <table class="assignment_actions">
        <tr>
            <td class="">
                ##class="button button_large button_style_1"
                <a class="action button_style_1" href="${h.url_from_widget(controller='assignment',action='accept',id=assignment.id)}">
                    ${_("Accept _assignment")}
                </a>
            </td>
            <td class="">
                ##class="button button_large button_style_1"
                <a class="action button_style_1" href="${h.url(controller='content', action='edit', parent_id=assignment.id)}" target="_blank">
                    ${_("Publish response")}
                </a>
            </td>
        </tr>
    </table>
    
    <div class="assignment_details">
        <div style="display: inline-block;"><strong>${_("Due in")}:      </strong>fix</div>
        <div style="display: inline-block;"><strong>${_("Accepted by")}: </strong>fix</div>
        <p><strong>${_("Responses:")}   </strong>fix</p>
        
        ##${h.time_ago_first_only(assignment.expiryDate)}
        ##${h.format_multiple_prefix(assignment.num_accepted_by_reporters + len(assignment.newsarticles),single=c.terminology['reporter'])}
        ##${h.format_multiple_prefix(len(assignment.newsarticles),nothing="Be the first to respond to this!")}
    </div>

    % if len(assignment.responses) > 0:
    <table class="assignment_responses">
        <tr><th>${_("Approved")}</th><th>${_("_article title")}</th><th colspan="2">${_("_reporter")}</th></tr>
        % for response in assignment.responses:
            <tr>
                <td>
                % if response.response_type = "approved":
                    <img src="/images/star2.gif" alt="${_("_article approved")}"/>
                % endif
                </td>
                <td>${response.title}</td> <!--article_includes.article_link(article)-->
                <td>fix</td> <!-- reporter_includes.reporter_thumbnail_no_text(article.reporter) -->
                <td>fix</td> <!-- reporter_includes.reporter_link(article.reporter, max_chars=8) -->
            </tr>
        % endfor
    </table>
    % endif

</%def>