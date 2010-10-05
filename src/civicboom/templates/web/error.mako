<html>
	<head>
		<title>Error</title>
		<style>
H1 {
	text-align: center;
}
		</style>
	</head>
	<body>

<h1>Civicboom Internal Error</h1>

##<p>Code:    ${c.error_code}</p>
##<p>Prefix:  ${c.error_prefix}</p>
##<p>Message: ${c.error_message}</p>
% if c.result:
% if 'code' in c.result:
    <p>code: <b>${c.result['code']}</b>
% endif

% if 'message' in c.result:
    <br>message: <b>${c.result['message']}</b>
% endif
% endif

<!--
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
here is some padding to bring the page over 512 bytes
-->

	</body>
</html>
