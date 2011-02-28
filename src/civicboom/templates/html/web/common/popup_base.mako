<%! import types %>

<%def name="body()">
    ## See companion JS misc.js:popup to populate this div
    ${popup_static(_('Dialog'), "", "popup", display_none=True)}
</%def>

<%def name="popup_static(title, content, html_id, display_none=False)">
    ## ${popup.popup('flag_content', _('Flag content'), flag_form)}
    ## involke with <a href='' onclick="$('#flag_content').modal(); return false;">
    <div id="${html_id}" class="hideable"
        % if display_none:
        style="display:none;"
        % endif
    >
        <div class="title_bar">
            <div class="title">
                <span class="icon16 popup"></span><span class="title_text">${title}</span>
            </div>
            <div class="common_actions">
                <a href='' title='${_('Close popup')}' class="icon16 close simplemodalClose"><span>Close</span></a>
            </div>
        </div>
        
        <div class="popup_content">
        % if next:
            ${next.body()}
        % endif
        % if isinstance(content, types.FunctionType):
            ${content()}
        % else:
            ${content}
        % endif
        </div>

        <div style="clear: both;">&nbsp;</div>
    </div>
</%def>

<%def name="popup_frag(title, url_frag)">
    <script type="text/javascript">
        ## wrapping th call in this function will be called when page is ready
        $(function() {
            popup('${title}','${url_frag}');
        });
    </script>
</%def>


<%def name="link(url, title='Dialog', text=None, class_='')">
    <%
        if title and text==None:
            text = h.literal("<span>%s</span>" % title)
        url_frag = None
        if isinstance(url, tuple):
            url, url_frag = h.url_pair(gen_format='frag', *url[0], **url[1])
    %>
    <a href="${url}" class="${class_}" title="${title}"
       % if url_frag:
       onclick="popup('${title}','${url_frag}'); return false;"
       % endif
    >
        ${text}
    </a>
</%def>
