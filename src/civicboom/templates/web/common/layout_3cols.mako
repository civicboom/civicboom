<%inherit file="html_base.mako"/>

<!-- 3 Column Layout -->

<!-- Column Left -->
<div id="col_left">
    ${next.col_left()}
</div>
<!-- End Column Left -->

<!-- Column Right (unfortunately needs to come before center col in document flow to be aligned at the top)-->
<div id="col_right">
${next.col_right()}
</div>
<!-- End Column Right -->

<!-- Column Center (Elastic) -->
<div id="col_main">
${next.body()}
</div>
<!-- End Column Center -->

<!-- End 3 Col Layout -->
