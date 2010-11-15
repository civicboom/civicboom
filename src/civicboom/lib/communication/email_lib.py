from pylons             import tmpl_context as c, config
from pylons.templating  import render_mako as render
from pylons.i18n.translation import _

from webhelpers.html.tools import auto_link
from webhelpers.html       import literal

from civicboom.lib.text import convert_html_to_plain_text

import re

import logging
log = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Send Email
#-------------------------------------------------------------------------------

def send_email(email_to, subject='', content_text=None, content_html=None):
    """
    Prepares and Send's an automated email generated by the system
    Prepares and converts between plain text and HTML content
    If email is disabled in the config it is sent to the logger
    """
    
    # User object passed, get email address
    #  else the email_to is assumed to be a CSV list of email address's
    if hasattr(email_to, 'email_unverifyed') and email_to.email_unverifyed!=None: email_to = email_to.email_unverifyed
    if hasattr(email_to, 'email'           ) and email_to.email           !=None: email_to = email_to.email
    email_to = str(email_to)
    
    # Check paramiters for validity and throw exception if needed
    if content_text==None and content_html==None:
      raise EmailContentError('email content for plain text or HTML not specifyed')
  
    # Convert plain text into html by:
    #   -autolinking any links
    #   -putting inside html header
    if content_text!=None and content_html==None:
        content_text_copy = content_text
        content_html      = auto_link(content_text_copy.replace('\n','<br/>').decode('UTF-8'))
    # Convert html emails into a plain text equivlent
    elif content_html!=None and content_text==None:
        content_text      = convert_html_to_plain_text(content_html)
  
    # If not already wrapped in HTML header
    if not re.search(r'<body.*</body>',content_html, re.DOTALL + re.IGNORECASE): #If content HTML is not a complete document with a head and body - put it in the standard email template
        c.email_content = literal(content_html)
        content_html = render('/email/base_email_from_plaintext.mako')
  
    # Subject - append site name to subject
    if subject==None or subject=='': subject = _("_site_name")
    else                           : subject = _("_site_name")+': '+subject  
  
    # Log Debug data if send disabled
    if config['feature.aggregate.email'] is False: send_email_log (email_to, subject, content_text, content_html)
    else                                         : send_email_smtp(email_to, subject, content_text, content_html)

#-------------------------------------------------------------------------------

def send_email_log(email_to, subject, content_text, content_html):
    log.info("--Email Send Disabled-- \n"
              "To: %s Subject: %s" % (email_to, subject) +"\n"
              "Message (content_text): %s" % content_text +"\n"
            #+ "Message (content_html): %s" % content_html +"\n"
              "\n")


#-------------------------------------------------------------------------------
# Send Email - SMTP
#-------------------------------------------------------------------------------
def send_email_smtp(email_to, subject, content_text, content_html, sender=None):
    """
    Takes a comma separated list (email_to) with a subject and message body
    and sends it out to all the recipients
    No modification is made to any content
    """
    from email.mime.multipart import MIMEMultipart
    from email.mime.text      import MIMEText
    from email.mime.image     import MIMEImage
    import smtplib

    if not sender:
        sender = config['email.autogen_from']
    
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From']    = sender
    msgRoot['To']      = email_to
    msgRoot.preamble   = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    
    #content_text - encoded correctly
    try                : content_text = content_text.encode('UTF-8')
    except UnicodeError: pass
    msgText = MIMEText(content_text, 'plain', 'UTF-8')
    msgAlternative.attach(msgText)
    
    #content_html - encoded correctly
    try                : content_html = content_html.encode('UTF-8')
    except UnicodeError: pass
    msgText = MIMEText(content_html, 'html', 'UTF-8')
    msgAlternative.attach(msgText)
    
    # Send the email
    try:
        smtp = smtplib.SMTP()
        smtp.connect(config['email.smtp_server'], int(config['email.smtp_port'])) #Use the smtp server from the configuration file
        smtp.ehlo()
        #sending locally so we don't need the below
        smtp.starttls()
        #need to rerun ehlo, as the smtplib on the server doesnt' do it again automatically
        smtp.ehlo()
        smtp.login(config['email.smtp_username'], config['email.smtp_password'])
        # Assuming the list is comma separated, send the message to each recipient.
        
        for recipient in email_to.split(','):
            smtp.sendmail(sender, recipient, msgRoot.as_string())
        smtp.quit()

    except smtplib.SMTPException as e:
        log.error('Unable to send email: %s' % e)
    except smtplib.socket.error as e:
        log.error('Mail server not available/misconfigured: %s' % e)

