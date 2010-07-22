from pylons import session

from webhelpers.html import literal


def flash_message(message):
    if 'flash_message' in session:
        session['flash_message'] = session['flash_message'] + literal("<br/>") + message
    else:
        session['flash_message'] = message
    session.save()
