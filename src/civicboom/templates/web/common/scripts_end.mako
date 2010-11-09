<%
if not "scripts_end" in locals():
	scripts_end = []
if not config['development_mode']:
	scripts_end.append("""
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
	""")
%>
${"\n".join(scripts_end)|n}
