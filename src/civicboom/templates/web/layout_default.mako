<%inherit file="/layout_2cols.mako"/>

##------------------------------------------------------------------------------
## YUI: Template Layout Type
##------------------------------------------------------------------------------
<%def name="yuiTemplateType()">yui-t6</%def>
##<%def name="rightColWidth()"  >180</%def>

##------------------------------------------------------------------------------
## Side Col
##------------------------------------------------------------------------------
<%def name="col_side()">
  ##<%include file="/includes/link_newsmap.mako"/>
  ##<%include file="/includes/link_makethenews.mako"/>
  ##<%include file="/includes/leftcol_ad_250px.mako"/>
	##<%include file="/includes/rightcol_ad_160px.mako"/>
  <%include file="/design09/includes/assignments_sidebar.mako"/>
</%def>

<%def name="col_right()">
</%def>

##------------------------------------------------------------------------------
## Center Body
##------------------------------------------------------------------------------

${next.body()}