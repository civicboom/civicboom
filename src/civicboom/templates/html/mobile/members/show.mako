<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />

## init
<%def name="init_vars()">
    <%
        self.member    = d['member']
        self.id        = self.member['username']
        self.name      = self.member.get('name')
    %>
</%def>

## page structure defs
<%def name="body()">
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-details-${self.id}" class="member_details_page">
        ${header()}
    </div>
    
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-extra-${self.id}" class="member_extra_page">
        ${header("extra")}
    </div>
</%def>

<%def name="page_title()">
    ${_("_site_name Mobile - " + self.member)}
</%def>

<%def name="header(heading=False, right_btn=False)">
    <div data-role="header" data-position="inline">
        <h1>
            ${self.member}
            % if heading:
                " - ${heading}"
            % endif
        </h1>
    </div>
</%def>