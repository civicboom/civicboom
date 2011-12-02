<%namespace name="share" file="/frag/common/share.mako"     />
<%!
  from pylons import request
%>

<%def name="body()">
	% if config['online']:
		${google_analytics_end()}
		${share.init_janrain_social()}
		##${share.share_this_js()}
	% endif

  <script src="${h.wh_url("public", "javascript/tiny_mce/tiny_mce.js")}"></script>
	% if config['development_mode'] and 'MSIE' not in request.environ.get('HTTP_USER_AGENT', ''):
        <div id="this is just here to make reading the source tree easier in dev mode">
            <%
            from glob import glob
            scripts_head = glob("civicboom/public/javascript/foot/*.js")
            scripts_head = [n[len("civicboom/public/"):] for n in scripts_head]
            scripts_head.sort()
            %>
            % for script in scripts_head:
                <script src="/${script}"></script>
            % endfor
        </div>
  % elif config['development_mode']:
    <script src="${h.wh_url("public", "javascript/_combined.foot.js")}"></script>
  % else:
		<script src="${h.wh_url("public", "javascript/_combined.foot.min.js")}"></script>
	% endif

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
