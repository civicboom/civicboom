<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="get_widget" file="/frag/misc/get_widget.mako"/>

<%def name="title()">${_("Welcome")}</%def>




##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <table style="display: inline-block; vertical-align: middle;"><tr>
        <td style="width: 200px;">${assignments_active()}</td>
        <td                      >${what_is()           }</td>
        <td style="width: 200px;">${mobile()            }</td>
    </tr></table>
</%def>

##------------------------------------------------------------------------------
## What is
##------------------------------------------------------------------------------

<%def name="assignments_active()">
<%
    c.widget['title' ] = _('Get involved with the latest _assignments on _site_name')
    c.widget['width' ] = 160
    c.widget['height'] = 250
%>
##<div style="padding: 1em;">
${get_widget.widget_iframe(protocol=None, iframe_url=h.url('contents', subdomain='widget', list='assignments_active'))}
##</div>
</%def>



##------------------------------------------------------------------------------
## What is
##------------------------------------------------------------------------------

<%def name="what_is()">
    <section class='description'>
        <div style="float: right; padding-bottom: 1em;">
            <a class="button" href="${url(controller='account', action='signin')}">${_('Sign up')}</a>
        </div>
        
        <div class='description_container'>
            <h1>${_('What is _site_name?')}</h1>
            <div class="steps_container">
                <div id="step_container">
                    <ul>
                        ${steps()}
                    </ul>
                </div>
                
                <a class="step_nav step_back" onclick="step_back(); return false;">&lt;</a>
                <a class="step_nav step_next" onclick="step_next(); return false;">&gt;</a>
                
                <script type="text/javascript">
                    var class_current = 'current';
                    function step_remove_current() {
                        var container = $('#step_container');
                        var current = container.find('.'+class_current);
                        current.removeClass(class_current);
                        current.fadeOut();
                        return current;
                    }
                    function step_next() {
                        var current = step_remove_current();
                        var next    = current.next();
                        if (!next.length) {next = $('#step_container ul li:first-child');}
                        next.addClass(class_current);
                        next.fadeIn();
                    }
                    function step_back() {
                        var current = step_remove_current();
                        var prev    = current.prev();
                        if (!prev.length) {prev = $('#step_container ul li:last-child');}
                        prev.addClass(class_current);
                        prev.fadeIn();
                    }
                    $('.step_next').click();
                </script>
                
                ##<div style="clear:both"></div>
            </div>
        </div>
        
        <a style="float:right;" class="button" href="${url(controller='misc', action='about')}">${_('Learn more')}</a>
        <p style="font-size: x-large; font-weight: bold;">${_("Don't just read it. Feed it.")}</p>
        
        <div style="clear: both; padding: 0.5em;"></div>
        
        <a style="float:right; color: black; background: none;" class="button" href="mailto:contact@civicboom.com">${_('Get in touch')}</a>
        <p style="font-weight: bold;">${_('Are you an organisation? Do you want to know how Civicboom can help you?')}</p>
    </section>
</%def>





##------------------------------------------------------------------------------
## Mobile
##------------------------------------------------------------------------------

<%def name="mobile()">
    <section class="mobile">
        
        <h2>${_('Grab the _site_name app')}</h2>
        <a href="${url(controller='misc', action='about', id='mobile')}">
            <img src="/images/misc/mobile_android.png">
        </a>
        <p>${_('Coming soon:')}</p>
        <ul>
            <li>Blackberry</li>
            <li>iPhone</li>
        </ul>
        
    </section>
</%def>


##------------------------------------------------------------------------------
## Steps
##------------------------------------------------------------------------------

<%def name="step()">
    ##% for s in range(3):
    <li class="step hideable">
        <div class="step_main">
            <div class="step_padding">
                ${caller.main()}
            </div>
        </div>
        <div class="step_description">
            <div class="step_padding">
                ${caller.description()}
            </div>
        </div>
    </li>
    ##% endfor
</%def>


<%def name="steps()">

    <%self:step arg>
        <%def name="main()">
            <div style="text-align: center; margin-top: 3em;"><img src="/images/civicboom.png" alt="Civicboom Logo" style="width: 50%;"/></div>
        </%def>
        <%def name="description()">
            <p style="font-weight: bold; font-size: 120%;">Civicboom empowers you connect, create and collaborate on what matters to you. </p>
        </%def>
    </%self:step>

    <%self:step>
        <%def name="main()">
            more steps
        </%def>
        <%def name="description()">
            more steps
        </%def>
    </%self:step>    
    
</%def>

