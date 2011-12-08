<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
            ${self.title_logo()}
            <h1>${_('The new way to source and share news!')}</h1>
            <div class="title_content">
                <a href="${h.url(controller='account', action='signin')}" rel="external" data-role="button" data-theme="b">${_('Sign in/Sign up')}</a>
                ##<button data-theme="b"></button>
                ##<p>
                <a href="${h.url(controller="contents", action="index")}" rel="external" data-role="button"               >${_("Just start exploring")}</a>
                ##</p>
                ##<p>
                <a href="${h.url(controller='misc', action='force_web')}" rel="external" data-role="button"               >${_('View the desktop website')}</a>
                ##</p>
            </div>
        </div>
    </div>
</%def>