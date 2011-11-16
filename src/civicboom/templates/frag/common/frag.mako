<%!
    import types
    import copy
    from webhelpers.html import HTML, literal

    title               = 'List'
    icon_type           = 'list'
    
    share_kwargs        = None
    
    frag_url            = True
    html_url            = True
    rss_url             = False
    ##auto_georss_link    = False
    
    help_frag           = None # This can be set to a string name to activate '/misc/help/HELP_FRAG' to render '/frag/help/HELP_FRAG.mako'
    
    frag_data_css_class = ''
    
    popup_url   = None  # Frags can set this if they want a loaded popup to show
%>



<%namespace name="share" file="/frag/common/share.mako"/>
<%namespace name="popup" file="/html/web/common/popup_base.mako"/>

##------------------------------------------------------------------------------
## Frag Basic
##------------------------------------------------------------------------------

## What a hack ... I quickly needed a way of putting content in the title frag div's
## This could be refactored and integrated into body below so we dont have the duplication of this
<%def name="frag_basic(title='', icon='', frag_content=None, include_white_background=True)">
    <div class="frag_bars">
        <%doc><div class="title_bar">
            <div class="title">
                <span class="icon16 i_${icon}"></span><span class="title_text">${title() if hasattr(title, '__call__') else title}</span>
            </div>
            <div class="common_actions">
            </div>
        </div></%doc>
        
        <div class="action_bar">
            <div class="object_actions_specific">
            </div>        
            <div class="object_actions_common">
            </div>        
        </div>
    </div>
    
    <div class="frag_data c-${c.controller} a-${c.action} u-${'user' if c.logged_in_persona else 'anon'} ${self.attr.frag_data_css_class}">
        % if include_white_background:
        <div class="frag_whitewrap fill">
        % endif
            <div class="frag_col fill">
                ##% if isinstance(frag_content, types.FunctionType):
                % if hasattr(frag_content, '__call__'):
                    ${frag_content()}
                % else:
                    ${frag_content}
                % endif
            </div>
        % if include_white_background:
        </div>
        %endif
    </div>
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

    <%
        # Default creation of URLS - these can be overridden by init_vars()
        import copy
        args   = []
        kwargs = {}
        
        if c.web_params_to_kwargs:
            args, kwargs = c.web_params_to_kwargs
            args   = copy.copy(args)
            kwargs = copy.copy(kwargs)
            self.args   = args
            self.kwargs = kwargs
        
        # Gen frag URL
        if self.attr.frag_url == True:
            kwargs['format'] = 'frag'
            self.attr.frag_url = h.url('current',**kwargs)
        
        kwargs['format'] = 'json'
        self.attr.json_url = h.url('current',**kwargs)
        
        # Gen html URL
        if self.attr.html_url == True:
            if 'format' in kwargs:
                del kwargs['format']
            kwargs['format'] = ''
            if 'sub_domain' in kwargs:
                #log.debug('old subdomain = %s' % kwargs['sub_domain'])
                # AllanC - annoyingly this should never happen ... but somhow the subdomain is leaking out of the URL generator - probably because somewhere there is a still a call to pylons.url rather than web.url
                del kwargs['sub_domain']
            self.attr.html_url = h.url('current', sub_domain='www', **kwargs)
            
        
        
        # Gen RSS URL
        if self.attr.rss_url == True:
            kwargs['format'] = 'rss'
            self.attr.rss_url = h.url('current', **kwargs)
    %>

    % if hasattr(self, 'init_vars'):
        ${self.init_vars()}
    % endif

    % if self.attr.popup_url:
        ${popup.popup_frag(_('What next ...'), self.attr.popup_url)}
    % endif
    
    <div class="frag_bars hide_if_print">
        <div class="title_bar">
            <div class="common_actions">
                ## AJAX Fragment refresh (not visible to user)
                <a class="frag_source" href="${self.attr.frag_url}" style="display: none;">frag source</a>
                ##.current_url()##
                
                ## Reload
                % if config['development_mode']:
                    ##c.format=='frag' and 
                    <a href='' class="icon16 i_reload link_update_frag" title='Reload Fragment'><span>Reload Fragment</span></a>
                    <span class="icon"></span>
                % endif
                <%doc>
                    
                ## Share
                % if self.attr.share_kwargs:
                    ${share.share(**self.attr.share_kwargs)}
                    ## padding
                    <span class="icon"></span>
                % endif
                </%doc>
                    
                <%doc>
                ## Help
                % if self.attr.help_frag:
                    <%
                        help_url = '/help/' + self.attr.help_frag
                        # GregM: Note the new method does not add classes "frag_col_1 frag_help"!
                    %>
                    <a href="${help_url}" data-frag="${help_url}" class="icon16 i_help link_new_frag" title="${_('Help')}"><span>${_('Help')}</span></a>
                    % if 'help' in kwargs:
                    <script type="text/javascript">${js_open_help}</script>
                    % endif
                % endif
                </%doc>
                
                ## RSS
                % if self.attr.rss_url:
                    <a href='${self.attr.rss_url}' class="icon16 i_rss" title='RSS'><span>RSS</span></a>
                % endif
                
                ## Close
                % if c.format=='frag':
                    <a href='' class="icon16 i_close link_remove_frag" title='${_('Close')}'><span>${_('Close')}</span></a>
                % else:
                    <span class="icon16 i_blank"></span>
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
    </div>
    <div
        class="frag_data c-${c.controller} a-${c.action} u-${'user' if c.logged_in_persona else 'anon'} ${self.attr.frag_data_css_class}"
        data-frag_url="${self.attr.frag_url}"
        data-html_url="${self.attr.html_url}"
        data-json_url="${self.attr.json_url}"
    >
    % if c.format=="frag" and c.result.get('message', '') != '':
        <% json_message = h.json.dumps(dict(status=c.result['status'], message=c.result['message'])) %>
        <div class="flash_message_data event_load" style="display:none;" data-message-json="${json_message}"></div>
    % endif
        <span style="clear: both; display: block;"></span>
        ##<div class="title">
            ## Title
        ##    <span class="title_text">${self.attr.title}</span>
        ##</div>
        ${next.body()}
    </div>
</%def>

<%def name="georss_link(georss_url=None)">
    <%
        ## Bug issue #300
        ## AllanC - This is incorrect! if the current URL is profile/index the RSS source returns a 403 Error when it trys to access it
        params = dict(request.params)
        if "format" in params:
            del params["format"]
        if "include_fields" in params:
            del params["include_fields"]
        feed = h.url(
            'current',
            format         = 'rss',
            include_fields = 'attachments',
            **params
        )
        
        georss_url = dict(
            controller = 'misc',
            action     = 'georss',
            location   = request.params.get('location'),
            feed       = feed
        )
        georss_url_frag = copy.copy(georss_url)
        georss_url_frag['format'] = 'frag'
        
        georss_url      = h.url(**georss_url)
        georss_url_frag = h.url(**georss_url_frag)
    %>
    <a class="link_new_frag" href="${georss_url}" title="${_('View on map')}" data-frag="${georss_url_frag}"><span class="icon16 i_map"></span>${_('Show these results on a map')}</a>
</%def>
