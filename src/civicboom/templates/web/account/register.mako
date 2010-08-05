<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Additional CSS and Javascripts
##------------------------------------------------------------------------------
<%def name="head_links()">
    ${parent.head_links()}
  
    <!-- Additional YUI imports-->
    <link   type="text/css"        href="http://yui.yahooapis.com/2.8.1/build/calendar/assets/skins/sam/calendar.css" rel="stylesheet" />
    <script type="text/javascript" src ="http://yui.yahooapis.com/2.8.1/build/calendar/calendar-min.js"></script>

    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/button/assets/skins/sam/button.css" />
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/container/container_core-min.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/button/button-min.js"></script>
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
## Style Overrides
##------------------------------------------------------------------------------
<%def name="styleOverides()">
    /*
        Set the "zoom" property to "normal" since it is set to "1" by the 
        ".example-container .bd" rule in yui.css and this causes a Menu
        instance's width to expand to 100% of the browser viewport.
    */
    div.yuimenu .bd {zoom: normal;}

    /*
        Restore default padding of 10px for the calendar containtainer 
        that is overridden by the ".example-container .bd .bd" rule 
        in yui.css.
    */
    #calendarcontainer {padding:10px;}
    #calendarmenu {position: absolute;}
    #calendarpicker  {vertical-align: baseline;}
    #calendarpicker button {
        background: url(http://developer.yahoo.com/yui/examples/button/assets/calendar_icon.gif) center center no-repeat;
        text-align: left;
        text-indent: -10em;
        overflow: hidden;
        *margin-left: 10em; /* For IE */
        *padding: 0 3em;    /* For IE */
        white-space: nowrap;
    }
</%def>



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
    Username<input type="text" name="username" value="${c.logged_in_reporter.username}" />
</%def>

<%def name="email()">
    email<input type="text" name="email" value="${c.logged_in_reporter.email}" />
</%def>

<%def name="dob()">
  dob
  ${date_component()}
</%def>

<%def name="password()">
  ${h.get_captcha()}
  
  password<input type="password" name="password"         value="" />
  password confirm<input type="password" name="password_confirm" value="" />
</%def>


##------------------------------------------------------------------------------
## Date Component
##------------------------------------------------------------------------------
##


<%def name="date_component()">

<div class="yui-skin-sam">

    ## Reference: http://developer.yahoo.com/yui/examples/button/btn_example09.html
    <script type="text/javascript">
	(function () {
		var Event = YAHOO.util.Event, Dom = YAHOO.util.Dom;
        
        Event.onDOMReady(function () {
            var oCalendarMenu; // Create an Overlay instance to house the Calendar instance
            oCalendarMenu = new YAHOO.widget.Overlay("calendarmenu", { visible: false });
            var oButton = new YAHOO.widget.Button({ // Create a Button instance of type "menu"
                                                type: "menu", 
                                                id: "calendarpicker", 
                                                label: "Choose A Date", 
                                                menu: oCalendarMenu, 
                                                container: "datefields" });
            oButton.on("appendTo", function () {
                oCalendarMenu.setBody(" "); // Create an empty body element for the Overlay instance in order to reserve space to render the Calendar instance into.
                oCalendarMenu.body.id = "calendarcontainer";
            });
            var onButtonClick = function () {
                var oCalendar = new YAHOO.widget.Calendar("buttoncalendar", oCalendarMenu.body.id); // Create a Calendar instance and render it into the body element of the Overlay.
                oCalendar.render();
                oCalendar.selectEvent.subscribe(function (p_sType, p_aArgs) {  // Subscribe to the Calendar instance's "select" event to update the month, day, year form fields when the user selects a date.
                    var aDate;
                    if (p_aArgs) {
                        aDate = p_aArgs[0][0];
                        Dom.get("month-field").value = aDate[1];
                        Dom.get("day-field").value = aDate[2];
                        Dom.get("year-field").value = aDate[0];
                    }
                    oCalendarMenu.hide();
                });
                Event.on(oCalendarMenu.element, "keydown", function (p_oEvent) { // Pressing the Esc key will hide the Calendar Menu and send focus back to its parent Button
                    if (Event.getCharCode(p_oEvent) === 27) {
                        oCalendarMenu.hide();
                        this.focus();
                    }
                }, null, this);
                var focusDay = function () {
                    var oCalendarTBody = Dom.get("buttoncalendar").tBodies[0],
                        aElements = oCalendarTBody.getElementsByTagName("a"),
                        oAnchor;
                    if (aElements.length > 0) {
                        Dom.batch(aElements, function (element) {
                            if (Dom.hasClass(element.parentNode, "today")) {
                                oAnchor = element;
                            }
                        });
                        if (!oAnchor) {
                            oAnchor = aElements[0];
                        }
                        YAHOO.lang.later(0, oAnchor, function () { // Focus the anchor element using a timer since Calendar will try to set focus to its next button by default
                            try {
                                oAnchor.focus();
                            }
                            catch(e) {}
                        });
                    }
                };
                
                oCalendarMenu.subscribe("show", focusDay);  // Set focus to either the current day, or first day of the month in the Calendar	when it is made visible or the month changes
                oCalendar.renderEvent.subscribe(focusDay, oCalendar, true);
                focusDay.call(oCalendar); // Give the Calendar an initial focus
                oCalendarMenu.align(); // Re-align the CalendarMenu to the Button to ensure that it is in the correct position when it is initial made visible
                this.unsubscribe("click", onButtonClick); // Unsubscribe from the "click" event so that this code is  only executed once            
            };
            
            oButton.on("click", onButtonClick); // Add a "click" event listener that will render the Overlay, and  instantiate the Calendar the first time the Button instance is clicked.
        });
    }());
    </script>


    ##<form id="button-example-form" name="button-example-form" method="post">
        <fieldset id="datefields">
            <legend>Date</legend>
            <label for="month-field">Month: </label> <input id="month-field" type="text" name="month"/>
            <label for="day-field">Day:</label> <input id="day-field" type="text" name="day"/>
            <label for="year-field">Year: </label> <input id="year-field" type="text" name="year"/>
        </fieldset>
    ##</form>

    
<%doc>
    <script type="text/javascript">
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
    <div id="cal1Container"></div>
</%doc>

</div>    
</%def>

