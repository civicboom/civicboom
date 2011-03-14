<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    rss_url   = False
    help_frag = 'link_accounts'
%>

<%namespace name="link_janrain" file="/frag/account/link_janrain.mako"/>

<%def name="title()">${link_janrain.title()}</%def>

<%def name="body()">
    ${link_janrain.body()}
</%def>
