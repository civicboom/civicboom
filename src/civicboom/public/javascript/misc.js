// Misc Functions

function confirm_before_follow_link(link_element, message) {
  var confirmation = confirm(message);
  if (confirmation) {
    window.location = link_element;
  }
}
