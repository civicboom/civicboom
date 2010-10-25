<%inherit file="/web/common/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<!--#include virtual="/messages/${d['message']['id']}.frag" -->
<!--#include virtual="/messages/new.frag?to=${d['message']['source']|u}&subject=${"Re: "+d['message']['subject']|u}" -->
</%def>
