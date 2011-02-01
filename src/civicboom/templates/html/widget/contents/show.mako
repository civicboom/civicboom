<%inherit file="../common/widget_content.mako"/>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%
    content = d['content']
    id      = content['id']
%>

<a href="${h.url('content',id=id, subdomain='')}" target="_blank">
  <h1>${content['title']}</h1>
  <img src=${content['thumbnail_url']}  style="max-width:100%;"/>
  <p>${h.truncate(h.strip_html_tags(content['content']), length=180, indicator='...', whole_word=True)}<strong>more</strong></p>
</a>


% if content['type'] == 'assignment':
    <table><tr>
        <td>
            <a href="${h.url('content_action', id=id, action='accept', subdomain='')}" target="_blank">${_('Accept _assignemnt')}</a>
        </td>'
        <td>
            <a href="${h.url('new_content', parent_id=id, subdomain='')}" target="_blank">${_("Respond now!")}</a>
        </td>
    </tr></table>
    
    <div>
        <div style="display: inline-block;"><strong>${_("Due in")}:      </strong>fix</div>
        <div style="display: inline-block;"><strong>${_("Accepted by")}: </strong>${content['num_accepted']} ${_('_members')}</div>
        <p                                 ><strong>${_("Responses:")}   </strong>${content['num_responses']}</p>        
        ##${h.time_ago_first_only(assignment.expiryDate)}
        ##${h.format_multiple_prefix(assignment.num_accepted_by_members + len(assignment.newsarticles),single=_("_member"))}
        ##${h.format_multiple_prefix(len(assignment.newsarticles),nothing="Be the first to respond to this!")}
    </div>
% endif

% if 'responses' in d and d['responses']['count'] > 0:
<table>
    <tr><th>${_("Approved")}</th><th>${_("_article title")}</th><th colspan="2">${_("_user")}</th></tr>
    % for response in d['responses']['items']:
        <%
            response_class = ""
            if response['approval']:
                response_class = response['approval']
        %>
        <tr class="${response_class}">
            <td class="${response_class}"></td>
            <td>${response['title']}</td> <!--article_includes.article_link(article)-->
            <td>fix</td> <!-- member_includes.member_thumbnail_no_text(article.member) -->
            <td>${response['creator']['name']}</td> <!-- member_includes.member_link(article.member, max_chars=8) -->
        </tr>
    % endfor
</table>
% endif



<%doc>
##------------------------------------------------------------------------------
## Content
##------------------------------------------------------------------------------


<a href="${h.url('content',id=id, subdomain='')}" target="_blank">
    <p class="content_title">${content['title']}</p>
    ##${content_list.content_thumbnail_icons(assignment)}
    <img src=${content['thumbnail_url']} class="assignment_thumbnail"/>
    ## AllanC TODO: optimise the need for the template to do this truncating processing
    ##              propose using content_short?
    <p class="assignment_content">${h.truncate(h.strip_html_tags(content['content']), length=180, indicator='...', whole_word=True)} <strong>more</strong></p>
</a>

##------------------------------------------------------------------------------
## Assignment Actions
##------------------------------------------------------------------------------

% if content['type'] == 'assignment':
    <table class="assignment_actions">
        <tr>
            <td class="">
                ${h.secure_link(
                    h.args_to_tuple('content_action', action='accept', format='redirect', id=id),
                    _("Accept _assignment") ,
                    title        = _("Accept _assignment") ,
                    css_class    = "action button_style_1" ,
                )}
            </td>
            <td class="">
                <a class="action button_style_1" href="${h.url('new_content', parent_id=id)}" target="_blank">
                    ${_("Respond now!")}
                </a>
            </td>
        </tr>
    </table>
    
    <div class="assignment_details">
        <div style="display: inline-block;"><strong>${_("Due in")}:      </strong>fix</div>
        <div style="display: inline-block;"><strong>${_("Accepted by")}: </strong>${content['num_accepted']} ${_('_members')}</div>
        <p                                 ><strong>${_("Responses:")}   </strong>${content['num_responses']}</p>
        
        ##${h.time_ago_first_only(assignment.expiryDate)}
        ##${h.format_multiple_prefix(assignment.num_accepted_by_members + len(assignment.newsarticles),single=c.terminology['member'])}
        ##${h.format_multiple_prefix(len(assignment.newsarticles),nothing="Be the first to respond to this!")}
    </div>
% endif


##------------------------------------------------------------------------------
## Responses
##------------------------------------------------------------------------------

% if 'responses' in d and d['responses']['count'] > 0:
<table class="assignment_responses">
    <tr><th>${_("Approved")}</th><th>${_("_article title")}</th><th colspan="2">${_("_user")}</th></tr>
    % for response in d['responses']['items']:
        <%
            response_class = ""
            if response['approval']:
                response_class = response['approval']
        %>
        <tr class="${response_class}">
            <td class="${response_class}"></td>
            <td>${response['title']}</td> <!--article_includes.article_link(article)-->
            <td>fix</td> <!-- member_includes.member_thumbnail_no_text(article.member) -->
            <td>${response['creator']['name']}</td> <!-- member_includes.member_link(article.member, max_chars=8) -->
        </tr>
    % endfor
</table>
% endif

</%doc>
