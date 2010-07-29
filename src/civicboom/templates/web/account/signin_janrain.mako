<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Sign in")}</%def>

##------------------------------------------------------------------------------
## Navigation override - remove it
##------------------------------------------------------------------------------
<%def name="navigation()"></%def>

##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
##<%def name="styleOverides()">
##fieldset{height: 12em;}
##</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

 <iframe src="http://civicboom.rpxnow.com/openid/embed?token_url=http%3A%2F%2Flocalhost%3A5000%2Faccount%2Fsignin_janrain"  scrolling="no"  frameBorder="no"  allowtransparency="true"  style="width:400px;height:240px"></iframe> 

</%def>