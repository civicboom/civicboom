<%!
    import types
    import copy

    title               = 'List'
    icon_type           = 'list'
    
    share_kwargs        = None
    
    frag_url            = True
    html_url            = True
    rss_url             = False
    ##auto_georss_link    = False
    
    help_frag           = None # This can be set to a string name to activate '/misc/help/HELP_FRAG' to render '/frag/help/HELP_FRAG.mako'
    
    frag_data_css_class = ''
%>



<%namespace name="share" file="/frag/common/share.mako"/>

##------------------------------------------------------------------------------
## Frag Basic
##------------------------------------------------------------------------------

## What a hack ... I quickly needed a way of putting content in the title frag div's
## This could be refactored and integrated into body below so we dont have the duplication of this
<%def name="frag_basic(title='', icon='', frag_content=None)">
    <div class="title_bar">
        <div class="title">
            <span class="icon icon_${icon}"></span><span class="title_text">${title}</span>
        </div>
        <div class="common_actions">
        </div>
    </div>
    
    <div class="action_bar">
        <div class="object_actions_specific">
        </div>        
        <div class="object_actions_common">
        </div>        
    </div>
    
    <div class="frag_data ${self.attr.frag_data_css_class}">
        <div class="frag_col">
            ##% if isinstance(frag_content, types.FunctionType):
            % if hasattr(frag_content, '__call__'):
                ${frag_content()}
            % else:
                ${frag_content}
            % endif
        </div>
    </div>
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

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
            self.attr.frag_url = h.url('current',**kwargs)
        
        # Gen html URL
        if self.attr.html_url == True:
            if 'format' in kwargs:
                del kwargs['format']
            if 'subdomain' in kwargs:
                #log.debug('old subdomain = %s' % kwargs['subdomain'])
                # AllanC - annoyingly this should never happen ... but somhow the subdomain is leaking out of the URL generator - probably because somewhere there is a still a call to pylons.url rather than web.url
                del kwargs['subdomain']
                
            self.attr.html_url = h.url('current', subdomain='', **kwargs)
        
        # Gen RSS URL
        if self.attr.rss_url == True:
            kwargs['format'] = 'rss'
            self.attr.rss_url = h.url('current', **kwargs)
    %>

    % if hasattr(self, 'init_vars'):
        ${self.init_vars()}
    % endif

    ## AJAX Fragment refresh (not visible to user)

    <a class="frag_source" href="${self.attr.frag_url}" style="display: none;">frag source</a>
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
                <span class="icon"></span>
            % endif
            
            ## Share
            % if self.attr.share_kwargs:
                ${share.share(**self.attr.share_kwargs)}
                ## padding
                <span class="icon"></span>
            % endif
            
            ## Help
            % if self.attr.help_frag:
                <%
                    help_url = '/help/' + self.attr.help_frag
                    js_open_help = h.literal("cb_frag($(this), '%s', 'frag_col_1');" % help_url)
                %>
                <a href="${help_url}" onclick="${js_open_help} return false;" class="icon icon_help" title="${_('Help')}"><span>${_('Help')}</span></a>
                % if 'help' in kwargs:
                <script type="text/javascript">${js_open_help}</script>
                % endif
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
        ## Bug issue #300
        ## AllanC - This is incorrect! if the current URL is profile/index the RSS source returns a 403 Error when it trys to access it
        feed = h.url(
            'current',
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
        
        georss_url      = h.url(**georss_url)
        georss_url_frag = h.url(**georss_url_frag)
    %>
    <a href="${georss_url}" title="${_('View on map')}" class="icon icon_map" onclick="cb_frag($(this), '${georss_url_frag}'); return false;"><span>${_('View on map')}</span></a>
</%def>
