"""
Python log of emails that have been sent
Used by unit tests to check email output
"""

from pylons import config

import logging
log = logging.getLogger(__name__)

emails = []


class Email:
    def __init__(self, email_to, subject, content_text, content_html, **kwargs):
        self.email_to     = email_to
        self.subject      = subject
        self.content_text = content_text
        self.content_html = content_html


def email_log(email_to, **kwargs): #subject, content_text, content_html,
    log.info("--Email Send Disabled-- To: %s Subject: %s" % (email_to, kwargs.get('subject')) )
    log.debug("Message (content_text): %s" % kwargs.get('content_text') )
    #log.debug("Message (content_html): %s" % content_html)
    
    if config['test_mode']:
        #print "Email: %s - %s" %(email_to, subject)
        emails.append(Email(email_to, **kwargs)) #subject, content_text, content_html
    

def getNumEmails():
    return len(emails)


def getLastEmail(offset = 1):
    return emails[0 - offset]


def getEmailSubjects():
    return [email.email_to +':'+ email.subject for email in emails]
