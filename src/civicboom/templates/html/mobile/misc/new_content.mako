<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="title()">${_('New _content')}</%def>

<%def name="body()">
    <div data-role="page" data-theme="b" id="new_content">
        ${self.header()}
        
        <div data-role="content">            
            ${self.form_button(h.url('new_content', target_type='assignment'), _("Ask for _articles"))}
            ${self.form_button(h.url('new_content', target_type='article'   ), _("Post a _article")  )}
            <a href="${h.url(controller='contents', target_type='assignment', action='index')}"><button>${_('See latest _assignments')}</button></a>
        </div>
        
        ${self.footer()}
    </div>
</%def>

<%doc>
    % for org in d['list']:
        <li class="mo-help">
            <div class="fl">${member_avatar(org)}</div>
            <div class="na-org-text">
                ${_('Post directly to %s') % org.get('name')}
            </div>
            <div class="pr">
                <div class="mo-help-l">
                    ${org.get('description')}
                </div>
            </div>
            <div class="fr">
                % if org.get('push_assignment'):
                    ${h.secure_link(h.url('new_content', target_type='article', parent_id=org.get('push_assignment')  ), _("Post a story") , css_class="button")}
</%doc>