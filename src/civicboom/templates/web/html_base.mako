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

    <div id="flash_message" style="position: absolute; top: 0px; left: 0px; right: 0px;" class="hidden_by_default status_${c.result['status']}">${c.result['message']}</div>
        
        <!-- animation for flash message -->
        <script type="text/javascript">
            function flash_message(json_message) {
                if (typeof(json_message) == "string") {json_message = {status:'ok', message:json_message};}
                if (json_message.message != "") {
                    $("#flash_message").removeClass("status_error").removeClass("status_ok").addClass("status_"+json_message.status);
                    $("#flash_message").text(json_message.message).slideDown("slow").delay(5000).slideUp("slow");
                }
            }
            % if c.result['message'] != "":
            <% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
            $(function() {flash_message(${json_message|n});});
            % endif
    </script>
    
</%def>


##------------------------------------------------------------------------------
## Logo & Tagline def (to be used in any sub pages)
##------------------------------------------------------------------------------

<%def name="tagline_markup()">
%if _("_tagline"):
<span class="tagline">${_("_tagline")}<sup>TM</sup></span>
%endif
</%def>
