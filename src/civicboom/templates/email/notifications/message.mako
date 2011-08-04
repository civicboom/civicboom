<%inherit file="default.mako"/>

## AllanC - ***ING mako wont render without a body, it complains about undefined c. .. wtf!
<%def name="body()"></%def>

<%def name="content()">
    <p>
    <% source = kwargs.get('source') %>
    % try:
        ${h.HTML.a(unicode(source), href=source.__link__())} 
    % except:
        ${source}
    % endtry
    ${_('sent you a message')}
    </p>
    
    <p>${          kwargs.get('subject') }</p>
    <p>${h.literal(kwargs.get('content'))}</p>
    <p><a href="${h.url('message', id=kwargs.get('id'), qualified=True)}">${_('Click here to reply!')}</a></p>
</%def>