<%inherit file="/web/html_base.mako"/>

<div>
  <h1>Content Unavalable</h1>
  % if c.error_message:
  <p>${c.error_message}</p>
  % endif
</div>
