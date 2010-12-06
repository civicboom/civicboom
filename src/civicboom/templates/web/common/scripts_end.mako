<%
if c.scripts_end is None:
	c.scripts_end = ["<!-- scripts_end not specified -->", ]
if (not config['development_mode']) and config['online']:
## civicboom@googlemail.com - https://www.google.com/analytics/settings/home?scid=19962566
	c.scripts_end.append("""
<!-- Civicboom Analytics -->
<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-19962566-1']);
  _gaq.push(['_trackPageview']);
  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
	""")
%>
${"\n".join(c.scripts_end)|n}

<%doc>
    OLD ANALITICS - unknown login?
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
</%doc>