<%inherit file="./widget_border.mako"/>

<%def name="widget_actions()">
    ## URL_FOR will automatically forward the widget variables such as user and theme
    % if c.widget['list']:
        <a class="icon icon_back" href="${h.url_from_widget('member', id=c.owner['username'], action=c.widget['list'])}"><span>${_("Back")}</span></a>
    % else:
        <a class="icon icon_back" href="${h.url_from_widget('member', id=c.owner['username']                         )}"><span>${_("Back")}</span></a>
    % endif
</%def>

## AllanC - note: as padding gets ADDED to a components size this buggers up the layout when we want the widget_component to take up 100% size, the padding is added so it's 105% (or so)
<div class="widget_content">
    <div class="widget_content_padding">
        ${next.body()}
    </div>
</div>
