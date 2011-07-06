<%inherit file="/html/widget/widget_base.mako"/>

<style>
    .widget_border {
        width : ${c.widget['width' ]-2}px;
        height: ${c.widget['height']-2}px;
    }
</style>

<div class="widget_border">
    <div class="padding">
    ##----------------------------------------
    ## Header
    ##----------------------------------------
    <div class="widget_header">
        
        <% owner = c.widget['owner'] %>
        % if owner and owner.get('push_assignment'):
        <div class="action">
            <a href="${h.url('new_content', target_type='article', parent_id=owner['push_assignment'], sub_domain="www")}">${_("Send us your stories")}</a>
        </div>
        % endif
        
        <div class="title">
            <div class="padding">
            Latest requests
            <a href="${h.url(controller='misc', action='titlepage', sub_domain='www')}" target="_blank"><img class="logo" src="/images/logo_com.png" /></a>
            </div>
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