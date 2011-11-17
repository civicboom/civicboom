##<%inherit file="/frag/common/frag.mako"/>

##<%namespace name="member_includes" file="/html/web/common/member.mako" />

<%!
    title               = 'Flag'
    icon_type           = 'flag'
%>

<%def name="body()">
    ##<% args, kwargs = c.web_params_to_kwargs %>

    ${flag_form(c.id)}
</%def>


##------------------------------------------------------------------------------
## Flag Form
##------------------------------------------------------------------------------

<%def name="flag_form(id)">
    ##<div id="flag_content" class="hideable">
    <div style="padding-bottom: 6px;">
##      <p class="form_instructions">${_('Flag this _content as inappropriate')}</p>
      ${h.form(h.args_to_tuple(controller='content_actions', action='flag', id=id, format='redirect'), data=dict(json_complete="[['close_modal']]"))}
          <select name="type">
              <% from civicboom.model import FlaggedEntity %>
              % for type in [type for type in FlaggedEntity._flag_type.enums if type!="automated"]:
              <option value="${type}">${_(type.capitalize())}</option>
              % endfor
          </select>
          <p style="padding-top: 3px; padding-bottom: 3px;" class="form_instructions">${_('Comment (optional)')}</p>
          <textarea name="comment" style="width:90%; height:3em;"></textarea>
          <input type="submit" name="flagit" value="${_("Flag it")}" class="" onclick="$.modal.close();"/>
          ##<a class="simplemodal-close">${_("Cancel")}</a>
      ${h.end_form()}
    </div>
</%def>
