<%namespace name="upgrade_plans" file="/html/web/misc/about/upgrade_plans.mako"/>
<h1>${_('Woah there, you seem to have reached your account limit!')}</h1>
<h2>${_('The good news is you can upgrade and get even more from _site_name')}</h2>
${upgrade_plans.upgrade_details()}
## AllanC - Wanted to keep all upgrade information in one template so info was not fragmented in codebase