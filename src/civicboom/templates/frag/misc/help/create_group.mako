<%inherit file="help_frag.mako"/>
<%def name="body()">

<h1>${_("Create a _Group")}</h>
<p>${_("_Groups are a very powerful tool for both organisations and individuals. They allow you to create specific \"personas\" associated with any issue, topic, theme, brand, publication, project etc. For example, you might create a group just focused on news in your town, or conservation, or a campaign.")}</p>

<p>${_("The user that creates a _group is automatically assigned as the Administrator. This means they have final \"say\" on what is published or used as a result of the group requests.")}</p>

<p>${_("Members of a _group have various privileges - and as such can have various levels of responsibility. As administrator, you decide what level to give members. But remember: a member of a _group is different to a Follower as they represent that group persona and as such have more \"rights\".")}</p>

<p>${_("By creating a _group, you also create a _widget associated with it. The _widget holds a list of all your requests and can be embedded on a specific page or website empowering your community to respond directly to requests set by that _group.")}</p>

<h2>${_("Open, Public and Private join modes")}</h>
<p>${_("There are various \"join\" levels that you can set when creating groups:")}</p>
<ul>${_("Open: this means anyone can join the _group")}</ul>
<ul>${_("Public: this means users can request to become a member of a _group, and can be invited to join by the Admin.")}</ul>
<ul>${_("Private: this means only those invited to join a _group by the Admin can do so.")}</ul> 

</%def>
