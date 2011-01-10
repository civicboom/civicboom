## civicboom@googlemail.com - https://www.google.com/analytics/settings/home?scid=19962566
##
## This code has been split with the header - see html_base.mako and the reference below
## http://code.google.com/apis/analytics/docs/tracking/asyncUsageGuide.html#SplitSnippet
% if (not config['development_mode']) and config['online']:
	<!-- Google Analytics -->
	<script type="text/javascript">
	  (function() {
		var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
		ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
		var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	  })();
	</script>
% endif

<script type="text/javascript">
	function refresh_fragment_height() {
		var height = $('footer').offset().top - $('#app').offset().top;
		//Y.log(height);
		createCSS(".frag_data", "height: "+(height-58)+"px !important;");
	}
	refresh_fragment_height();
	$(window).resize(refresh_fragment_height);
</script>

## Maps (should be loaded on-demand, but frags confuse that
% if config['development_mode']:
	<script src="/javascript/gears_init.js"></script>
	<script src="/javascript/geo.js"></script>
	<script src="/javascript/OpenLayers.js"></script>
	<script src="/javascript/minimap.js"></script>
    <script src="/javascript/tiny_mce/tiny_mce.js"></script>
% else:
	<script src="/javascript/_combined.maps.js"></script>
% endif
