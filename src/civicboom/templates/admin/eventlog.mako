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
	background: rgba(0, 0, 0, 0.25);
	position: absolute;
	top: 0px;
	left: 0px;
	right: 0px;
	bottom: 0px;
	display: none;
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
            <br><a href="${url.current(offset=int(request.params.get('offset', 0))-50)}">Prev</a>
            | <a href="${url.current(offset=int(request.params.get('offset', 0))+50)}">Next</a>
		</div> 
		Event Log
	</h1>
	<script>
	function show_extra(id) {
		bl = document.getElementById("blackout");
		ex = document.getElementById("extratext");
		source = document.getElementById(id);
		ex.innerHTML = source.innerHTML;
		bl.style.display = "block";
	}
	function hide_extra() {
		bl = document.getElementById("blackout");
		bl.style.display = "none";
	}
	</script>
	<div id="blackout">
		<div id="extra">
			<div style="float: right;">
				[<a href="javascript: hide_extra()">Close</a>]
			</div>
			<div id="extratext">
			</div>
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
					<center>${event.module}:${event.line_num}</center>
					<br><a href="?module=${event.module}">Find other messages from this module</a>
					<br><a href="?module=${event.module}&line_num=${event.line_num}">Find other messages from this line</a>
					<br><a href="https://dev.civicboom.com/gitweb/?p=website;a=blob;f=src/${event.module}#l${event.line_num}">View source code</a>
				</div>
			</td>
			<td style="white-space: nowrap;">
				<a href="javascript: show_extra('extra_${event.id}_u');" style="overflow: hidden; width: 20em; display: block;">${h.shorten_url(event.url)}</a>
				<div id="extra_${event.id}_u" style="display: none;">
					<center>${event.url}</center>
					<br><a href="?url=${event.url}">Find other messages from this url</a>
					<br><a href="${event.url}">Visit this url</a>
				</div>
			</td>
			<td style="white-space: nowrap;">
				% if event.username == "None":
				<a href="javascript: show_extra('extra_${event.id}_a');">${event.address}</a>
				% else:
				<a href="javascript: show_extra('extra_${event.id}_a');">${event.username}</a>
				% endif
				<div id="extra_${event.id}_a" style="display: none;">
					<center>${event.username} (${event.address})</center>
					<br><a href="?username=${event.username}">Find other messages from this user</a>
					<br><a href="?address=${event.address}">Find other messages from this IP address</a>
					<br><a href="${url('member', id=event.username)}">Visit this user's profile</a>
				</div>
				% if event.persona != "None":
				(${event.persona})
				% endif
			</td>
			<td>${h.link_to_objects(event.message)|n}</td>
		</tr>
	% endfor
	</table>
</%def>
