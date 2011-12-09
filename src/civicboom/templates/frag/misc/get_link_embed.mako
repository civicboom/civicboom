<%namespace name="components" file="/html/web/common/components.mako" />

##------------------------------------------------------------------------------
## Imports
##------------------------------------------------------------------------------
<%!

%>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    %if d['type'] in ['content', 'member']:
        <div id="link_embed">
            <div>
                <h1>Link</h1>
                <p>
                    Paste link in <b>email</b> or <b>IM</b><br />
                    <textarea onclick="this.focus();this.select();" readonly="readonly" style="width: 100%">${h.url(d['type'], action='show', id=d['id'], qualified=True)}</textarea>
                </p>
                % if d['type']=='content':
                    <h1>Embed</h1>
                    <p>
                        Paste HTML to embed in website<br />
                        <textarea onclick="this.focus();this.select();" readonly="readonly" style="width:100%"><div class="civicboom-ranger" boom:type="content" boom:id="${d['id']}" boom:img="64"${' boom:host="https://localhost.civicboom.com"' if config['development_mode'] else ''} boom:responses="4"><h2>Share your _content on Civicboom!</h2><div class="holder"></div><a href="${h.url('new_content', parent_id=d['id'], qualified=True)}" class="share">Click here to share your story!</a></div><script type="text/javascript" src="${h.wh_url("public", "javascript/_boom_ranger.js")}"></script></textarea><br />
                        Please note this code is in Beta and is subject to change<br /><br />
                    </p>
                % endif
            </div>
            <div>
                <img src="${h.url(d['type']+'_action', id=d['id'], action='qrcode')}" alt="QRCode for ${d['type']} ${d['id']}"/>
            </div>
        </div>
    % endif
</%def>