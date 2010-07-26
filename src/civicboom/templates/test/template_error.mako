<%inherit file="/web/html_base.mako"/>

<%def name="body()">
    Mako Error throwing test
    ##${h.raise_exception_test()}
    
    % for license in app_globals.licenses:
    % endfor
</%def>
