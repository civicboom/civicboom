## -*- coding: utf-8 -*-
<%!
    import textile
    import re
%>
<html>
    <head>
        <title>Civicboom: Future Features</title>
        
        <link rel="stylesheet" href="http://yui.yahooapis.com/3.3.0/build/cssreset/reset.css"       type="text/css">
        <link rel="stylesheet" href="http://yui.yahooapis.com/3.3.0/build/cssfonts/fonts.css"       type="text/css">
        <link rel="stylesheet" href="http://yui.yahooapis.com/3.3.0/build/cssbase/base-context.css" type="text/css">
        
        <style type="text/css">
            BODY {
                padding: 1em;
            }
            H1 {
                font-size: xx-large;
                font-weight: bold;
                margin-top: 0.5em;
                margin-bottom: 0.5em;
            }
            H2 {
                font-size: large;
                font-weight: bold;
            }
            TABLE {
                
            }
            TD, TH {
                border: 0.1em solid black;
                vertical-align: top;
                padding: 0.5em;
            }
            TH {
                font-weight: bold;
            }
            LI {
                margin-left: 2em;
                list-style: disc;
            }
            LI LI {
                margin-left: 2em;
                list-style: circle;
            }
        </style>
    </head>
    
    <body>
        <h1>Civicboom: Future Features</h1>
        
        <table>
            <tr>
                <th>Feature</th>
                <th>Description</th>
                <th>Benefit/Revolution</th>
                <th>Time and Resorces</th>
                <% num_cols = 4 %>
            </tr>
        % for item in redmine_data:
            <tr>
                <td>
                    ${item['subject']}
                    
                ## Check number of times <h?> occours
                ## AllanC - Enhancement: Maybe we should be specifically looking for H2's so we can have lower level headings in the sections?
                <%
                    html = textile.textile(item['description'])
                    num_headings = html.count('<h') or 1
                %>
                % if num_headings > 1:
                    ## Put each h2 in an individual cell
                    ${re.sub(r'<h\d>(.*?)</h\d>', '<td>', html) |n}
                    ## Fill in any empty trailing cells
                    % for i in range(num_cols-num_headings-1):
                        <td></td>
                    % endfor
                % else:
                    ## No headings to split by, put all data in one epic cell
                    <td colspan="${num_cols-num_headings}">${html |n}</td>
                % endif
            </tr>
        % endfor
        </table>
        
    </body>
    
</html>