var media_thumbnail_timers = {};

function updateMedia(id, hash) {
  $.getJSON(
    '/media/' + hash + '.json',
    processingStatus${id}
  );
  function processingStatus(data) {
    _status = data.data.status;
    /*alert("Status got = "+_status);*/
    if(!_status) {
      clearInterval(media_thumbnail_timers[id]);
      delete media_thumbnail_timers[id];
      /*alert("processing complete reload the image!!!");*/
      $("#media_thumbnail_" + id).src = "${media['thumbnail_url']}" + "?" + (new Date().getTime());
      $("#media_status_" + id).text("");
    }
    else {
      $("#media_status_" + id).text(_status);
    }
  }
}