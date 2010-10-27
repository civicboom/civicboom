<h1>${d['content']['title']}</h1>

##----Type----
<p>Type: ${d['content']['type']}</p>

##----Details----
% if hasattr(d['content'],'views'):
<p>views: ${d['content']['views']}</p>
% endif

##----Content----
<div class="content_text">
    ${h.literal(h.scan_for_embedable_view_and_autolink(d['content']['content']))}
</div>

% for media in d['content']['attachments']:
    % if media['type'] == "image":
        <a href="${media['original_url']}"><img src="${media['media_url']}" alt="${media['caption']}"/></a>
    % endif
% endfor