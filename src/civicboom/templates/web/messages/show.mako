<%inherit file="/web/common/frag_container.mako"/>

<%!
    frag_container_css_class  = 'frag_bridge'
%>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <%include file="/frag/messages/show.mako"/>
    ##<%include file="/frag/messages/index.mako"/>

    <%doc>
    <!--#include virtual="/messages/${d['message']['id']}.frag" -->
    <!--#include virtual="/messages/new.frag?to=${d['message']['source']|u}&subject=${"Re: "+d['message']['subject']|u}" -->
    </%doc>
</%def>

##<%def name="body2()">
##    <div id="frag__" class="frag_container frag_bridge">
##        <%include file="/frag/messages/show.mako"/>
##    </div>
##</%def>