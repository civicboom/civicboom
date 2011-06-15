<%inherit file="widget_border.mako"/>

<%!
    from civicboom.lib.web import current_referer
%>

<%def name="widget_actions()">
    ## URL_FOR will automatically forward the widget variables such as user and theme
    <%
        back_url = ''
        if c.widget['base_list'] and c.widget['owner']['username']:
            back_url = h.url('member_action', id=c.widget['owner']['username'], action=c.widget['base_list'])
        elif c.widget['owner']['username']:
            back_url = h.url('member', id=c.widget['owner']['username'])
        else:
            back_url = current_referer()
    %>
    ##<a class="icon16 i_back" href="${back_url}"><span>${_("Back")}</span></a>
    <a href="${back_url}">&#171; ${_("Back")}</a>
</%def>

## AllanC - note: as padding gets ADDED to a components size this buggers up the layout when we want the widget_component to take up 100% size, the padding is added so it's 105% (or so)
##<div class="widget_content">
##    <div class="widget_content_padding">
${next.body()}
##    </div>
##</div>
