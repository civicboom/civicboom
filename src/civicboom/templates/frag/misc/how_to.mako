<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="components" file="/html/web/common/components.mako" />

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_whitewrap layout">
        <p class="step">${_("3. Your profile: the basics to getting started")}</p>
        
        <%
            my_type = 'ind'
            if c.logged_in_user:
                my_type = 'hub' if c.logged_in_persona.__type__ == 'group' else (c.logged_in_persona.config.get('help_type') or 'ind')
        %>
        
        <div class="getting_started">
            <img src="/images/misc/registration/reg_step3_${my_type}.png" />
        </div>
        
        <div class="special_button">
            % if my_type in ['org', 'hub']:
                <a class="button" href="${url(controller='misc', action='what_is_a_hub')}">${_("Okay, I'm ready to learn about _groups!")}</a>
            % else:
                <a class="button" href="${url(controller='profile', action='index')}">${_("Okay, I'm ready!")}</a>
            % endif
        </div>
    </div>
</%def>