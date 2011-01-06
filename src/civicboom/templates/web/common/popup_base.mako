<%def name="body()">
##popup(id, title, content)
</%def>
<%def name="popup(id, title, content)">
    ## ${popup.popup('flag_content', _('Flag content'), flag_form)}
    ## involke with <a href='' onclick="$('#flag_content').modal(); return false;">
    <div id="${id}" class="hideable">
        <div class="title_bar gradient">
            <div class="title">
                <span class="icon icon_popup"></span><span class="title_text">${title}</span>
            </div>
            <div class="common_actions">
                <a href='' title='${_('Close popup')}' class="icon icon_close simplemodalClose"><span>Close</span></a>
            </div>
        </div>
        
        <div class="popup_content">
        % if next:
            ${next.body()}
        % endif
        <% import types %>
        % if isinstance(content, types.FunctionType):
            ${content()}
        % else:
            ${content}
        % endif
        </div>

    </div>
</%def>
