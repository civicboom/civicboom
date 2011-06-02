<%inherit file="/rss/rss_base.mako"/>
<%def name="title()">${d['member']['name']}</%def>

<%def name="body()">
    ##please use ${h.url('contents', creator=d['member']['username'], format='rss', qualified=True)}
    
    ##% for content in d['content']['items']:
    ##    ${self.rss_content_item(content)}
    ##% endfor
    
    % for list in [cb_list['items'] for cb_list in d.values() if isinstance(cb_list, dict) and cb_list.get('type')=='content']:
        % for content in list:
            ${self.rss_content_item(content)}
        % endfor
    % endfor
</%def>
