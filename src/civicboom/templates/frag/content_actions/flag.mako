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
      <p class="form_instructions">${_('Flag this _content as inappropriate')}</p>
      ${h.form(h.args_to_tuple(controller='content_actions', action='flag', id=id, format='redirect'), json_form_complete_actions="cb_frag_remove(current_element);")}
          <select name="type">
              <% from civicboom.model.content import FlaggedContent %>
              % for type in [type for type in FlaggedContent._flag_type.enums if type!="automated"]:
              <option value="${type}">${_(type.capitalize())}</option>
              % endfor
          </select>
          <p class="form_instructions">${_('Comment (optional)')}</p>
          <textarea name="comment" style="width:90%; height:3em;"></textarea>
          <input type="submit" name="flagit" value="Flag it" class=""/>
          ##<a class="simplemodal-close">${_("Cancel")}</a>
      ${h.end_form()}
    ##</div>
</%def>
