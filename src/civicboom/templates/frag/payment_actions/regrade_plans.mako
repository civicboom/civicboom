<%inherit file="/frag/common/frag.mako"/>
<%namespace name="upgrade_plans"           file="/html/web/misc/about/upgrade_plans.mako" />
<div class="frag_whitewrap">
    ${upgrade_plans.blurb()}
    <p>
    <div style="font-size: 75%">
        ${upgrade_plans.upgrade_details('regrade_plans')}
    </div>
    </p>
</div>
