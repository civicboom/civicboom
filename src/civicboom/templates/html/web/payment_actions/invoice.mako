<%inherit file="/html/web/common/frag_container.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Invoice')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%        
        self.attr.frags = [payment, invoice]
    %>
</%def>

<%def name="payment()">
    <!--#include file="${h.url(controller='payments', action='show', id=d['payment_account']['id'], format='frag')}"-->
</%def>

<%def name="invoice()">
    <%include file="/frag/payment_actions/invoice.mako"/>
</%def>
