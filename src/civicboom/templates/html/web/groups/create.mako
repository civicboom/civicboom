<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="group_settings" file="/frag/settings/panel/general_group.mako" import="body"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = group
        if c.action in ('new', 'create'):
            self.attr.frags = [group]
            self.attr.frag_col_sizes = [2]
    %>
</%def>


##------------------------------------------------------------------------------
## new/edit group
##------------------------------------------------------------------------------

<%def name="group()">
    ${frag.frag_basic(title=_('%s _Group') % c.action.capitalize(), icon='group', frag_content=group_content)}
</%def>
<%def name="group_content()">
${group_settings.body()}
</%def>

##------------------------------------------------------------------------------
## Quick group
##------------------------------------------------------------------------------

<%def name="quick_group()">
    ${frag.frag_basic(title=_('Quick _Group'), icon='group', frag_content=quick_group_content)}
</%def>
<%def name="quick_group_content()">
    <script type="text/javascript">
      var quickOrder = ['default_role', 'join_mode', 'member_visibility', 'default_content_visibility'];
      var quickSelection = {'news': '0010',
                            'interest':'1100',
                            'educational':'2200',
                            'marketing':'0101',
                            'internal':'2211',
                            'business':'2211',
                            'creative':'0010',
                            'research':'2101'};
      var quickBlurb =     {'news': '${_("Connect with your community and audience by creating _Groups for your titles, sections or issues. Send out breaking news requests, get coverage directly from the source and utilise the power of the crowd. Empower the community you serve to be part of news and its creation.")}',
                            'interest':'${_("Create a _Group and crowdsource social action, motivate advocacy from your community, generate real case studies and _articles for your publications, heighten awareness, build a movement. Use the creativity of your community to heighten awareness on issues you need to know about.")}',
                            'educational':'${_("Students can create _Groups on specific topics - evolve ideas together, share your creative work, tap into the wider community, build your portfolio. University departments can utilise the collective wisdom of their students to develop and improve courses and reach new audiences.")}',
                            'marketing':'${_("Get first hand experience and feedback directly form your customers and target audiences. What products do your consumers want? How can you improve? Set requests through your _Group and ask the crowd.")}',
                            'internal':'${_("Create a private _Group and empower your employees to submit ideas, upload their reports from events, share experiences - good and bad. Identify champions, learn from your workforce: they have the insight to help make your workplace and business better for all.")}',
                            'business':'${_("Work with your partners and customers: use _Groups to push out new products, get engagement on hot topics associated with your industry, build a community around your brand, and improve brand awareness to wider audiences.")}',
                            'creative':'${_("From documentary makers to designers and everything in between, ask the crowd - photos, text, videos, audio. Empower people to share their experience, authenticity and creativity for your project through a _Group.")}',
                            'research':'${_("Work in a closed, private _Group with key people in your organisation or trusted external sources in research on any topic you choose.")}' };
      function changePlaceholder (jquery_object, text) {
        if (typeof text === 'undefined') var text = '';
        var oldPlaceholder = jquery_object.attr('placeholder'); 
        jquery_object.attr('placeholder', text);
        if ((!Modernizr.input.placeholder) && (jquery_object.val() === oldPlaceholder))
          jquery_object.val(jquery_object.attr('placeholder'));
      }
      $(function () {
      var defaultDescPlaceholder = $('textarea#group_description').attr('placeholder');
        if (!Modernizr.input.placeholder) {
          if ($('textarea#group_description').val() == '')
            $('textarea#group_description').val($('textarea#group_description').attr('placeholder'));
          $('textarea#group_description').focus(function (e) {
            $(this).val('');
          });
          $('textarea#group_description').blur(function (e) {
            if ($(this).val() === '') $(this).val($(this).attr('placeholder'));
          });
          $('textarea#group_description').parents('form').submit(function (e) {
            if ($('textarea#group_description').val() === $('textarea#group_description').attr('placeholder')) $('textarea#group_description').val('');
          });
        }
        $('input.quickbutton').click(function () {
          var quickHilite = false
          $('td.quickchangehilite').removeClass('quickchangehilite');
          var quickName = $(this).attr('name');
          if (typeof quickSelection[quickName] != 'undefined') {
            if (quickSelection[quickName].length == quickOrder.length) {
              for (var qI = 0; qI < quickOrder.length; qI ++) {
                var quickValue = 1 * quickSelection[quickName][qI];
                $('[name='+quickOrder[qI]+']')[quickValue].checked = true;
                quickHilite = true;
              }
            }
          }
          changePlaceholder ($('#group_description'), quickBlurb[quickName]);
          if (quickHilite) $('.quickchange:checked').parents('td').addClass('quickchangehilite');
          hiliteQuickButtons (quickSelection[quickName]);
        });
        
        function hiliteQuickButtons (quickString) {
          var quickHilite = false;
          $('.quickbutton').removeClass('quickhilite');
          for (var qS in quickSelection) {
            if (quickSelection[qS] == quickString) {
              $('.quickbutton[name='+qS+']').addClass('quickhilite');
              quickHilite = true;
            }
          }
          return quickHilite;
        }
        $('input.quickchange').click(function () {
          var quickString = '';
          for (var qI = 0; qI < quickOrder.length; qI ++) {
            quickString = quickString + $('[name='+quickOrder[qI]+']').index($('[name='+quickOrder[qI]+']:checked'));
          }
          $('td.quickchangehilite').removeClass('quickchangehilite');
          if (hiliteQuickButtons (quickString)) $('.quickchange:checked').parents('td').addClass('quickchangehilite');
          changePlaceholder ($('#group_description'), defaultDescPlaceholder);
        });
      });
    </script>
    <form id="quick_group">
      <table class="">
        <tr class="padding">
         <td colspan="2" class="bold bigger">Need help?</td>
        </tr>
        <tr class="doublepadding">
          <td colspan="2">The buttons below represent some of the most common uses for hubs. Click one to highlight the recommended options for that type of hub.)}</td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="news" value="${_('News Organisation')}" /></td>
          <td><input class="button quickbutton" type="button" name="interest" value="${_('Interest Group / Charity')}" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="educational" value="${_('Educational Establishment')}" /></td>
          <td><input class="button quickbutton" type="button" name="marketing" value="${_('Marketing')}" /></td>
        </tr>
        <tr class="padding">
          <td><input class="button quickbutton" type="button" name="internal" value="${_('Internal Communications')}" /></td>
          <td><input class="button quickbutton" type="button" name="business" value="${_('Business')}" /></td>
        </tr>
        <tr class="doublepadding">
          <td><input class="button quickbutton" type="button" name="creative" value="${_('Creative Collaboration')}" /></td>
          <td><input class="button quickbutton" type="button" name="research" value="${_('Research')}" /></td>
        </tr>
        <tr class="padding">
          <td colspan="2" class="bold bigger center">OR</td>
        </tr>
        <tr>
          <td colspan="2" class="bold big">${_('Create your own _Group by filling in the form to suit your needs.')}</td>
        </tr>
      </table>
    </form>
</%def>


##------------------------------------------------------------------------------
## Deprication
##------------------------------------------------------------------------------

<%doc>
    Radio button temp example
    <%
    if ():
        type_selected = "checked='checked' "
    else:
        type_selected = ""
    %>
    ##<option value="${newsarticle_type.id}" ${type_selected}>${newsarticle_type.type}</option>
    <input type="radio" name="newsarticle_type" value="${newsarticle_type.id}" ${type_selected}/>${newsarticle_type.type}</a>
</%doc>
