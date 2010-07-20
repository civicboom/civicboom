<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Hide Navigation if not logged in
##------------------------------------------------------------------------------
<%def name="navigation()">
  % if c.logged_in_user:
    ${parent.navigation()}
  % endif
</%def>

##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
<%def name="styleOverides()">
  #bd {padding: 0em;}
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<div class="misc_page background_gradient_dark">
  ##% if c.http_referer:
  ##<div class="link_float"><a href="${c.http_referer}">${_("Back")}</a></div>
  ##% endif
  ${next.body()}
</div>
