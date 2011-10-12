<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%namespace name="confirmpost" file="/html/web/misc/confirmpost.mako" />

<div data-role="page">
    <div data-role="content">
        ${confirmpost.confirm_message()}
    </div>
</div>
