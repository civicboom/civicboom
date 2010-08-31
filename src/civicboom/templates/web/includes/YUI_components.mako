<%doc>
Each of these YUI components require aditional Javascript and CSS includes

TODO: these should be documented for each component
      in an ideal world it would be nice if these imports could be done automatically, but this is not possible because we have no way of keeping track which ones have been added in previous templates without implemeanting a crazy dependency system
</%doc>


##------------------------------------------------------------------------------
## File Uploader
##------------------------------------------------------------------------------
<%def name="file_uploader(progressbar_size=(300,5))">
    
    ## YUI 2.8.1 - File Uploader Component
    ## Reference - http://developer.yahoo.com/yui/uploader/
    
    ## Overlay a transparent SWF object over the button by using CSS absolute positioning
    <div id="uploaderContainer" style="width:80px; height:30px; position: absolute"></div>
    <button type="button"                                            >Select file</button>
    <button type="button" onClick="upload();           return false;">Upload     </button>
    <button type="button" onClick="handleClearFiles(); return false;">Clear      </button>
    
    <div style="border: black 1px solid; width:${progressbar_size[0]}px; height:40px;">
        <div id="upload_file"     style="text-align:center; margin:5px; font-size:15px; width:${progressbar_size[0]-10}px; height:25px; overflow:hidden"></div>
        <div id="upload_progress" style="width:${progressbar_size[0]}px;height:${progressbar_size[1]}px;background-color:#CCCCCC"></div>
    </div>

    <script type="text/javascript">
        YAHOO.widget.Uploader.SWFURL = "http://yui.yahooapis.com/2.8.1/build/uploader/assets/uploader.swf";
        ## Flash has a security model to stop uploaded to unauthorised domains
        ## If the .swf file is not served fromt the local server
        ## the file crossdomain.xml MUST be present in the root public dir for the flash component to upload to the server
        ## Example crossdomain.xml
        ##  <?xml version="1.0"?>
        ##  <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
        ##  <cross-domain-policy>
        ##    <allow-access-from domain="*"/>
        ##    <site-control permitted-cross-domain-policies="master-only"/>
        ##  </cross-domain-policy>

        
        var uploader = new YAHOO.widget.Uploader( "uploaderContainer" ); //, "assets/buttonSprite.jpg"
        var fileID;
    
        uploader.addListener('contentReady'      , handleContentReady);
        uploader.addListener('fileSelect'        , onFileSelect      );
        uploader.addListener('uploadStart'       , onUploadStart     );
        uploader.addListener('uploadProgress'    , onUploadProgress  );
        uploader.addListener('uploadCancel'      , onUploadCancel    );
        uploader.addListener('uploadComplete'    , onUploadComplete  );
        uploader.addListener('uploadCompleteData', onUploadResponse  );
        uploader.addListener('uploadError'       , onUploadError     );
    
        function handleContentReady () {
            uploader.setAllowLogging(true);  	   // Allows the uploader to send log messages to trace, as well as to YAHOO.log
            uploader.setAllowMultipleFiles(false); // Restrict selection to a single file (that's what it is by default).
            var ff = new Array({description:"Images", extensions:"*.jpg;*.png;*.gif;*.jpeg"}, // New set of file filters.
                               {description:"Videos", extensions:"*.avi;*.mov;*.mpg;*.3gp;*.3gpp;*.flv;*.mp4"});
            uploader.setFileFilters(ff);           // Apply new set of file filters to the uploader.
        }

        function handleClearFiles() {
            uploader.clearFileList();
            uploader.enable();
            fileID = null;
            document.getElementById("upload_file"    ).innerHTML = "";
            document.getElementById("upload_progress").innerHTML = "";
        }

        function onFileSelect(event) {
            for (var item in event.fileList) {
                if(YAHOO.lang.hasOwnProperty(event.fileList, item)) {
                    YAHOO.log(event.fileList[item].id);
                    fileID = event.fileList[item].id;
                }
            }
            uploader.disable();
            document.getElementById("upload_file"    ).innerHTML = event.fileList[fileID].name;
            document.getElementById("upload_progress").innerHTML = "";
        }
    
        function upload() {
            if (fileID != null) {
                ##uploader.upload(fileID, "${app_globals.site_url}/content/upload_media/${c.content_media_upload_key}", "POST");
                uploader.upload(fileID, "${url(host=app_globals.site_host, controller='content', action='upload_media', id=c.content_media_upload_key)}", "POST");
                fileID = null;
            }
        }

        function onUploadProgress(event) {
            setProgressBar(event["bytesLoaded"]/event["bytesTotal"]);
        }
        
        function onUploadComplete(event) {
            uploader.clearFileList();
            uploader.enable();
            setProgressBar(1);
            ## submit save draft (to reload page with preview thumbnail)
        }

        function onUploadStart   (event) {YAHOO.log("Upload Start");    YAHOO.log(event);}
        function onUploadError   (event) {YAHOO.log("Upload Error");    YAHOO.log(event);}
        function onUploadCancel  (event) {YAHOO.log("Upload Cancel");   YAHOO.log(event);}
        function onUploadResponse(event) {YAHOO.log("Upload Response"); YAHOO.log(event);}

        function setProgressBar(percent) {
            document.getElementById("upload_progress").innerHTML = "<div style='background-color: #0f0; height: ${progressbar_size[1]}px; width: "+ Math.round(percent*${progressbar_size[0]}) + "px'/>";
        }

    </script>

</%def>


##------------------------------------------------------------------------------
## Date Component
##------------------------------------------------------------------------------

<%def name="calendar(form_field_name='form_date')">



    <%doc>
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
    </%doc>



<div class="yui-skin-sam">

<%doc>
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
</%doc>
    

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
            
            YAHOO.example.calendar.${form_field_name} = new YAHOO.widget.Calendar("${form_field_name}","${form_field_name}Container", {navigator:navConfig, pagedate: "1/1980", selected: "1/1/1980"});
            YAHOO.example.calendar.${form_field_name}.render();
            
            YAHOO.example.calendar.${form_field_name}.selectEvent.subscribe(function (type, args, obj) {
                var dates = args[0];
                var date  = dates[0];
                var year  = date[0], month = date[1], day = date[2];
                YAHOO.log("year:"+year);
                YAHOO.util.Dom.get("${form_field_name}").value = day+'/'+month+'/'+year;
            });
        }
        YAHOO.util.Event.onDOMReady(YAHOO.example.calendar.init);
    </script>
    <div id="${form_field_name}Container"></div>

    <input id="${form_field_name}" type="text" name="${form_field_name}"/>

</div>
</%def>

