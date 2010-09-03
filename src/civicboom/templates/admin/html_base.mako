<%!
from formalchemy.ext.pylons.controller import model_url
from pylons import url
%>
<html>
	<head>
		<title>${self.title()}</title>
		<link rel="stylesheet" type="text/css" href="${url('fa_static', path_info='/admin.css')}" />
		<link rel="stylesheet" type="text/css" href="/styles/jquery.ui-1.8.4.css" />
		<script type="text/javascript" src="/javascript/jquery-1.4.2.js"></script>
		<script type="text/javascript" src="/javascript/jquery.ui-1.8.4.js"></script>
		<style>
TABLE.outer {width: 90%; margin: auto;}
TABLE.outer > TBODY > TR > TD {border: none; width: 50%;}
TABLE.outer TABLE {width: 95%;}

TD A {display: inline;}
TD > INPUT[type="text"],
TD > TEXTAREA,
TD > SELECT {width: 100%;}
TD > TEXTAREA {height: 150px;}
.input_row TD:first-child {
	vertical-align: middle;
	text-align: right;
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
