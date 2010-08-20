// Misc Functions

function confirm_before_follow_link(link_element, message) {
  var confirmation = confirm(message);
  if (confirmation) {
    window.location = link_element;
  }
}

// http://www.sean.co.uk/a/webdesign/javascriptdelay.shtm
function wait(millis) {
    var date = new Date();
    var curDate = null;
    
    do { curDate = new Date(); }
    while(curDate-date < millis);
}