<html>
	<head>
		<title>Civicboom - Internal Error</title>
	</head>
	<body style="text-align: center; vertical-align: middle;">

        <div style="padding:2em; background-color: #005493; color: white; display: inline-block;">
            <h1>CIVICFAIL</h1>
            
            <p style="font-size: 180%; font-weight: bold; margin: 0em;">KEEP<br/>CALM</p>
            <span style="font-weight: normal;">AND</span>
            <p style="font-size: 180%; font-weight: bold; margin: 0em;">MAKE A<br/>CUP OF TEA</p>
            <p>OUR TECH MONKEYS HAVE BEEN ALERTED</p>
        </div>

% if c.result:
    % if 'code' in c.result:
        <p>code: <b>${c.result['code']}</b>
    % endif
    
    % if 'message' in c.result:
        <br>message: <b>${c.result['message']}</b>
    % endif
% endif

        <!--#include file="/misc/feedback.frag"-->

	</body>
</html>
