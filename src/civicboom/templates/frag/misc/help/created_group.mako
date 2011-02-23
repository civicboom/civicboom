<%inherit file="help_popup.mako"/>

<%! config_key = 'help_popup_created_group' %>

<%def name="body()">
<div style="width:750px; height:400px;">
    <h1>${_("Congratulations - you've created a Hub. Here are 3 simple things you can do to help amplify its reach:")}</h1>
    <img src="/images/misc/help/created_group.png"/>
</div>
</%def>