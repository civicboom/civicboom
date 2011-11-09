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
                <div class="h1 fl">1.</div>
                <div class="na-padleft">
                    <h1 class="fl">${_('Post your _content on Civicboom:')}</h1>
                    <div class="fr">${h.secure_link(h.url('new_content', target_type='article'   ), _("Post _content") , css_class="button")}</div>
                    <div class="cb"></div>
                </div>
            </div>
            <div class="frag_whitewrap na-other">
                <div class="h1 fl">2.</div>
                <div class="na-padleft">
                    <h1 class="fl">${_('Respond to a request:')}</h1>
                    <div class="fr"><a href="${h.url(controller='contents', target_type='assignment', action='index')}" class="button" onclick="cb_frag($(this), '${h.url(controller='contents', target_type='assignment', action='index', format='frag')}'); return false;">${_('See full list')}</a></div>
                    <div class="cb"></div>
                </div>
            </div>
        </div>
    </div>
</%def>
