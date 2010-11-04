<%doc>
<!-- redirect javascript function -->
<script type="text/javascript">
function redirect_function() {
  redirect_url = "${h.url(controller='account',action='signin', redirect=c.current_path)}"
  window.location = redirect_url;
  return false;
}
</script>
</%doc>

<script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#username=xa-4b7acd5429c82acd"></script>

% if not config['development_mode']:
<!-- Civicboom Analytics -->
<script type="text/javascript">
  var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
  document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
  try {
    var pageTracker = _gat._getTracker("UA-12427902-1");
    pageTracker._trackPageview();
  } catch(err) {}
</script>
% endif
