<%namespace name="frag_lists" file="/frag/common/frag_lists.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
${frag_lists.content_list(d['list'], _("Responses"), max=None, creator=True)}
</%def>