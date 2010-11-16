<%
if c.scripts_end is None:
	c.scripts_end = ["<!-- scripts_end not specified -->", ]
if not config['development_mode']:
	c.scripts_end.append("""
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
${"\n".join(c.scripts_end)|n}
