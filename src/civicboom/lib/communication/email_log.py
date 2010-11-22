"""
Python log of emails that have been sent
Used by unit tests to check email output
"""

import logging
log = logging.getLogger(__name__)

emails = []

class Email:
    def __init__(self, email_to, subject, content_text, content_html):
        self.email_to     = email_to
        self.subject      = subject
        self.content_text = content_text
        self.content_html = content_html

def email_log(email_to, subject, content_text, content_html):
    log.info("--Email Send Disabled-- \n"
              "To: %s Subject: %s" % (email_to, subject) +"\n"
              "Message (content_text): %s" % content_text +"\n"
            #+ "Message (content_html): %s" % content_html +"\n"
              "\n")
    
    # AllanC: TODO in the future, we may have servers that have email aggregation disabled
    #         it is VERY important that any emails dont get logged in memory and swell to a crazzy size after days or hours of use
    
    emails.append(Email(email_to, subject, content_text, content_html))
    
def getNumEmails():
    return len(emails)

def getLastEmail():
    return emails[-1]