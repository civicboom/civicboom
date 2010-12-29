<%!
    title               = 'List'
    icon_type           = 'list'
    
    share_url           = ''
    share_title         = ''
    share_description   = ''
    
    frag_data_css_class = ''
%>

<%namespace name="share" file="/frag/common/share.mako"/>

<%def name="body()">

    % if hasattr(next, 'init_vars'):
    ${next.init_vars()}
    % endif

    ## AJAX Fragment refresh (not visable to user)
    <a class="frag_source" href="${h.current_url()}" style="display: none;">frag source</a>
    ##url.current(format='frag')
    
    <div class="title_bar">
        <div class="title">
            ## Title
            <span class="icon icon_${self.attr.icon_type}"></span><span class="title_text">${self.attr.title}</span>
        </div>

        <div class="common_actions">
            ## Reload
            % if c.format=='frag' and config['development_mode']:
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
            % if c.format=='frag':
                <%
                    args, kwargs = c.web_params_to_kwargs
                    rss_kwargs = dict(kwargs)
                    rss_kwargs['format'] = 'rss'
                %>
                <a href='${url.current(**rss_kwargs)}' title='RSS' class="icon icon_rss"><span>RSS</span></a>
            % endif
            
            ## Close
            <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon icon_close"><span>${_('Close')}</span></a>
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
        </div>        
    </div>
    
    <div class="frag_data ${self.attr.frag_data_css_class}">
        ${next.body()}
    </div>
</%def>