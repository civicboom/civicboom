<%inherit file="html_header.mako"/>

##------------------------------------------------------------------------------
## Default Base Components
##------------------------------------------------------------------------------
## Components such as Navigation, Header, Footer can be overridden by subclass's to add there own or remove it

<%def name="navigation()">
  <%include file="design09/includes/navigation.mako"/>
</%def>
<%def name="header()">
  <%include file="design09/includes/header.mako"/>
</%def>
<%def name="footer()">
  <%include file="design09/includes/footer.mako"/>
</%def>

## Depricated in redesign Jan10, could be re-implemented as the popup was useful
## AllanC: this is so some specail pages can add controls to the header banner, e.g the frontpage my have extra bits, the body has a margin so this cant be put in the normal body include
##<%def name="header_additions()"></%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <!-- header/banner -->
    ##role="banner" role landmarks are used for screen readers but it makes the XHTML invalid, commented out for now
    <div id="hd">
      ${self.header()}
      ${self.navigation()}
      ${flash_message()}
      ##${self.header_additions()}
    </div>
    <!-- end of header/banner -->
    
    <!-- main body --> 
    <div id="bd">
      ##${first_view_message()}
      ${next.body()}
    </div>
    <!-- end of main body -->
    
    <!-- footer -->
    <div id="ft">
      ${self.footer()}
    </div>
    <!-- end of footer-->
</%def>



##------------------------------------------------------------------------------
## Flash Message Area
##------------------------------------------------------------------------------
## Some form functions will need to return a status to inform users the operation completed
## This displays the message and then removes it from the session once it is displayed the first time
## See "Definitive Guide to Pylons" pg 191 for details
<%def name="flash_message()">
  % if session.has_key('flash_message'):
    <div id="flash_message">${session.get('flash_message')}</div>
    
    <!-- YUI animation for flash message -->
    <script type="text/javascript">
        var a = new YAHOO.util.Anim(YAHOO.util.Dom.get('flash_message'));
        a.attributes.opacity  = {to: 1};
        a.duration            = 5.0;
        ##a.attributes.height   = {to: 0};
          ##YAHOO.util.Easing.easeOut
        a.onComplete.subscribe(function() {
          var b = new YAHOO.util.Anim(YAHOO.util.Dom.get('flash_message'));
          b.attributes.opacity  = {to: 0};
          b.duration            = 1.0;
          b.attributes.height   = {to: 0};
          ##b.attributes.padding  = {to: 0};
          ##b.attributes.margin   = {to: 0};
          b.onComplete.subscribe(function() {
            ## AllanC - If the element is removed then IE gets confused and puts the footer at the top
            ## Why in gods name this happens is anybodys guess ... ****ing IE!
            ## I tryed other ways of removing the element with the same effect. Investigate IE dom
            ##
            ## Update, this is not an issue with the new layout, IE is behaving itself.
            YAHOO.util.Dom.setStyle('flash_message','display','none');
            ##YAHOO.util.Dom.setStyle('flash_message','margin','0em'); //an alternative was to set margin and padding to 0
          });
          b.animate();
        })
        a.animate();
    </script>
    
    <%
      del session['flash_message']
      #session.save()
    %>
  %endif
</%def>


##------------------------------------------------------------------------------
## First view popup
##------------------------------------------------------------------------------
<%def name="first_view_message()">
  % if not session.has_key('first_view_message'):
    <div id="first_view_message" class="popup hidden_by_default">
      ##${session.get('first_view_message')}
      <a class="popup_close_button" href="#" onclick="swap('first_view_message'); return false;"></a>
      <p><strong>${_("_site_name is undergoing exciting changes!")}</strong></p>
      <p>${_("We want your feedback! Tell us what you think:")} <a href="mailto:feedback@indiconews.com">feedback@indiconews.com</a></p>
      <br/>
      <p>${_("Thanks, from the _site_name Team.")}</p>
      <a class="first_view_message_close" href="#" onclick="swap('first_view_message'); return false;">${_("close")}</a>
    </div>
    <script type="text/javascript">swap('first_view_message');</script>
    <%
      session['first_view_message'] = '1'
      #session.save()
    %>
  % endif
</%def>



##------------------------------------------------------------------------------
## Logo & Tagline def (to be used in any sub pages)
##------------------------------------------------------------------------------

<%def name="tagline_markup()">
%if _("_tagline"):
<span class="tagline">${_("_tagline")}<sup>TM</sup></span>
%endif
</%def>

##<%def name="logo_small()">
##<a href="/"><img src="/design09/logo.png" class="logo_small"></a>
##</%def>
