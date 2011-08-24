<%namespace name="share" file="/frag/common/share.mako"     />

<%def name="body()">
	${refresh_fragment_height()}

	% if config['online']:
		${google_analytics_end()}
		${share.init_janrain_social()}
		##${share.share_this_js()}
	% endif

	## Maps (should be loaded on-demand, but frags confuse that
	% if config['development_mode']:
		## AllanC - Please note the order of these JS files should match the order in /public/javascript/Makefile to reduce potential errors with loading dependencys between the live and development sites
		<!-- non-urgent bits -->
		<script src="/javascript/jquery.ui.js"></script>
		<script src="/javascript/jquery.ui.stars-3.0.1.js"></script>
		<script src="/javascript/jquery.ui.timepicker-addon.js"></script>
		<script src="/javascript/jquery.html5-0.0.1.js"></script>
		<script src="/javascript/jquery.scrollTo.js"></script>
		<script src="/javascript/jquery.simplemodal-1.4.1.js"></script> <!-- http://www.ericmmartin.com/projects/simplemodal/ -->
		<script src="/javascript/jquery.uploadify.v2.1.4.js"></script>
		<script src="/javascript/jquery.simple-color-picker.js"></script>
		<script src="/javascript/jquery.ba-hashchange.min.js"></script>
		<script src="/javascript/jquery.limit-1.2.js"></script>
		<script src="/javascript/jquery.getUrlParam.js"></script>
		<script src="/javascript/jquery.cookie.js"></script>
		<script src="/javascript/jquery.jcarousel.js"></script>
		<script src="/javascript/invite.js"></script>
		<script src="/javascript/mobile.js"></script>
		<script src="/javascript/rpx.js"></script>
		<script src="/javascript/misc.foot.js"></script>
		<!-- maps -->
		<script src="/javascript/gears_init.js"></script>
		<script src="/javascript/geo.js"></script>
		<script src="/javascript/OpenLayers.js"></script>
		<script src="/javascript/minimap.js"></script>
	% else:
		<script async src="${h.wh_url("public", "javascript/_combined.foot.js")}"></script>
	% endif

	## tinymce, should also be loaded on demand
	<script async src="/javascript/tiny_mce/tiny_mce.js"></script>
</%def>


##----------------------------------------------------------------------------
## Google Analitics
##----------------------------------------------------------------------------
<%def name="google_analytics_head()">
    ## --Google Analitics - ASync array setup ----------------------------------
    ## http://code.google.com/apis/analytics/docs/tracking/asyncUsageGuide.html#SplitSnippet
    ## As this is just an array there is no harm in declaring it here
	<!-- Google Analytics -->
	<script type="text/javascript">
		var _gaq = _gaq || [];
		_gaq.push(['_setAccount', '${config['api_key.google.analytics']}']);
		_gaq.push(['_trackPageview']);
	</script>
</%def>

<%def name="google_analytics_end()">
    ## civicboom@googlemail.com - https://www.google.com/analytics/settings/home?scid=19962566
    ##
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
</%def>


##----------------------------------------------------------------------------
## Dynamic Fragment Height
##----------------------------------------------------------------------------
<%def name="refresh_fragment_height()">
## this only works properly if it is the first of the footer scripts and
## included in the HTML -- if it is in the header bundle or footer bundle,
## or if it is in the footer but after the external scripts, then there
## is a flash of wrong-heighted content
<script>
function refresh_fragment_height() {
	var height = $('footer').offset().top - $('#app').offset().top;
	//Y.log(height);
	createCSS(".frag_data", "height: "+(height-40)+"px !important;");
}
refresh_fragment_height();
$(window).resize(refresh_fragment_height);
</script>
</%def>
