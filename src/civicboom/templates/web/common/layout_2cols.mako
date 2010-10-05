<%inherit file="html_base.mako"/>

<!-- 2 Column Layout -->

<!-- Left Column -->
<div id="col_left">
	${self.col_side()}
</div>
<!-- End Left Column -->

<!-- Column Center (Elastic) -->
<div id="col_main">
	${next.body()}
</div>
<!-- End Column Center -->

<!-- End 2 Col Layout -->

<%def name="col_side()"></%def>
