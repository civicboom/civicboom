<%!
    import icalendar
    
    status = {
        'accepted' : 'ACCEPTED',
        'withdrawn': 'DECLINED',
    }
    types = {
        'user' : 'INDIVIDUAL',
        'group': 'GROUP',
    }
    
    def ical_member(member):
        return 'CUTYPE=%s:CN="%s":%s' % (types.get(member['type']), member['name'], member['url'])
    
    def ical_langauge(content):
        return 'LANGUAGE=%s' % content.get('langauge','en-US')
    
    def ical_content(content, ical_obj):
        ical_obj.add('SUMMARY'    , '%s:%s' % (ical_langauge(content), content['title'])
        ical_obj.add('DESCRIPTION', comment.get('content_short') or h.truncate(comment.get('content'), length=150, whole_word=True, indicator='...')
        ical_obj.add('CATEGORIES' , content['tags'])
        ical_obj.add("CLASS"      , 'PRIVATE' if content['private'] else 'PUBLIC')
        ical_obj.add("URL"        , content['url'])
        ical_obj.add('ORGANIZER'  , ical_member(content['creator']))
        ical_obj.add('DTSTAMP'    , h.api_datestr_to_datetime(content.get('update_date'))
        
        for media in content['attachments']:
            event.add('ATTACH' , media['original_url'])
            #event.add('ATTACH' ,'FMTTYPE=%s/%s:%s' % (media['type'], media['subtype'], media['original_url'])) # AllanC - didnt want to attach the full items

%>

<%def name="body()"><%
    self.cal = icalendar.Calendar()
    cal = self.cal
    cal.add('prodid', '-//Civicboom//civicboom.com//')
    cal.add('version', '2.0')
%>\
${next.body()}\
${cal.as_string()}
</%def>

<%def name="ical_member_item(member)">
</%def>

<%def name="ical_content_item(content)"><%
    if content.get('type') == 'assignment':
        if content.get('event_date'):
            event_date = h.api_datestr_to_datetime(content.get('event_date')
            
            event = Event()
            
            ical_content(content, event)
            
            event.add('dtstart', event_date) # Need to take into accout hour ... if hour is 00:00 then take whole day?
            event.add('dtend'  , )
            
            event['uid'] = content.get('id') + 'event'
            
            location = content.get('location').split()
            location.reverse()
            if len(location)==2:
                event.add('GEO', ";".join(location))
            event.add('LOCATION', content.get('location_text'))
            
            #for atendee in d['accepted_status']['items'] if status.get(atendee['status']):
            #    event.add('ATTENDEE', 'ROLE=OPT-PARTICIPANT;PARTSTAT=%s;%s' % (status.get(atendee['status']), ical_member(atendee) ))
            #for comment in d['comments']['items']:
            #    event.add('COMMENT', "%s: %s" % (comment['creator']['name'], comment['content']) )
            
            self.cal.add_component(event)
            
        if content.get('due_date'):
            todo = icalendar.Todo()
            ical_content(content, todo)
            
            todo.add('DUE', h.api_datestr_to_datetime(content.get('due_date'))
            todo['uid'] = content.get('id') + 'due'
            
            todo.add('STATUS', 'NEEDS-ACTION') # 'COMPLETED'

            #DTSTART:20070514T110000Z
            #DUE:20070709T130000Z
            #COMPLETED:20070707T100000Z
    
    if content.get('type') == 'draft':
        #.add('STATUS', 'DRAFT')
        
%></%def>

<%doc>

REFERENCE

http://www.ietf.org/rfc/rfc5545.txt


ATTENDEE;RSVP=TRUE;ROLE=REQ-PARTICIPANT:mailto:jsmith@example.com
ATTACH:http://example.com/public/quarterly-report.doc

ORGANIZER;CN="John Smith":mailto:jsmith@example.com
ATTENDEE;CUTYPE=GROUP:mailto:ietf-calsch@example.org

ATTENDEE;DELEGATED-FROM="mailto:jsmith@example.com":mailto:jdoe@example.com
        
ORGANIZER;DIR="ldap://example.com:6666/o=ABC%20Industries, c=US???(cn=Jim%20Dolittle)":mailto:jimdo@example.com
        
ATTACH;FMTTYPE=application/msword:ftp://example.com/pub/docs/agenda.doc

SUMMARY;LANGUAGE=en-US:Company Holiday Party

LOCATION;LANGUAGE=en:Germany

ATTENDEE;PARTSTAT=DECLINED:mailto:jsmith@example.com

RELATED-TO;RELTYPE=SIBLING:19960401-080045-4000F192713@example.com

ATTENDEE;RSVP=TRUE:mailto:jsmith@example.com

ORGANIZER;SENT-BY="mailto:sray@example.com":mailto:jsmith@example.com


duration -- P15DT5H0M20S


GEO:37.386013;-122.082932

       LOCATION:Conference Room - F123\, Bldg. 002

       LOCATION;ALTREP="http://xyzcorp.com/conf-rooms/f123.vcf":
        Conference Room - F123\, Bldg. 002



       statvalue       = (statvalue-event
                       /  statvalue-todo
                       /  statvalue-jour)

       statvalue-event = "TENTATIVE"    ;Indicates event is tentative.
                       / "CONFIRMED"    ;Indicates event is definite.
                       / "CANCELLED"    ;Indicates event was cancelled.
       ;Status values for a "VEVENT"

       statvalue-todo  = "NEEDS-ACTION" ;Indicates to-do needs action.
                       / "COMPLETED"    ;Indicates to-do completed.
                       / "IN-PROCESS"   ;Indicates to-do in process of.
                       / "CANCELLED"    ;Indicates to-do was cancelled.
       ;Status values for "VTODO".

       statvalue-jour  = "DRAFT"        ;Indicates journal is draft.
                       / "FINAL"        ;Indicates journal is final.
                       / "CANCELLED"    ;Indicates journal is removed.

 Purpose:  This property defines the date and time that a to-do was
      actually completed.

COMPLETED:19960401T150000Z

   Purpose:  This property defines the date and time that a to-do is
      expected to be completed.

DUE:19980430T000000Z


       

      The following is an example of this property for an event that is
      opaque or blocks on free/busy time searches:
       TRANSP:OPAQUE
       TRANSP:TRANSPARENT

UTC offset
       TZOFFSETFROM:-0500
       
ORGANIZER;CN=John Smith:mailto:jsmith@example.com


URL:http://example.com/pub/calendars/jsmith/mytime.ics



DTSTAMP
this is the update date


     icalparameter = altrepparam       ; Alternate text representation
                   / cnparam           ; Common name
                   / cutypeparam       ; Calendar user type
                   / delfromparam      ; Delegator
                   / deltoparam        ; Delegatee
                   / dirparam          ; Directory entry
                   / encodingparam     ; Inline encoding
                   / fmttypeparam      ; Format type
                   / fbtypeparam       ; Free/busy time type
                   / languageparam     ; Language for text
                   / memberparam       ; Group or list membership
                   / partstatparam     ; Participation status
                   / rangeparam        ; Recurrence identifier range
                   / trigrelparam      ; Alarm trigger relationship
                   / reltypeparam      ; Relationship type
                   / roleparam         ; Participation role
                   / rsvpparam         ; RSVP expectation
                   / sentbyparam       ; Sent by
                   / tzidparam         ; Reference to time zone object
                   / valuetypeparam    ; Property value data type
                   / other-param



http://en.wikipedia.org/wiki/ICalendar    

-- EVENT --

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
BEGIN:VEVENT
UID:uid1@example.com
DTSTAMP:19970714T170000Z
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
DTEND:19970715T035959Z
SUMMARY:Bastille Day Party
END:VEVENT
END:VCALENDAR

       BEGIN:VEVENT
       UID:19970901T130000Z-123401@example.com
       DTSTAMP:19970901T130000Z
       DTSTART:19970903T163000Z
       DTEND:19970903T190000Z
       SUMMARY:Annual Employee Review
       CLASS:PRIVATE
       CATEGORIES:BUSINESS,HUMAN RESOURCES
       END:VEVENT

       BEGIN:VEVENT
       UID:19970901T130000Z-123402@example.com
       DTSTAMP:19970901T130000Z
       DTSTART:19970401T163000Z
       DTEND:19970402T010000Z
       SUMMARY:Laurel is in sensitivity awareness class.
       CLASS:PUBLIC
       CATEGORIES:BUSINESS,HUMAN RESOURCES
       TRANSP:TRANSPARENT
       END:VEVENT

-- TODO --

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ABC Corporation//NONSGML My Product//EN
BEGIN:VTODO
DTSTAMP:19980130T134500Z
SEQUENCE:2
UID:uid4@host1.com
ORGANIZER:MAILTO:unclesam@us.gov
ATTENDEE;PARTSTAT=ACCEPTED:MAILTO:jqpublic@example.com
DUE:19980415T235959
STATUS:NEEDS-ACTION
SUMMARY:Submit Income Taxes
BEGIN:VALARM
ACTION:AUDIO
TRIGGER:19980403T120000
ATTACH;FMTTYPE=audio/basic:http://example.com/pub/audio-
 files/ssbanner.aud
REPEAT:4
DURATION:PT1H
END:VALARM
END:VTODO
END:VCALENDAR


       BEGIN:VTODO
       UID:20070313T123432Z-456553@example.com
       DTSTAMP:20070313T123432Z
       DUE;VALUE=DATE:20070501
       SUMMARY:Submit Quebec Income Tax Return for 2006
       CLASS:CONFIDENTIAL
       CATEGORIES:FAMILY,FINANCE
       STATUS:NEEDS-ACTION
       END:VTODO

       BEGIN:VTODO
       UID:20070514T103211Z-123404@example.com
       DTSTAMP:20070514T103211Z
       DTSTART:20070514T110000Z
       DUE:20070709T130000Z
       COMPLETED:20070707T100000Z
       SUMMARY:Submit Revised Internet-Draft
       PRIORITY:1
       STATUS:NEEDS-ACTION
       END:VTODO


--JOURNAL--

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ABC Corporation//NONSGML My Product//EN
BEGIN:VJOURNAL
DTSTAMP:19970324T120000Z
UID:uid5@host1.com
ORGANIZER:MAILTO:jsmith@example.com
STATUS:DRAFT
CLASS:PUBLIC
CATEGORIES:Project Report, XYZ, Weekly Meeting
DESCRIPTION:Project xyz Review Meeting Minutes\n
 Agenda\n1. Review of project version 1.0 requirements.\n2.
 Definition
 of project processes.\n3. Review of project schedule.\n
 Participants: John Smith, Jane Doe, Jim Dandy\n-It was
  decided that the requirements need to be signed off by
  product marketing.\n-Project processes were accepted.\n
 -Project schedule needs to account for scheduled holidays
  and employee vacation time. Check with HR for specific
  dates.\n-New schedule will be distributed by Friday.\n-
 Next weeks meeting is cancelled. No meeting until 3/23.
END:VJOURNAL
END:VCALENDAR



       BEGIN:VJOURNAL
       UID:19970901T130000Z-123405@example.com
       DTSTAMP:19970901T130000Z
       DTSTART;VALUE=DATE:19970317
       SUMMARY:Staff meeting minutes
       DESCRIPTION:1. Staff meeting: Participants include Joe\,
         Lisa\, and Bob. Aurora project plans were reviewed.
         There is currently no budget reserves for this project.
         Lisa will escalate to management. Next meeting on Tuesday.\n
        2. Telephone Conference: ABC Corp. sales representative
         called to discuss new printer. Promised to get us a demo by
         Friday.\n3. Henry Miller (Handsoff Insurance): Car was
         totaled by tree. Is looking into a loaner car. 555-2323
         (tel).
       END:VJOURNAL


-- BUSY --

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//RDU Software//NONSGML HandCal//EN
BEGIN:VFREEBUSY
ORGANIZER:MAILTO:jsmith@example.com
DTSTART:19980313T141711Z
DTEND:19980410T141711Z
FREEBUSY:19980314T233000Z/19980315T003000Z
FREEBUSY:19980316T153000Z/19980316T163000Z
FREEBUSY:19980318T030000Z/19980318T040000Z
URL:http://www.example.com/calendar/busytime/jsmith.ifb
END:VFREEBUSY
END:VCALENDAR

-- ALARMS --


       BEGIN:VALARM
       TRIGGER;VALUE=DATE-TIME:19970317T133000Z
       REPEAT:4
       DURATION:PT15M
       ACTION:AUDIO
       ATTACH;FMTTYPE=audio/basic:ftp://example.com/pub/
        sounds/bell-01.aud
       END:VALARM
       
       BEGIN:VALARM
       TRIGGER:-PT30M
       REPEAT:2
       DURATION:PT15M
       ACTION:DISPLAY
       DESCRIPTION:Breakfast meeting with executive\n
        team at 8:30 AM EST.
       END:VALARM

       BEGIN:VALARM
       TRIGGER;RELATED=END:-P2D
       ACTION:EMAIL
       ATTENDEE:mailto:john_doe@example.com
       SUMMARY:*** REMINDER: SEND AGENDA FOR WEEKLY STAFF MEETING ***
       DESCRIPTION:A draft agenda needs to be sent out to the attendees
         to the weekly managers meeting (MGR-LIST). Attached is a
         pointer the document template for the agenda file.
       ATTACH;FMTTYPE=application/msword:http://example.com/
        templates/agenda.doc
       END:VALARM

</%doc>