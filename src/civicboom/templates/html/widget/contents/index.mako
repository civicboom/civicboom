<%inherit file="../common/widget_border.mako"/>

<%namespace name="member_includes" file="/html/widget/common/member.mako"/>

% if d['list']['count'] == 0:
    ${_('No content')}
% else:
    ${content_list(d['list']['items'])}
% endif


<%def name="content_list(contents)">
    ##<div class="widget_content_assignment_list">
    <table class="content_list">
    % for content in contents:
        ${content_item(content)}
    % endfor
    </table>
    ##</div>
</%def>

<%def name="content_item(content)">
    ##<a href="${url('content', id=content['id'])}">${content['id']}</a>
    ##${content['title']}
    <tr style="border-bottom: 1px solid #${c.widget['color_border']};">
        <td>
            <img class="thumbnail" src="${content['thumbnail_url']}" style="border: 1px solid #${c.widget['color_border']};"/>
        </td>
        <td>
            <a href="${h.url('content', id=content['id'])}">
                
                <p class="title">${content['title']}</p>
                ##<div style="clear: both;"></div>
                % if c.widget['owner']['username'] != content['creator']['username']:
                <p class="creator">${member_includes.by_member(content['creator'], link=False)}</p>
                % endif
            </a>
        </td>
    </tr>
</%def>