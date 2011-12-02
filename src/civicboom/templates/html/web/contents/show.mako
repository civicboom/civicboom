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
<%def name="description()">${d['content']['content_short']}</%def>
<%def name="canonical_url()">${h.url(controller='contents', action='show', id=d['content']['id'], title=h.make_username(d['content']['title']), sub_domain='www', protocol='https', qualified=True)}</%def>
<%def name="breadcrumbs()">
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url('contents')}" itemprop="url"><span itemprop="title">Content</span></a>
</span>
&rarr;
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
<%
_ctype = "_%ss" % d['content']['type'].capitalize()
%>
	<a href="${h.url('contents', type=d['content']['type'])}" itemprop="url"><span itemprop="title">${_(_ctype)}</span></a>
</span>
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = content %>
</%def>

<%def name="content()">
    <%include file="/frag/contents/show.mako"/>
</%def>
