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
        <div style="width: 420px;">
            <div>
                <h1>Link</h1>
                <p>
                    Paste link in <b>email</b> or <b>IM</b><br />
                    <textarea onclick="this.focus();this.select();" readonly="readonly" style="width: 100%">${h.url(d['type'], action='show', id=d['id'], qualified=True)}</textarea>
                </p>
                % if d['type']=='content':
                    <h1>Embed</h1>
                    <p>
                        Paste HTML to embed in your website<br />
                        <textarea onclick="this.focus();this.select();" readonly="readonly" style="width:100%"><div class="civicboom-ranger" boom:type="content" boom:id="${d['id']}" boom:img="64"${' boom:host="https://localhost.civicboom.com"' if config['development_mode'] else ''} boom:responses="4"><h2>Share your _content on Civicboom!</h2><div class="holder"></div><a href="${h.url('new_content', parent_id=d['id'], qualified=True)}" class="share">Click here to share your story!</a></div><script type="text/javascript" src="${h.wh_url("public", "javascript/_boom_ranger.js")}"></script></textarea><br />
                        Please note this code is in Beta and is subject to change<br /><br />
                    </p>
                    <h2>Styling embedded content</h2>
                    <p>
                      The HTML above can be styled using some simple css. For example the following CSS could be used:
                    </p>
                    <br />
                    <div style="width: 100%; overflow: auto; height: 8.5em">
                    <pre>.civicboom-ranger { color: #00C; }
.civicboom-ranger h2 { font-family: sans-serif; }
.civicboom-ranger .holder img { padding: 0 0.5 em }
.civicboom-ranger .holder h3 { padding: 0; margin: 0; }
.civicboom-ranger .holder .content { font-size: 0.75em; }
.civicboom-ranger .holder .creator { font-size: 0.75em; }
.civicboom-ranger .share { color: #F0F; }</pre>
                    </div>
                % endif
            </div>
            <div>
                <h1>QR Code</h1>
                <img src="${h.url(d['type']+'_action', id=d['id'], action='qrcode')}" alt="QRCode for ${d['type']} ${d['id']}"/>
            </div>
        </div>
    % endif
</%def>
