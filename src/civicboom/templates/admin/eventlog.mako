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
.log50 {color: #F00;} /* critical, bright red */

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
	vertical-align: middle;
}
#blackout {
	background: #8888;
	position: absolute;
	top: 0px;
	left: 0px;
	right: 0px;
	bottom: 0px;
}
#extra {
	border: 1px solid black;
	border-radius: 8px;
	background: white;
	padding: 4px;
	position: fixed;
	top: 25%;
	left: 25%;
	right: 25%;
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
	<script>
	function show_extra(id) {
		ex = document.getElementById("extra");
		source = document.getElementById(id);
		ex.innerHTML = source.innerHTML;
		ex.style.display = block;
	}
	</script>
	<div id="blackout">
		<div id="extra">
			extra stuff goes here
		</div>
	</div>
	<table class="event_log">
		<tr>
			<th>${_("Date / Time")}</th>
			<th>${_("Module")}</th>
			<th>${_("URL")}</th>
			<th>${_("Username")}</th>
			<th>${_("Message")}</th>
		</tr>
	% for i, event in enumerate(events):
		<tr class='${i % 2 and 'odd' or 'even'} log${event.priority}'>
			<td style="white-space: nowrap;">${str(event.date_sent)[0:19]}</td>
			<td style="white-space: nowrap;">
				<a href="javascript: show_extra('extra_${event.id}_m');">${h.shorten_module(event.module)}</a>
				<div id="extra_${event.id}_m" style="display: none;">
					<a href="?module=${event.module}">Filter for similar rows</a>
					<br><a href="https://dev.civicboom.com/">View source code</a>
				</div>
			</td>
			<td><a href="${event.url}">${h.shorten_url(event.url)}</a></td>
			<td>${h.username_plus_ip(event.username, event.address)|n}</td>
			<td>${h.link_to_objects(event.message)|n}</td>
		</tr>
	% endfor
	</table>
</%def>
