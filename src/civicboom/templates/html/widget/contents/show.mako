<%inherit file="../common/widget_content.mako"/>

<%namespace name="member_includes" file="/html/widget/common/member.mako"/>


##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%
    content = d['content']
    id      = content['id']
%>


<a class="content_preview" href="${h.url('content',id=id, subdomain='')}" target="_blank">
  <h1>${content['title']}</h1>
  <img src=${content['thumbnail_url']}  style="max-width:40%; float: left;"/>
  <p>${h.truncate(h.strip_html_tags(content['content']), length=180, indicator='...', whole_word=True)}<strong>more</strong></p>
</a>

<div style="clear: both;"></div>

## If the widget is not owned by anybody then show the creator
% if not c.widget['owner']['username'] and c.widget['owner']['username'] != content['creator']['username']:
<p style="float: right; text-align: right;">
    By ${member_includes.by_member(content['creator'])}
</p>
% endif

<div style="clear: both; margin-bottom: 1em;"></div>



% if content['type'] == 'assignment':
    <table><tr>
        <td class="action">
            <div class="padding" style="background-color: #${c.widget['color_header']}; margin-right: 1em;">
            <a href="${h.url('content_action', id=id, action='accept', subdomain='')}" target="_blank">${_('Accept _assignment')}</a>
            </div>
        </td>
        <td class="action">
            <div class="padding" style="background-color: #${c.widget['color_header']};">
            <a href="${h.url('new_content', parent_id=id, subdomain='')}" target="_blank">${_("Respond now!")}</a>
            </div>
        </td>
    </tr></table>
    
    <div>
        % if content.get('due_date'):
        <div style="display: inline-block;"><strong>${_("Due in")}:      </strong>${h.time_ago(content.get('due_date'))}</div>
        % endif
        <div style="display: inline-block;"><strong>${_("Accepted by")}: </strong>${content.get('num_accepted')} ${_('_members')}</div>
        
        ##${h.time_ago_first_only(assignment.expiryDate)}
        ##${h.format_multiple_prefix(assignment.num_accepted_by_members + len(assignment.newsarticles),single=_("_member"))}
        ##${h.format_multiple_prefix(len(assignment.newsarticles),nothing="Be the first to respond to this!")}
    </div>
% endif

% if 'num_responses' in content:
    <h2>${_("Responses:")} (${content['num_responses']})</h2>
% endif
% if 'responses' in d and d['responses']['count'] > 0:
<table class="responses">
    ##<tr><th>${_("Approved")}</th><th>${_("_article title")}</th><th colspan="2">${_("_user")}</th></tr>
    % for response in d['responses']['items']:
        <%
            response_class = ""
            if response['approval']:
                response_class = response['approval']
        %>
        <tr class="${response_class}">
            <td class="${response_class}"></td>
            <td><img src="${response['thumbnail_url']}" alt="${response['title']}" style="border: 1px solid #${c.widget['color_border']}; margin-right: 0.5em;"/></td>
            <td><a href="${h.url('content', id=response['id']                 , subdomain='')}" target="_blank">${response['title']}</a></td>
            <td><a href="${h.url('member' , id=response['creator']['username'], subdomain='')}" target="_blank"><img src="${response['creator']['avatar_url']}" alt="${response['creator']['name'] or response['creator']['username']}" style="border: 1px solid #${c.widget['color_border']};"/></a></td>
        </tr>
    % endfor
</table>
% else:
  ${_('Get involved! Respond now!')}
% endif