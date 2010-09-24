<html>
    <head>
        <title>Search Page</title>
        <style>
.and, .or, .not, .fil {
    padding: 16px;
    border: 1px solid black;
}   
.and {background: #AFA;}
.or  {background: #AAF;}
.not {background: #FAA;}
.fil {background: #FFF;}
        </style>
    </head>
    <body>
<%
from civicboom.lib.search import html
f = c.result['data']['feed']
%>
<h1>${f.name}</h1>
${html(f.query)|n}
	</body>
</html>
