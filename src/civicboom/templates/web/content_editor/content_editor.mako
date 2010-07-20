<%inherit file="/web/html_base.mako"/>

<div class="content_form">

  <form action="" method="post">
    <fieldset><legend>Content</legend>
      <p class="form_instuctions">Got an opinion? want to ask a question?</p>


        <p><label for="form_title">Title</label><input id="form_title" name="form_title" type="text" style="width:80%;"/><span class="tooltip tooltip_icon"><span>extra info</span></span></p>
  
        ${richtext()}
  
        <input type="submit" name="submit_draft"   value="Save Draft"   style="float: right;"/>
  
        <p><label for="form_owner">By</label>
        <select name="form_owner">
          <option value="" selected="selected">my_username</option>
          <option value=""                    >Group I am member of 1</option>
          <option value=""                    >Group I am member of 2</option>
        </select>
        <span class="tooltip tooltip_icon"><span>extra info</span></span>
        </p>
        <p><label for="form_tags">Tags</label><input id="form_tags" name="form_tags" type="text" value="cat garden"/><span class="tooltip tooltip_icon"><span>extra info</span></span></p>

  </form>
  
</div>


##------------------------------------------------------------------------------
## YUI Rich Text Component
##------------------------------------------------------------------------------
<%def name="richtext(width='100%', height='300px')">

  <!-- Rich Text Component -->
  <div class="yui-skin-sam">
    <textarea id="form_content" name="form_content" style="width:${width}; height:${height};">The cat was playing in the garden.</textarea>  
    <script type="text/javascript">
      var myEditor = new YAHOO.widget.SimpleEditor('form_content', {
          height: '${height}',
          width: '${width}',
          //dompath: true //Turns on the bar at the bottom
          toolbar: {
            collapse: true,
            titlebar: 'Editing Tools',
            draggable: false,
            buttons: [
              { group: 'text', label: 'Text Effects',
                  buttons: [
                    { type: 'push', label: 'Bold CTRL + SHIFT + B', value: 'bold' },
                    { type: 'push', label: 'Italic CTRL + SHIFT + I', value: 'italic' }
                  ]
              },
              { type: 'separator' },
              { group: 'indentlist', label: 'Lists',
                  buttons: [
                      { type: 'push', label: 'Create an Unordered List', value: 'insertunorderedlist' },
                      { type: 'push', label: 'Create an Ordered List', value: 'insertorderedlist' }
                  ]
              },
              { type: 'separator' },
              { group: 'insertitem', label: 'Insert Link',
                  buttons: [
                      { type: 'push', label: 'HTML Link CTRL + SHIFT + L', value: 'createlink', disabled: true }
                  ]
              }
            ]
          }
      });
      myEditor.set("handleSubmit", true); 
      myEditor.render();										
    </script>

  </div>
  <!-- End Rich Text Component -->

</%def>