<%!
    title               = 'List'
    icon_type           = 'list'
    
    share_url           = ''
    share_title         = ''
    share_description   = ''
    
    rss_url             = True
    
    frag_data_css_class = ''
    auto_georss_link    = False
%>



<%namespace name="share" file="/frag/common/share.mako"/>

<%def name="body()">

    <%
        import copy
        args, kwargs = c.web_params_to_kwargs
    %>

    % if hasattr(next, 'init_vars'):
    ${next.init_vars()}
    % endif

    ## AJAX Fragment refresh (not visable to user)
    <%
        kwargs_frag = copy.copy(kwargs)
        kwargs_frag['format'] = 'frag'
    %>
    <a class="frag_source" href="${h.url.current(**kwargs_frag)}" style="display: none;">frag source</a>
    ##.current_url()##
    
    <div class="title_bar">
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
            % if self.attr.share_url:
                ${share.share(
                    url         = self.attr.share_url ,
                    title       = self.attr.share_title ,
                    description = self.attr.share_description ,
                )}
            % endif
            
            ## RSS
            % if self.attr.rss_url:
                ##c.format=='frag' and 
                <%
                    rss_kwargs = copy.copy(kwargs)
                    rss_kwargs['format'] = 'rss'
                %>
                <a href='${url.current(**rss_kwargs)}' title='RSS' class="icon icon_rss"><span>RSS</span></a>
            % endif
            
            ## Close
            % if c.format=='frag':
                <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon icon_close"><span>${_('Close')}</span></a>
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

            % if self.attr.auto_georss_link:
                ${georss_link()}
            % endif
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