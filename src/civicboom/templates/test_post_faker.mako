<%inherit file="/web/common/html_base.mako"/>

<h1>Comment Post Faker</h2>

${h.form(url('contents', format='redirect'))}
    <input type="text" name="parent_id" value="">
    <input type="text" name="title" value="Re: stuff">
    <input type="text" name="type" value="comment">
    <textarea name="content" style="width: 100%; height: 100px;"></textarea>
    <br><!--<input type="submit" name="submit_preview" value="Preview">--><input type="submit" name="submit_response" value="fake">
${h.end_form()}

