<html>
	<head>
		<meta name="viewport" content="width=480, initial-scale=1">
<%
mode = "android"
ua = request.environ.get("HTTP_USER_AGENT").lower()
if "android" in ua:
	mode = "android"
%>
<style>
HTML, BODY, TABLE, TD, P {
	margin: 0px;
	border: 0px;
	padding: 0px;
}
HTML {
	font-family: sans-serif;
	font-weight: bold;
	font-size: 1.5em;
	background: #000;
	line-spacing:
}
A {
	text-decoration: none;
}
P {
	margin: 0.3em;
}
TABLE {
	width: 100%;
	height: 100%;
}
TD {
	height: 50%;
	vertical-align: middle;
	padding: 0.5em;
}
#android, #iphone, #blackberry, #civicboom {
	text-align: center;
	border-radius: 2em;
	width: 100%;
	height: 100%;
}

#android {
	background: #004400;
	border: 3px solid #008800;
}
#iphone {
	background: #444444;
	border: 3px solid #888888;
}
#blackberry {
	background: #440000;
	border: 3px solid #880000;
}
#civicboom {
	background: #000044;
	border: 3px solid #000088;
}
</style>
	</head>
	<body>

<table>
	<tr>
% if mode == "android" or mode == "all":
		<td>
<a href="market://details?id=com.civicboom.mobile2">
	<table id="android"><tr><td>
		<img src="/images/misc/qr-landing/android-text.png">
		<p><img src="/images/misc/qr-landing/android-logo.png">
		<p><img src="/images/misc/qr-landing/gta.png">
	</td></tr></table>
</a>
		</td>
% elif mode == "iphone" or mode == "all":
		<td>
<a href="">
	<table id="iphone"><tr><td>
		<img src="/images/misc/qr-landing/iphone-text.png">
		<p><img src="/images/misc/qr-landing/iphone-logo.png">
		<p><img src="/images/misc/qr-landing/gta.png">
	</td></tr></table>
</a>
		</td>
% elif mode == "blackberry" or mode == "all":
		<td>
<a href="">
	<table id="blackberry"><tr><td>
		<img src="/images/misc/qr-landing/blackberry.png">
		<p><img src="/images/misc/qr-landing/blackberry.png">
		<p><img src="/images/misc/qr-landing/gta.png">
	</td></tr></table>
</a>
		</td>
% endif
	</tr>
	<tr>
		<td colspan="3">
<a href="">
	<table id="civicboom"><tr><td>
		<img src="/images/misc/qr-landing/boom-text.png">
		<p><img src="/images/misc/qr-landing/boom-logo.png">
		<p><img src="/images/misc/qr-landing/vtw.png">
	</td></tr></table>
</a>
		</td>
	</tr>
</table>

	</body>
</html>
