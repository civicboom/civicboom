<%inherit file="/web/common/html_base.mako"/>

<div>
  <h1>${_("Content Unavalable")}</h1>
  % if c.error_message:
  <p>${c.error_message}</p>
  % endif
</div>
