<%!
    title               = 'List'
    icon_type           = 'list'
    
    share_kwargs        = None
    
    frag_url            = True
    html_url            = True
    rss_url             = True
    auto_georss_link    = False
    
    frag_data_css_class = ''
%>



<%namespace name="share" file="/frag/common/share.mako"/>

<%def name="body()">

    <%
        # Default creation of URLS - these can be overridden by init_vars()
        import copy
        if c.web_params_to_kwargs:
            args, kwargs = c.web_params_to_kwargs
            args   = copy.copy(args)
            kwargs = copy.copy(kwargs)
        else:
            args   = []
            kwargs = {}
        
        # Gen frag URL
        if self.attr.frag_url == True:
            kwargs['format'] = 'frag'
            self.attr.frag_url = url.current(**kwargs)
        
        # Gen html URL
        if self.attr.html_url == True:
            if 'format' in kwargs:
                del kwargs['format']
            self.attr.html_url = url.current(host=app_globals.site_host, **kwargs)
        
        # Gen RSS URL
        if self.attr.rss_url == True:
            kwargs['format'] = 'rss'
            self.attr.rss_url = url.current(**kwargs)
    %>

    % if hasattr(next, 'init_vars'):
    ${next.init_vars()}
    % endif

    ## AJAX Fragment refresh (not visible to user)

    <a class="frag_source" href="${self.attr.frag_url}" style="display: none;">frag source</a>
    ##.current_url()##
    
    <div class="title_bar gradient">
        <div class="title">
            ## Title
            <span class="icon icon_${self.attr.icon_type}"></span><span class="title_text">${self.attr.title}</span>
        </div>

        <div class="common_actions">
            ## Reload
            % if config['development_mode']:
                ##c.format=='frag' and 
                <a href='' class="icon icon_reload" onclick='cb_frag_reload($(this)); return false;' title='Reload Fragment'><span>Reload Fragment</span></a>
            % endif
            
            ## Share
            % if self.attr.share_kwargs:
                ${share.share(**self.attr.share_kwargs)}
            % endif
            
            ## RSS
            % if self.attr.rss_url:
                <a href='${self.attr.rss_url}' title='RSS' class="icon icon_rss"><span>RSS</span></a>
            % endif
            
            ## Close
            % if c.format=='frag':
                <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon icon_close"><span>${_('Close')}</span></a>
            % else:
                <span class="icon"></span>
            % endif
        </div>
    </div>
    
    <div class="action_bar">
        <div class="object_actions_specific">
            % if hasattr(next, 'actions_specific'):
            ${next.actions_specific()}
            % endif
        </div>
        
        <div class="object_actions_common">
            % if hasattr(next, 'actions_common'):
            ${next.actions_common()}
            % endif

            ##% if self.attr.auto_georss_link:
            ##    ${georss_link()}
            ##% endif
        </div>        
    </div>
    
    <div class="frag_data ${self.attr.frag_data_css_class}">
        ${next.body()}
    </div>
</%def>

<%def name="georss_link(georss_url=None)">
    <%
        import copy
        
        feed = url.current(
            format         ='rss' ,
            query          =request.params.get('query') ,
            location       =request.params.get('location') ,
            include_fields = 'attachments' ,
        )
        
        georss_url = dict(
            controller = 'misc',
            action     = 'georss',
            location   = request.params.get('location'),
            feed       = feed
        )
        georss_url_frag = copy.copy(georss_url)
        georss_url_frag['format'] = 'frag'
        
        georss_url      = url(**georss_url)
        georss_url_frag = url(**georss_url_frag)
    %>
    <a href="${georss_url}" title="${_('View on map')}" class="icon icon_map" onclick="cb_frag($(this), '${georss_url_frag}'); return false;"><span>${_('View on map')}</span></a>
</%def>
