<html>
    <head>
        <title>${_('_site_name')}: ${_('Browser Unsupported')}</title>
        <script src="${h.wh_url("public", "javascript/_combined.head.js")}"></script>
        <script src="/javascript/jquery.cookie.js"></script>
    </head>
    
    <body>
        <div style="text-align: center;">
            <div style="text-align: left; width: 750px; margin-left: auto; margin-right: auto;">
            
            <h1>Errr... sorry about this but <img src="/images/logo-v2-128x32.png" alt="${_('_site_name')}" style="height: 1.5em; position: relative; top: 0.5em;" /> doesn't support Microsoft Internet Explorer 7</h1>
            <p>We do however support Internet Explorer 8 and 9!</p>
            
            <p>You can still access Civicboom with IE7, it's just really not that pretty. If you want to continue using the site in Internet Explorer 7 click <a href="${h.url(controller='misc', action='titlepage')}" onclick="allow_lt_ie8(); redirect('${h.url(controller='misc', action='titlepage')}'); return false;">here</a></p>
            
            <p>So if you want to experience Civicboom in all its glory (and probably lots of other cool sites), take a look at <a href="http://www.browserchoice.eu/">Browser Choice</a> to get a list of different browsers available.</p>
            <p>Or if you want to upgrade with Internet Explorer go <a href="http://windows.microsoft.com/en-US/internet-explorer/downloads/ie">here</a>.</p>
            
            <p>Pssst: If you don't have the privileges to upgrade, why not have a quiet chat with your systems admin - see if they can help</p>
            </div>
            
            <%doc>
            <h1>${_('Browser Unsupported')}</h1>
            
            <!--[if lt IE 8 ]>
            <p>${_('You are currently using Internet Explorer 7 or below')}</p>
            <![endif]-->
            <p>${_('_site_name will not function with your current web browser software. You require a software upgrade to use the site.')}
            
            <p>${_('Please upgrade your browser by visiting ')}<a href="http://www.browserchoice.eu/">www.browserchoice.eu</a></p>
            <p>${_('If you are using a company manged machine please enocourage your systems administrator to upgrade.')}</p>
            </%doc>
        </div>
        
        <script type="text/javascript">
            function allow_lt_ie8() {
                $.cookie('allow_lt_ie8', 'True', {path: '/'});
            }
            function redirect(url) {
                window.location = url;
            }
        </script>
    </body>
</html>
