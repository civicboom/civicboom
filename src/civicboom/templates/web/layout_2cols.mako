<%inherit file="html_base.mako"/>

## Template for 2 Column Layout
## -The middle col is elastic, left col is fixed width
## -The style information here is to keep the "width" information for the columns in one place
## -look at the YUI documentation for template type widths http://developer.yahoo.com/yui/grids/

## Default col template - see YUI grids for template types -
## this can be overriden to put the col on the left or the right
##yui-t2 width=180px
<%def name="yuiTemplateType()">yui-t3</%def>

<%def name="body()">
<!-- 2 Column Layout -->


<!-- Column Side -->
<div id="col_side" class="yui-b">
  <div class="page_bordered_section">
    ${self.col_side()}
  </div>
</div>
<!-- End Column Left -->

<div id="yui-main">
  <div class="yui-b">    
    <!-- Column Center (Elastic) -->
    <div id="main">
       ${next.body()}
    </div>
    <!-- End Column Center -->
  </div>
</div>

<!-- End 2 Col Layout -->
</%def>

## Null declaration so inheriters are not forced to have a side col populated
<%def name="col_side()">
</%def>