
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
            body {font-family: sans-serif; font-size: small;}
            h2   {border-bottom: 2px solid black;}
            p    {margin: 0em;}
        </style>
    </head>
    
    <%
		site_url = h.url(controller='misc', action='titlepage', protocol='https', sub_domain='www', qualified=True)
    %>
    <body>
        <a href="${site_url}"><img src="${site_url}/images/logo.png" alt="${_("_site_name: _tagline")}" style="margin-bottom:30px; border:none; max-width:200px;"/></a>
        <br/>
        ${next.body() if callable(self.body) else self.body}
    </body>
</html>
</%def>

<%def name="footer()">
    <br/>
    <p>${_("Thanks!")}</p>
    <p>${_("_site_name team.")}</p>
</%def>
