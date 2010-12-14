<%inherit file="/web/common/html_base.mako"/>

<%def name="styleOverides()">
#frag_containers {overflow-x:scroll;}
.frag_container {width:200px; display:inline-block; position:relative;}

</%def>


<h1>Frag Test</h1>

<div id='frag_containers'>
    <div id="frag_1" class="frag_container" style="border: 1px dashed red;">
        <p>hello all</p>
        <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this)); return false;">Link of AJAX</a>
    </div>
</div>