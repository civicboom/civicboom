<%inherit file="help_popup.mako"/>

<%! config_key = 'help_popup_created_user' %>

<%def name="body()">
<div style="width:700px; height:400px;">
    <h1>${_("Welcome to Civicboom! Here are 5 simple things you can do to help kick-start your experience:")}</h1>
    <img src="/images/misc/help/created_user.png"/>
</div>
</%def>