<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="components" file="/html/web/common/components.mako" />

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <div style="background: white; border-radius: 16px; padding: 16px; margin: 1em; width: 722px; margin: auto;" class="frag_whitewrap">
        <h1>How to use your profile</h1>
        <p>images go here and stuff is explained, high fives</p>
        
        <%
            my_type = ''
            if c.logged_in_user:
                my_type = 'hub' if c.logged_in_persona.__type__ == 'group' else (c.logged_in_persona.config.get('help_type') or 'ind')
        %>
        
        <div class="special_button">
            % if my_type in ['org', 'hub']:
                <a class="button" href="${url(controller='misc', action='what_is_a_hub')}">Okay, I'm ready to learn about hubs!</a>
            % else:
                <a class="button" href="${url(controller='profile', action='index')}">Okay, I'm ready!</a>
            % endif
        </div>
    </div>
</%def>