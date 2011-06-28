<%inherit file="/frag/common/frag.mako"/>

<%def name="body()">
    <div class="frag_col">
        <h1>new stuff</h1>
        
        ${h.secure_link(h.url('new_content', target_type='article'   ), _("Post a story") , css_class="button")}
    </div>
</%def>