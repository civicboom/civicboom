<%inherit file="/html/web/common/frag_container.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Regrade plans')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%        
        self.attr.frags = [regrade_plans]
    %>
</%def>

<%def name="regrade_plans()">
    <%include file="/frag/payment_actions/regrade_plans.mako"/>
</%def>
