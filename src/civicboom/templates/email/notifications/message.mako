<%inherit file="default.mako"/>

## AllanC - ***ING mako wont render without a body, it complains about undefined c. .. wtf!
<%def name="body()"></%def>

<%def name="content()">
    <p>${kwargs.get('source')} sent you a message</p>
    <p>${kwargs.get('subject')}</p>
    <p>${kwargs.get('content')}</p>
</%def>