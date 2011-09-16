
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
        <style type="text/css">
            body {border:0; margin:0; padding:0; font-family: sans-serif;}
            img {border:0;}
        </style>
    </head>
    <%
        site_url = h.url(controller='misc', action='titlepage', protocol='https', sub_domain='www', qualified=True)
    %>
    <body>
<table bgcolor="#DCE4F1" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td bgcolor="#FFFFFF">&nbsp;</td>
        <td bgcolor="#FFFFFF">
            <a href="${site_url}?r=e_l">
                <img src="${site_url}images/logo-v3-128x28.png" alt="${_("_site_name: _tagline")}" />
            </a>
        </td>
        <td bgcolor="#FFFFFF">&nbsp;</td>
    </tr><tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr><tr>
        <td width="20">&nbsp;</td>
        <td bgcolor="#FFFFFF">
            <h2>Hi,</h2>
            <p>${next.body() if callable(self.body) else self.body}</p>
        </td>
        <td width="20">&nbsp;</td>
    </tr><tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr><tr>
        <td>&nbsp;</td>
        <td>
            <h2>
                <a href="${h.url(controller='misc', action='new_article', protocol='https', sub_domain='www', qualified=True, r='e_p')}">Post a story</a><br />
            </h2>
            <a href="http://twitter.com/civicboom">
                <img src="${site_url}images/twitter-email.png" alt="Twitter"><br />
                Follow us
            </a>
        </td>
        <td>&nbsp;</td>
    </tr><tr>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr><tr>
        <td>&nbsp;</td>
        <td>
            If you'd rather not receive notifications from Civicboom, you can unsubscribe by going to your account
            settings. You can also manage all your notifications from your settings. Please don't reply to this
            message. No one will read it as it's been sent from an unmonitored email account. Which is a shame.
            So if you do want to get in touch please use <a href="mailto:contact@civicboom.com">contact@civicboom.com</a>. Thank you.
        </td>
        <td>&nbsp;</td>
    </tr>
</table>
</html>
</%def>

<%def name="footer()">
    <br/>
    <p>${_("Thanks!")}</p>
    <p>${_("_site_name team.")}</p>
</%def>
