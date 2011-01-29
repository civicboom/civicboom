<%inherit file="../common/widget_border.mako"/>

% if d['list']['count'] == 0:
    ${_('No content')}
% else:
    ${content_list(d['list']['items'])}
% endif


<%def name="content_list(contents)">
    <div class="widget_content_assignment_list">
        <ul>
        % for content in contents:
            ${content_item(content)}
        % endfor
        </ul>
    </div>
</%def>

<%def name="content_item(content)">
    ##<a href="${url('content', id=content['id'])}">${content['id']}</a>
    ##${content['title']}
    <li>
        <a href="${h.url('content', id=content['id'])}">
            <img src="${content['thumbnail_url']}"/>
            <span>${content['title']}</span>
            <div style="clear: both;"></div>
        </a>
    </li>
</%def>