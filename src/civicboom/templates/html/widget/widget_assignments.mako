<%inherit file="./widget_border.mako"/>

##<%namespace name="widget_assignment_includes"   file="widget_assignment.mako"/>
<% assignments = c.result['data']['list']['items'] %>

% if len(assignments) == 0:
    % if c.widget_owner == c.logged_in_persona:
        <p style="margin: 0.5em;">
            ${_("Set an _assignment to have it appear here on your widget")}
        </p>
    % else:
        <p style="margin: 0.5em; font-size: 200%;">
            ${_("Watch this space!")}
        </p>
    % endif

## Else we have a list of assignments to show
% else:
    <div class="widget_content_assignment_list">
        <ul>
            ${widget_assignments(assignments)}
        </ul>
    </div>
% endif

<%def name="widget_assignments(assignments)">
    % for assignment in assignments:
        ${widget_assignment(assignment)}
    % endfor
</%def>

<%def name="widget_assignment(assignment)">
    <li>
        <div class="test">
        <a href="${h.url_from_widget(controller='widget',action='assignment',id=assignment['id'])}">
            <img src="${assignment['thumbnail_url']}"/>
            <span>${assignment['title']}</span>
            <div class="clearboth_hack"></div>
            ##&#8220; &#8221;
            ##<div class="popup_content widget_content">
            ##  ${widget_assignment_includes.widget_assignment(assignment)}
            ##</div><!--end popup-->
        </a>
        </div>
      </li>
</%def>