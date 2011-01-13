<%inherit file="/rss/rss_base.mako"/>

<%def name="title()"      >Messages</%def>
<%def name="description()">Messages</%def>

<%def name="body()">
    % for message in d['list']:
        ${message_item(message)}
    % endfor
</%def>

<%def name="message_item(message)">
    <item> 
        <title>${message.get('subject')}</title> 
        <link>${h.url('message', id=message['id'])}</link>
        <description>${message.get('content')}</description> 
        <pubDate>${h.date_to_rss(message.get('timestamp'))}</pubDate> 
        <guid isPermaLink="false">Civicboom Message #${message['id']}</guid>
        ##<category>${list}</category>
        % if 'source' in message:
        <dc:creator>${message.get('source',dict()).get('name')} (${message.get('source',dict()).get('username')})</dc:creator>
        % endif
    </item>
</%def>