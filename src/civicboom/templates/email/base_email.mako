
<%def name="subject()">${_('_site_name')}</%def>

##<%def name="subject()">${_("_site_name: _tagline")}</%def>

<%def name="body()">\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>${self.subject() if callable(self.subject) else self.subject}</title>
        <meta name="keywords" content="" />
        <meta name="Authors"  content="" />
        <meta name="robots"   content="all" />
##        <style type="text/css">
##            body {font-family: sans-serif; font-size: small;}
##            h2   {border-bottom: 2px solid black;}
##            p    {margin: 0em;}
##        </style>
    </head>
    
    <%
		site_url = h.url(controller='misc', action='titlepage', protocol='https', sub_domain='www', qualified=True)
    %>
    <body style="border:0; margin:0; padding:0; font-family: sans-serif;">
        <div style="padding: 1em 4em;">
            <h1 style="margin:0;">
                <a href="${site_url}">
                    <img src="${site_url}/images/logo-v2-128x32.png" alt="${_("_site_name: _tagline")}" style="margin-bottom:30px; border:none; max-width:200px;"/>
                </a>
            </h1>
        </div>
        <div style="padding: 2em; background: #DCE4F1;border-radius:0.5em;-moz-border-radius:0.5em;-webkit-border-radius:0.5em;">
            <div style="padding: 2em; background: #fff;border-radius:0.5em;-moz-border-radius:0.5em;-webkit-border-radius:0.5em;">
                <h2 style="margin: 0; margin-bottom: 0.25em;">Hi,</h2>
                <p>
                    ${next.body() if callable(self.body) else self.body}
                </p>
            </div>
            <h2>
                <a style="color: #005493; font: normal normal bold sans-serif;" href="${h.url(controller='misc', action='new_article', protocol='https', sub_domain='www', qualified=True)}">Post a story</a>
            </h2>
            <div style="float: right; text-align: right:">
                <a style="color: #005493; text-decoration: none; font: normal normal bold 125% sans-serif;" href="http://twitter.com/civicboom">
                    <img src="${site_url}/images/twitter-email.png" alt="Twitter" style="float: right;"><br />
                    Follow us
                </a>
            </div>
            <div style="font-size: 75%; width: 75%; float: left;">
                If you'd rather not receive notifications from Civicboom, you can unsubscribe by going to your account
                settings. You can also manage all your notifications from your settings. Please don't reply to this
                message. No one will read it as it's been sent from an unmonitored email account. Which is a shame.
                So if you do want to get in touch please use <a href="mailto:contact@civicboom.com">contact@civicboom.com</a>. Thank you.
            </div>
            <div style="clear: both"></div>
        </div>
    </body>
</html>
</%def>

<%def name="footer()">
    <br/>
    <p>${_("Thanks!")}</p>
    <p>${_("_site_name team.")}</p>
</%def>
