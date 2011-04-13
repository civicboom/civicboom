<html>
	<head>
		<title>Civicboom QR Landing Page</title>
<%
mode = "android"
ua = request.environ.get("HTTP_USER_AGENT",'').lower()
if "android" in ua:
	mode = "android"
%>
<style>
HTML, BODY {
	margin: 0px;
	border: 0px;
	padding: 0px;
	background: #000;
}
A {
	text-decoration: none;
	display: block;
	width: 90%;
	margin: auto;
	text-align: center;
	border-radius: 2em;
	padding: 1em;
}
IMG {
	max-width: 90%;
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

<p>&nbsp;

% if mode == "android" or mode == "all":
<a id="android" href="market://details?id=com.civicboom.mobile2">
	<img src="/images/misc/qr-landing/android-text.png">
	<br><img src="/images/misc/qr-landing/android-logo.png">
	<br><img src="/images/misc/qr-landing/gta.png">
</a>
% elif mode == "iphone" or mode == "all":
<a id="android" href="">
	<img src="/images/misc/qr-landing/iphone-text.png">
	<br><img src="/images/misc/qr-landing/iphone-logo.png">
	<br><img src="/images/misc/qr-landing/gta.png">
</a>
% elif mode == "blackberry" or mode == "all":
<a id="android" href="">
	<img src="/images/misc/qr-landing/blackberry.png">
	<br><img src="/images/misc/qr-landing/blackberry.png">
	<br><img src="/images/misc/qr-landing/gta.png">
</a>
% endif

<p>&nbsp;

<a id="civicboom" href="https://www.civicboom.com/">
	<img src="/images/misc/qr-landing/boom-text.png">
	<br><img src="/images/misc/qr-landing/boom-logo.png">
	<br><img src="/images/misc/qr-landing/vtw.png">
</a>

	</body>
</html>
