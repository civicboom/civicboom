<%def name="by_member(member, link=True)">
    % if link:
    <a href="${h.url('member', id=member['username'], subdomain='')}" target="_blank">
    % endif
        By
        <img src="${member['avatar_url']}" style="max-height:1em;" onerror='this.onerror=null;this.src="/images/default/avatar.png"'/>
        ${member['name'] or member['username']}
    % if link:
    </a>
    % endif
</%def>

