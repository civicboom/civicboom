<%inherit file="../common/widget_border.mako"/>

<%namespace name="member_includes" file="/html/widget/common/member.mako"/>

% if d['list']['count'] == 0:
    ${_('No content')}
% else:
    ${content_list(d['list']['items'])}
% endif


<%def name="content_list(contents)">
    ##<div class="widget_content_assignment_list">
    <ul class="content_list">
    % for content in contents:
        ${content_item(content)}
    % endfor
    </ul>
    ##</div>
</%def>

<%def name="content_item(content)">
    ##<a href="${url('content', id=content['id'])}">${content['id']}</a>
    ##${content['title']}
    <li style="border-bottom: 1px solid #${c.widget['color_border']};">
            <a href="${h.url('content', id=content['id'])}">
        ##<td>
                <img class="thumbnail" src="${content['thumbnail_url']}" style="border: 1px solid #${c.widget['color_border']};"/>
        ##</td>
        ##<td>
            
                <div class="details">
                    <p class="title">${content['title']}</p>
                    ##<div style="clear: both;"></div>
                    % if 'creator' in content and c.widget['owner']['username'] != content['creator']['username']:
                    <p class="creator">${member_includes.by_member(content['creator'], link=False)}</p>
                    % endif
                    <p class="content">${content['content_short']}</p>
                </div>
            </a>
        ##</td>
        <div style="clear:both;"></div>
    </li>
</%def>