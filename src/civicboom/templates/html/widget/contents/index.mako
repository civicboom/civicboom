% for content in d['list']['items']:
    <a href="${url('content', id=content['id'])}">${content['id']}</a>
    ${content['title']}    
% endfor