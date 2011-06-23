<%inherit file="/html/widget/widget_base.mako"/>
<%
    font_size  = 19
%>
<style>

.widget_border {
    font-size: ${font_size}px;
    ##color    : #${c.widget['color_font']};
    width : ${c.widget['width' ]-2}px;
    height: ${c.widget['height']-2}px;
    
    border: 0.1em solid #c4cdd2;
    ##${c.widget['color_border']};


}
    
    
</style>
<div class="widget_border">
    <div class="padding">
    ##----------------------------------------
    ## Header
    ##----------------------------------------
    <div class="widget_header">
        <div class="padding">
        See the latest requests
        <a href="${h.url(controller='misc', action='titlepage', sub_domain='www')}" target="_blank"><img class="logo" src="/images/logo_com.png" /></a>
        </div>
    </div>
    
    ##----------------------------------------
    ## Body
    ##----------------------------------------
    <div class="widget_content">
        <div class="padding">
        ${next.body()}
        </div>
    </div>
    
    ##----------------------------------------
    ## Footer
    ##----------------------------------------
    <div class="widget_footer">
    </div>
    
    </div>
</div>