<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

<%def name="page_title()">
    ${_("Edit~")}
</%def>

## page structure defs
<%def name="body()">
    <div data-role="page">
        ${components.header()}
        <div data-role="content">

            <form action="${h.url(controller='contents', action='new')}" method="POST" data-ajax="false" data-theme="b">
                <div data-role="fieldcontain" data-theme="b">
                    <label for="title">${_("Title")}</label>
                    <input data-theme="b" type="text" id="title" name="title" />
                    <label for="content">${_("Content")}</label>
                    <textarea data-theme="b" id="content" name="content">
                    
                    </textarea>
                </div>
                <div data-role="fieldcontain" data-theme="b">
                    <input data-theme="b" type="submit" name="submit" value="${_("Post!")}"/>
                </div>
            </form>

        </div>
    </div>
</%def>