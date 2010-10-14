<%inherit file="/web/common/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<!--#include virtual="/messages/${d['id']}.frag" -->
<!--#include virtual="/messages/new.frag?to=${d['source']|u}&subject=${"Re: "+d['subject']|u}" -->
</%def>
