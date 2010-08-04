<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Additional CSS and Javascripts
##------------------------------------------------------------------------------
<%def name="head_links()">
  ${parent.head_links()}
  
  <!-- Additional YUI imports-->
  <link   type="text/css"        href="http://yui.yahooapis.com/2.8.1/build/calendar/assets/skins/sam/calendar.css" rel="stylesheet">
  <script type="text/javascript" src ="http://yui.yahooapis.com/2.8.1/build/calendar/calendar-min.js"></script>
    
</%def>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Register")}</%def>

##------------------------------------------------------------------------------
## Navigation override - remove it
##------------------------------------------------------------------------------
<%def name="navigation()"></%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

  % for field in c.required_fields:
    
  % endfor

username

% if not c.logged_in_user.email or c.logged_in_user.email == "":
  email needed
% endif

## if not janrain user then captcha is need
% if True:
  captcha
  password
  
% endif

% if True:
##'dob' not in c.logged_in_user.config:
  dob needed
  

% endif


</%def>


##------------------------------------------------------------------------------
## Date Component
##------------------------------------------------------------------------------

<%def name="date_component()">
    <script>
        YAHOO.namespace("example.calendar");
        YAHOO.example.calendar.init = function() {
            
            var navConfig = {
                  strings : {
                      month      : "${_('Choose Month')}",
                      year       : "${_('Enter Year')}",
                      submit     : "${_('OK')}",
                      cancel     : "${_('Cancel')}",
                      invalidYear: "${_('Please enter a valid year')}"
                  },
                  monthFormat: YAHOO.widget.Calendar.LONG,
                  initialFocus: "year"
            };
            
            YAHOO.example.calendar.cal1 = new YAHOO.widget.Calendar("cal1","cal1Container", {navigator:navConfig});
            YAHOO.example.calendar.cal1.render();
        }
        YAHOO.util.Event.onDOMReady(YAHOO.example.calendar.init);
    </script>

    <div class="yui-skin-sam">
        <div id="cal1Container"></div>
    </div>
</%def>