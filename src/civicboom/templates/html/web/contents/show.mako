<%inherit file="/html/web/common/frag_container.mako"/>

##<%namespace name="frag_content" file="/frag/contents/show.mako"/>

##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------

<%def name="rss()">${self.rss_header_link()}</%def>
<%def name="rss_url()">${url(controller='search', action='content', response_to=c.result['data']['content']['id'], format='xml')}</%def>
<%def name="rss_title()">Responses to ${c.result['data']['content']['title']}</%def>
## FIXME: extra RSS for "more by this author"?


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${d['content']['title']}</%def>
<%def name="description()">${h.strip_html_tags(d['content']['content'])[:300]}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = content %>
</%def>

<%def name="content()">
    <%include file="/frag/contents/show.mako"/>
</%def>
