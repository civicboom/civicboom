
<%namespace name="widget_code" file="/widget/get_widget_code.mako" />

<h1>${_('Widget test drive')}</h1>
<p>${_('This widget is a preview of the widget for %s' % c.widget_user_preview.username)}</p>
${widget_code.get_widget_code(c.widget_user_preview)}
