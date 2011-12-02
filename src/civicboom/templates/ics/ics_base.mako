## REFERENCE
## http://www.ietf.org/rfc/rfc5545.txt
<%!
    import re
    import datetime
    from cbutils.text import strip_html_tags
    from civicboom.lib.helpers import api_datestr_to_datetime
    
    # Dicts to convert between Civicboom terms and iCal terms
    status = {
        'accepted' : 'ACCEPTED',
        'withdrawn': 'DECLINED',
    }
    types = {
        'user' : 'INDIVIDUAL',
        'group': 'GROUP',
    }
    
    def api_datestr_to_icsdatestr(datetime, include_hour=True):
        if include_hour:
            return api_datestr_to_datetime(datetime).strftime('%Y%m%dT%H%M%S')
        else:
            return api_datestr_to_datetime(datetime).strftime('%Y%m%d')
%>

<%def name="body()">\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Civicboom//civicboom.com//
${next.body()}
END:VCALENDAR
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------
<%def name="ics_content_item(content)">\
## Assignment
% if content.get('type') == 'assignment':
${assignment(content)}\
% endif
## Draft
% if content.get('type') == 'draft' and content.get('target_type') == 'article':
${journal(content, **dict(STATUS='DRAFT'))}\
% endif
## Article
% if content.get('type') == 'article':
<%
    journal_kwargs = {}
    if content.get('edit_lock'):
        journal_kwargs['STATUS'] = 'FINAL'
%>\
${journal(content, **journal_kwargs)}\
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
##
## Event
% if content.get('event_date'):
<%
    event_date = h.api_datestr_to_datetime(content.get('event_date'))
    location = None
    if content.get('location'):
        location = content.get('location').split()
        location.reverse()
%>
BEGIN:VEVENT
${ics_content_base(content)}\
% if event_date.hour > 0:
DTSTART:${api_datestr_to_icsdatestr(event_date)}
DTEND:${api_datestr_to_icsdatestr(event_date+datetime.timedelta(hours=1))}
% else:
DTSTART;VALUE=DATE:${api_datestr_to_icsdatestr(event_date, include_hour=FALSE)}
% endif
TRANSP:TRANSPARENT
% if location and len(location)==2:
GEO:${";".join(location)}
LOCATION:${content.get('location_text')}
% endif
## If we are displaying a singl item of content then include extra fields
% try:
    % if d['content']['id'] == content['id']:
        % for atendee in d['accepted_status']['items']:
        ##if status.get(atendee['status'])
ATTENDEE;ROLE=OPT-PARTICIPANT;PARTSTAT;${status.get(atendee['status'])}${ics_member(atendee)}
        % endfor
    % endif
% except Exception as e:
% endtry
## AllanC - TODO? How could we supoort TENTATIVE, CONFIRMED, CANCELLED
##          'CANCELLED' - what if this request is deleted? - we want it to come up as cancled, but we just remove it from the DB. Currently it is not possible to do this
END:VEVENT
% else:
BEGIN:VTODO
${ics_content_base(content)}\
DTSTART:${api_datestr_to_icsdatestr(content.get('update_date'))}
END:VTODO
% endif
##
## Todo
% if content.get('due_date'):
BEGIN:VTODO
${ics_content_base(content, child_id='due')}\
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
${ics_content_base(content, **kwargs)}\
END:VJOURNAL
</%def>



##------------------------------------------------------------------------------
## Utils
##------------------------------------------------------------------------------
<%def name="ics_member(member)">\
% if isinstance(member, basestring):
:${h.url('member', id=member, qualified=True)}\
% else:
;CUTYPE=${types.get(member['type'])};CN="${member['name']}":${member['url']}\
% endif
</%def>

<%def name="ics_langauge(content_or_member)">\
LANGUAGE=${content_or_member.get('langauge') if content_or_member.get('langauge') else 'en-US'}\
</%def>

<%def name="ics_content_text(content)">\
<%
    if isinstance(content, basestring):
        text = content
    else:
        if content.get('type') == 'comment':
            text = content.get('content')
        else:
            text = content.get('content_short')
    text = re.sub(r'[\t\n\r\f\v]', '\\\\n', text)
%>\
${text}\
</%def>

##------------------------------------------------------------------------------
## Content Base fields
##------------------------------------------------------------------------------
<%def name="ics_content_base(content, **kwargs)">\
<%
    parent_id = content.get('parent_id') or content.get('parent',{}).get('id')
    # Overwrite parent_id with current id if this is a generated sub component
    uid_kwargs_additions = {}
    if kwargs.get('child_id'):
        parent_id = content.get('id')
        uid_kwargs_additions['child_id'] = kwargs['child_id']
        del kwargs['child_id']
    creator = content.get('creator') or content.get('creator_id')
%>\
UID:${h.url('content', id=content.get('id'), qualified=True, **uid_kwargs_additions)}
DTSTAMP:${api_datestr_to_icsdatestr(content.get('update_date'))}
SUMMARY;${ics_langauge(content)}:${content['title']}
DESCRIPTION;${ics_langauge(content)}:${ics_content_text(content)}
% if content['tags']:
CATEGORIES:${','.join(content['tags'])}
% endif
CLASS:${'PRIVATE' if content['private'] else 'PUBLIC'}
URL:${content['url']}
ORGANIZER${ics_member(creator)}
% if parent_id:
RELATED-TO;RELTYPE=CHILD:${h.url('content', id=parent_id, qualified=True)}
% endif
% for media in content.get('attachments',[]):
ATTACH:${media['original_url']}
##event.add('ATTACH' ,'FMTTYPE=%s/%s:%s' % (media['type'], media['subtype'], media['original_url'])) # AllanC - didnt want to attach the full items
% endfor
% for key, value in kwargs.iteritems():
${key}:${value}
% endfor
% try:
    % if d['content']['id'] == content['id']:
        % for comment in d['comments']['items']:
COMMENT;${ics_langauge(comment['creator'])}:${comment['creator']['name']} - ${ics_content_text(comment)}
        % endfor
        % for response in d['responses']['items']:
COMMENT;${ics_langauge(response)}:${response['title']} - ${ics_content_text(response)} - ${response['creator']['name']} - ${response['url']}
        % endfor
    % endif
% except Exception as e:
% endtry
</%def>