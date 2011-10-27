% if 'conversation_with' in d['list']['kwargs']:
    <%include file="conversation.mako"/>
% else:
    <%include file="index_.mako"/>
%endif
