<%inherit file="/admin/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Event Log")}</%def>

##------------------------------------------------------------------------------
## Navigation override - remove it
##------------------------------------------------------------------------------
##<%def name="navigation()"></%def>

##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
<%def name="styleOverides()">
.log0  {color: #0F0;} /* undefined, green     */
.log10 {color: #999;} /* debug, grey          */
.log20 {color: #000;} /* info, black          */
.log30 {color: #800;} /* warning, dark red    */
.log40 {color: #C00;} /* error, mid red       */
.log50 {background: #F00;} /* critical, bright red background */

.event_log    {
	border: 1px solid black;
	margin: auto;
	margin-top: 8px;
}
.event_log TR {
	border-top: 1px solid black;
}
.event_log TD,
.event_log TH {
	padding: 2px 8px 2px 8px;
}
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <h1 id="header" class="ui-widget-header ui-corner-all">
		<div class="breadcrumb"> 
			/<a href="/admin">admin</a>/<a href="/admin/event_log">event log</a>
		</div> 
		Event Log
	</h1>
	<table class="event_log">
		<tr>
			<th>${_("Date / Time")}</th>
			<th>${_("Module")}</th>
			<th>${_("URL")}</th>
			<th>${_("Username")}</th>
			<th>${_("Message")}</th>
		</tr>
	% for event in events:
		<tr class='log${event.priority}'>
			<td>${str(event.date_sent)[0:19]}</td>
			<td><a href="?module=${event.module}" title="${event.module}">${h.shorten_module(event.module)}</a></td>
			<td><a href="${event.url}">${h.shorten_url(event.url)}</a></td>
			<td>${h.username_plus_ip(event.username, event.address)|n}</td>
			<td>${h.link_to_objects(event.message)|n}</td>
		</tr>
	% endfor
	</table>
</%def>
