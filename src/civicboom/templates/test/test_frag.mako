<%inherit file="/web/common/html_base.mako"/>

<h1>Frag Test</h1>

<div id='frag_containers'>
    <% frag_url = url('content', id=1, format='frag') %>
    ${h.frag_div("frag_", frag_url, class_="frag_container")}
    ##<div id="frag_1" class="frag_container" style="border: 1px dashed red;">
        ##<p>hello all</p>
        ##<a href="${url("content", id=1, format='frag')}" onclick="cb_frag($(this)); return false;">Link of AJAX</a>
    ##</div>
</div>