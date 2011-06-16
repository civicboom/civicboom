<%inherit file="../common/widget_border.mako"/>

% if d['list']['count'] == 0:
    ${_('No content')}
% else:
    ${content_list(d['list']['items'])}
% endif


<%def name="content_list(contents)">
<div id="widget_carousel_fallback_container" class="content_list">
    <ul id="widget_carousel" class="jcarousel-skin-tango">
    % for content in contents:
        ${content_item(content)}
    % endfor
    </ul>
</div>
</%def>


<%def name="content_item(content)">
    <li>
        <a href="${h.url('content', id=content['id'])}">
            <img class="thumbnail" src="${content['thumbnail_url']}" />
            <div class="details">
                <p class="title">${content['title']}</p>
                ##% if 'creator' in content and c.widget['owner']['username'] != content['creator']['username']:
                ##<p class="creator">${member_includes.by_member(content['creator'], link=False)}</p>
                ##% endif
                <p class="content">${content['content_short']}</p>
            </div>
            <a href="" class="button">Click to share your story</a>
        </a>
        <div style="clear:both;"></div>
    </li>
</%def>


<%doc>

</%doc>