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
            <img src="/images/logo-v2-128x32.png" style="float: right;"/>
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

	% if c.result.get('code') == 404:
	<!--
		<hr>
		<p>
		<script type="text/javascript">
			var GOOG_FIXURL_LANG = 'en-GB';
			var GOOG_FIXURL_SITE = 'https://www.civicboom.com'
		</script>
		<script type="text/javascript"
			src="http://linkhelp.clients.google.com/tbproxy/lh/wm/fixurl.js">
		</script>
	-->
	% endif

		<hr>
        <h3>Feedback</h3>
        <!--#include virtual="/misc/feedback.frag"-->

	</body>
</html>
