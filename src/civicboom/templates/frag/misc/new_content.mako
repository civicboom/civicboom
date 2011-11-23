<%inherit file="/frag/common/frag.mako"/>
<%namespace name="member_includes" file="/html/web/common/member.mako"     />

<%def name="member_avatar(member, img_class='')">
    ${member_includes.avatar(member, class_='thumbnail', img_class=img_class)}
</%def>

<%def name="body()">
    <div class="frag_col">
        <div class="new-article">
            <div class="frag_whitewrap">
                <h1>
                    ${_('Great! You want to post _content...')}<br />
                    ${_('You now have two choices:')}
                </h1>
            </div>
            <div class="frag_whitewrap na-other">
                <div class="fr">${h.secure_link(h.url('new_content', target_type='article'   ), _("Post _content") , link_class="button")}</div>
                <h1>${_('1. Post your story on Civicboom:')}</h1>
            </div>
            <div class="frag_whitewrap na-other">
                <div class="fr"><a href="${h.url(controller='contens', target_type='assignment', action='index')}" class="button link_new_frag" data-frag="${h.url(controller='contents', target_type='assignment', action='index', format='frag')}">${_('See full list')}</a></div>
                <h1>${_('2. Respond to a _assignment:')}</h1>
            </div>
        </div>
    </div>
</%def>
