<%inherit file="html_header.mako"/>

<%def name="body()">
  ${flash_message()}
  ${next.body()}
</%def>


## AllanC
## Flash Message Area - some form functions will need to return a status to inform users the operation completed
## This displays the message and then removes it from the session once it is displayed the first time
## See "Definitive Guide to Pylons" pg 191 for details
<%def name="flash_message()">
  % if session.has_key('flash_message'):
    <div id="flash_message">${session.get('flash_message')}</div>
    <%doc>
    <script type="text/javascript">
        var a = new YAHOO.util.Anim(YAHOO.util.Dom.get('flash_message'));
        a.attributes.opacity  = {to: 1};
        a.duration            = 5.0;
        ##a.attributes.height   = {to: 0};
          ##YAHOO.util.Easing.easeOut
        a.onComplete.subscribe(function() {
          var b = new YAHOO.util.Anim(YAHOO.util.Dom.get('flash_message'));
          b.attributes.opacity  = {to: 0};
          b.duration            = 1.0;
          b.attributes.height   = {to: 0};
          ##b.attributes.padding  = {to: 0};
          ##b.attributes.margin   = {to: 0};
          b.onComplete.subscribe(function() {
            ## AllanC - If the element is removed then IE gets confused and puts the footer at the top
            ## Why in gods name this happens is anybodys guess ... ****ing IE!
            ## I tryed other ways of removing the element with the same effect. Investigate IE dom
            ##
            ## Update, this is not an issue with the new layout, IE is behaving itself.
            YAHOO.util.Dom.setStyle('flash_message','display','none');
            ##YAHOO.util.Dom.setStyle('flash_message','margin','0em'); //an alternative was to set margin and padding to 0
          });
          b.animate();
        })
        a.animate();
    </script>
    </%doc>
    <%
      del session['flash_message']
      session.save()
    %>
  %endif
</%def>