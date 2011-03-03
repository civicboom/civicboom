<html>
	<head>
		<title>Civicboom - Internal Error</title>
	</head>

    % if c.result.get('code') == 500:
	<body style="text-align: center; vertical-align: middle;">

        <div style="padding:2em; background-color: #005493; color: white; display: inline-block;">
            <h1>CIVICFAIL</h1>
            
            <p style="font-size: 180%; font-weight: bold; margin: 0em;">KEEP<br/>CALM</p>
            <span style="font-weight: normal;">AND</span>
            <p style="font-size: 180%; font-weight: bold; margin: 0em;">MAKE A<br/>CUP OF TEA</p>
            <p>OUR TECH MONKEYS HAVE BEEN ALERTED</p>
            <img src="/images/logo.png" style="float: right;"/>
        </div>
    % else:
    <body>
        <h1>Error</h1>
    % endif
    
        % if 'code' in c.result:
        <p>code: <b>${c.result['code']}</b>
        % endif
        
        <br/>
        
        % if 'message' in c.result:
        message: <b>${c.result['message']}</b>
        % endif
        
        <!--#include file="/misc/feedback.frag"-->

	</body>
</html>
