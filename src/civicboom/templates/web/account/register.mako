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

    <form action="" method="post">
        % for field in c.required_fields:
            % if field=='username':
              ${username()}
            % endif
            % if field=='email':
              ${email()}
            % endif
            % if field=='dob':
              ${dob()}
            % endif
            % if field=='password':
              ${password()}
            % endif
            ##${eval(field)} wanted to just eval the field name but mako defs use differnt python names :( it's going to have to be a set of IF's
            

        % endfor
        <input type="checkbox" name="terms" value="checked" />${_("Agree to terms")}
        <input type="submit" name="submit" value="${_("Register")}"/>
    </form>

</%def>

##------------------------------------------------------------------------------
## Optional Required component defs
##------------------------------------------------------------------------------
<%def name="username()">
  username
</%def>

<%def name="email()">
  email
</%def>

<%def name="dob()">
  dob
  ${date_component()}
</%def>

<%def name="password()">.
  captcha & password
</%def>


##------------------------------------------------------------------------------
## Date Component
##------------------------------------------------------------------------------
##
## Reference: http://developer.yahoo.com/yui/examples/button/btn_example09.html

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