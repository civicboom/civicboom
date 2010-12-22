<%inherit file="/web/common/html_base.mako"/>

<%def name="body()">
    <div id='frag_containers'>
		## AllanC - Methods 1 and 2 have the same outcome
		
		## Method 1: Use SSI to get the fragment
		##<% frag_url = url('content', id=1, format='frag') %>
		##${h.frag_div("frag_", frag_url, class_="frag_container")}
		
		## Method 2: Create the div manually and render from the template
		<div id="frag_" class="frag_container">
			${next.body()}
		</div>
		
		## Disscussion
		## Method 1 relys on a second call to the server, most of the time this will be cached, but it is still a second call
		## Method 2 The query and formatting to a dictionary have already happened and are avalable, so we can just give them to the template
		
		## Development notes (marked for removal)
		##<div id="frag_1" class="frag_container" style="border: 1px dashed red;">
			##<p>hello all</p>
			##<a href="${url("content", id=1, format='frag')}" onclick="cb_frag($(this)); return false;">Link of AJAX</a>
		##</div>

    </div>

    <%
	c.scripts_end.append("""
		<script type="text/javascript">
			function refresh_fragment_height() {
				var height = $('footer').offset().top - $('#app').offset().top;
				//Y.log(height);
				createCSS(".frag_data", "height: "+(height-70)+"px !important;");
			}
			refresh_fragment_height();
			$(window).resize(refresh_fragment_height);
		</script>
    """)
	%>
</%def>
