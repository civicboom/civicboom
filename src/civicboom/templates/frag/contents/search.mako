<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/web/common/location.mako"/>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.attr.title     = _('Search')
        self.attr.icon_type = 'search'
        
        self.attr.frag_data_css_class = 'frag_search'
    %>
</%def>


##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_col">
        <form id="form_search" action="${url('contents')}" method="GET"
              onsubmit="cb_frag($(this), '/contents.frag?' + $('#form_search').serialize()); return false;"
        >
            <fieldset>
                <legend>Search</legend>
                <br/>
                Text: <input type="text" name="query"/>
                <br/>
                Location: ${loc.location_picker()}
                <br/>
                <input type="submit" value="Search"/>
            </fieldset>
        </form>
        <%doc>
        <script type="text/javascript">
            $(document).ready(function(){
                $('#form_search').submit(function(){
                    cb_frag($(this), ${url('contents')} + $('#form_search').serialize());
                    
                    $.post(
                        '%(href_json)s' ,
                        $('#form_search').serialize() ,
                        function(data) {
                            flash_message(data);
                            if (data.status == 'ok') {
                                %(javascript_json_complete_actions)s
                            }
                        },
                        'json'
                    );
                    
                });
            });
        </script>
        </%doc>
    </div>
</%def>