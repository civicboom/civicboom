<%def name="css(css_files)">
    <%doc>
        Iterate though the css filenames given and print the files contents.
        This is used because IE is retarded and wont allow more than 31 files .. even using @include
    </%doc>
    % for css in css_files:
        ## AllanC - path joining safe here because we are in development mode
        <% file = open("civicboom/public/" + css, 'r') %>
        % for line in file:
${line}\
        % endfor
        <% file.close() %>
    % endfor
</%def>

<%def name="body()">${css(h.css_files())}</%def>