<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%namespace name="terms_includes" file="/html/web/misc/about/terms.mako" />

<%def name="body()">
    <div data-role="page">
        <div data-role="header">
            <h1>Terms and conditions</h1>
        </div>
        
        <div data-role="content">
            ##style='font-size: 75%;'
            ${terms_includes.terms_list()}
        </div>
    </div>
</%def>