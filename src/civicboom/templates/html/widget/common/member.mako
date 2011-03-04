<%def name="by_member(member, link=True)">
    % if link:
    <a href="${h.url('member', id=member['username'], subdomain='')}" target="_blank">
    % endif
        ${member['name'] or member['username']}
        <img src="${member['avatar_url']}" style="max-height:1em;" onerror='this.onerror=null;this.src="/images/default/avatar.png"'/>
    % if link:
    </a>
    % endif
</%def>

