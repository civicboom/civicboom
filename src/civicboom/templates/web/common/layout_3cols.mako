<%inherit file="html_base.mako"/>

## Template for 3 Column Layout
## -The middle col is elastic, left and right cols are fixed width
## -The style information here is to keep the "width" information for the columns in one place
## -look at the YUI documentation for template type widths http://developer.yahoo.com/yui/grids/

<%def name="body()">
<!-- 3 Column Layout -->

<!-- Column Left -->
<div id="col_left" class="yui-b">
  <div class="page_bordered_section">
    ${next.col_left()}
  </div>
</div>
<!-- End Column Left -->

<div id="yui-main">
  ## YUI requires the YUI-MAIN div to have a YUI-BLOCK within it so it is positioned against the left col correctly
  ## It feels confusing, but thats the way YUI and CSS work. (at leist in the mako templates you just have def's for left,right, center to abstract you from it)
  <div class="yui-b">
    <!-- Column Right (unfortunately needs to come before center col in document flow to be aligned at the top)-->
    <div id="col_right">
      <div class="page_bordered_section">
        ${next.col_right()}
      </div>
    </div>
    <!-- End Column Right -->
    
    <!-- Column Center (Elastic) -->
    <div id="main">
      ## AllanC this is given a new div because main encompases the right col margin as well because the right col is floated
      ##   this new div gives individual control over the center col border
      <div id="col_center">
        ${next.body()}
      </div>
    </div>
    <!-- End Column Center -->
  </div>
</div>
<!-- End 3 Col Layout -->
</%def>

## yui-t1 width=160px left
## yui-t2 width=180px left
## yui-t2 width=300px left
## yui-t2x width=240px left (custom addition)
<%def name="yuiTemplateType()">yui-t1</%def>
<%def name="rightColWidth()"  >260</%def>

## Set the right col to match the yui-t2 width
<%def name="styleOverides()">
  ##${parent.styleOverrides()}
  #col_right {
    float: right;
    width: ${self.rightColWidth()}px;
  }
  #main {
    margin-right: ${self.rightColWidth()}px;
  }
</%def>