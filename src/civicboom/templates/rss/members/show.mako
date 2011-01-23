<%inherit file="/rss/rss_base.mako"/>
<%def name="title()">${d['member']['name']}</%def>

<%def name="body()">
    please use ${url('contents', creator=d['member']['username'], format='rss')}
    ##% for content in d['content']['items']:
    ##    ${self.rss_content_item(content)}
    ##% endfor
</%def>