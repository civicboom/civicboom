<%inherit file="/web/common/html_base.mako"/>


<h1>Frag Test</h1>

<div id='frag_container'>
    <div id="frag_1" class="frag" style="border: 1px dashed red;">
        <p>hello all</p>
        <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>
    </div>
</div>