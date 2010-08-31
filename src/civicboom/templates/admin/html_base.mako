<%!
from formalchemy.ext.pylons.controller import model_url
from pylons import url
%>
<html>
	<head>
		<title>${self.title()}</title>
		<link rel="stylesheet" type="text/css" href="${url('fa_static', path_info='/admin.css')}" />
		<script type="text/javascript" src="/javascript/_combined.js"></script>
		<style>
TABLE.outer {
	width: 90%;
	margin: auto;
}
TABLE.outer > TBODY > TR > TD {
	border: none;
	width: 50%;
}
TABLE.outer TABLE {
	width: 95%;
}

#content, #header {
	border: 1px solid black;
	border-radius: 5px;
}
#header {
	box-shadow: 5px 5px 5px #CCC;
	-webkit-box-shadow: 5px 5px 5px #CCC;
	-moz-box-shadow: 5px 5px 5px #CCC;
	margin-bottom: 16px;
}
#content {
	box-shadow: 5px 5px 5px #AAA;
	-webkit-box-shadow: 5px 5px 5px #AAA;
	-moz-box-shadow: 5px 5px 5px #AAA;
}
.breadcrumb {
	font-size: 0.5em;
}
TEXTAREA {
	border:1px solid #F5F5F5;
	border-left-color:#DDD;
	border-top-color:#DDD;
}
TD A {
    display: inline;
}
		</style>
		% if hasattr(self,'styleOverides'):
		<style type="text/css">
${self.styleOverides()}
		</style>
		% endif
	</head>
	<body>
		<div id="content" class="ui-admin ui-widget">
${self.body()}
		</div>
	</body>
</html>
