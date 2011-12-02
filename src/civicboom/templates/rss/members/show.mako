<%inherit file="/rss/rss_base.mako"/>

<%def name="title()">\
    % if d['member']['name']==d['member']['username']:
${d['member']['name']}
    % else:
${d['member']['name']} (${d['member']['username']})
    %endif
</%def>

<%def name="description()">${d['member']['description']}</%def>

<%def name="body()">
    ##please use ${h.url('contents', creator=d['member']['username'], format='rss', qualified=True)}
    
    ##% for content in d['content']['items']:
    ##    ${self.rss_content_item(content)}
    ##% endfor
    
    % for list in [cb_list['items'] for cb_list in d.values() if isinstance(cb_list, dict) and cb_list.get('type')=='contents']:
        % for content in list:
            ${self.rss_content_item(content)}
        % endfor
    % endfor
</%def>
