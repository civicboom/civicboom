<%def name="by_member(member, link=True)">
    % if link:
    <a href="${h.url('member', id=member['username'], sub_domain='www')}" target="_blank">
    % endif
        ${member['name']}
        <img src="${member['avatar_url']}" style="max-height:1em;" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
    % if link:
    </a>
    % endif
</%def>

