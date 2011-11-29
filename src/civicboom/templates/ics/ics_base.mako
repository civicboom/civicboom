## REFERENCE
## http://www.ietf.org/rfc/rfc5545.txt
<%!
    # Dicts to convert between Civicboom terms and iCal terms
    status = {
        'accepted' : 'ACCEPTED',
        'withdrawn': 'DECLINED',
    }
    types = {
        'user' : 'INDIVIDUAL',
        'group': 'GROUP',
    }
    
    def api_datestr_to_icsdatestr(datetime):
        return h.api_datestr_to_datetime(datetime).strftime('%Y%m%dT%H%M%S')
%>

<%def name="body()">
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Civicboom//civicboom.com//
${next.body()}
END:VCALENDAR
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------
<%def name="ics_content_item(content)">
## Assignment
% if content.get('type') == 'assignment':
${assignment(content)}
% endif
## Draft
% if content.get('type') == 'draft' and content.get('target_type') == 'article':
${journal(content, **dict(STATUS='DRAFT'))}
% endif
## Article
% if content.get('type') == 'article':
<%
    journal_kwargs = {}
    if content.get('edit_lock'):
        journal_kwargs['STATUS'] = 'FINAL'
%>\
${journal(content, **journal_kwargs)}
%endif
</%def>






##------------------------------------------------------------------------------
## Member Item
##------------------------------------------------------------------------------
<%def name="ics_member_item(member)">
</%def>




##------------------------------------------------------------------------------
## Calendar objects
##------------------------------------------------------------------------------

## EVENT
## -----

<%def name="assignment(content)">
## Assignments may need 2 items raised.
##   Event date and Due date are separate events

## Event
% if content.get('event_date'):
<%
    event_date = h.api_datestr_to_datetime(content.get('event_date'))
    location = content.get('location').split()
    location.reverse()
%>
BEGIN:VEVENT
${ics_content_base(content)}
DTSTART:${api_datestr_to_icsdatestr(event_date)}
## Need to take into accout hour ... if hour is 00:00 then take whole day?
##DTEND ?
% if len(location)==2:
GEO:${";".join(location)}
LOCATION:${content.get('location_text')}
% endif
## If we are displaying a singl item of content then include extra fields
% try:
    % if d['content']['id'] == content['id']:
        % for atendee in d['accepted_status']['items'] :
        ##if status.get(atendee['status'])
ATTENDEE;ROLE=OPT-PARTICIPANT;PARTSTAT;${status.get(atendee['status'])};${ics_member(atendee)}
        % endfor
        % for comment in d['comments']['items']:
COMMENT:"${comment['creator']['name']} - ${comment['content']}
        % endfor
    % endif
% except Exception as e:
% endtry
## AllanC - TODO? How could we supoort TENTATIVE, CONFIRMED, CANCELLED
##          'CANCELLED' - what if this request is deleted? - we want it to come up as cancled, but we just remove it from the DB. Currently it is not possible to do this
END:VEVENT
% endif

## Todo
% if content.get('due_date'):
BEGIN:VTODO
${ics_content_base(content, child_id='due')}
DUE:${api_datestr_to_icsdatestr(content.get('due_date'))}
STATUS:NEEDS-ACTION
## "IN-PROCESS"   ;Indicates to-do in process of. - AllanC - could we look at the state of the response draft and if there is content in the content field it's 'in progress'?
END:VTODO
## 'COMPLETED'?
## Could we see if this user has responded to this
##COMPLETED:20070707T100000Z
% endif
</%def>


## JOURNAL
## -------
<%def name="journal(content, **kwargs)">
BEGIN:VJOURNAL
${ics_content_base(content, **kwargs)}
END:VJOURNAL
</%def>



##------------------------------------------------------------------------------
## Utils
##------------------------------------------------------------------------------
<%def name="ics_member(member)">\
CUTYPE=${types.get(member['type'])}:CN="${member['name']}":${member['url']}\
</%def>

<%def name="ics_langauge(content)">\
LANGUAGE=${content.get('langauge','en-US')}\
</%def>

##------------------------------------------------------------------------------
## Content Base fields
##------------------------------------------------------------------------------
<%def name="ics_content_item_base(content, child_id='', **kwargs)">
<%
    parent_id = content.get('parent_id') or content.get('parent',{}).get('id')
    if child_id:
        parent_id = content.get('id')
%>\
UID:"${h.url('contents', id=content.get('id'), child_id=child_id)}"
DTSTAMP:${api_datestr_to_icsdatestr(content.get('update_date'))}
SUMMARY;${ics_langauge(content)}:"${content['title']}"
DESCRIPTION;${ics_langauge(content)}:"${comment.get('content_short') or h.truncate(comment.get('content'), length=150, whole_word=True, indicator='...')}"
CATEGORIES:${content['tags']}
CLASS:${'PRIVATE' if content['private'] else 'PUBLIC'}
URL:content['url'])
ORGANIZER:${ics_member(content['creator'])}
##TRANSP:TRANSPARENT
% if parent_id:
RELATED-TO;RELTYPE=CHILD:"${h.url('contents', id=parent_id)}"
% endif
% for media in content.get('attachments'):
ATTACH:${media['original_url']}
##event.add('ATTACH' ,'FMTTYPE=%s/%s:%s' % (media['type'], media['subtype'], media['original_url'])) # AllanC - didnt want to attach the full items
% endfor
% for key, value in kwargs.iteritems():
${key}:${value}
% endfor
</%def>
