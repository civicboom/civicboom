/**
 * @author Greg Miell
 * @title Additional javascript object prototype functions
 */
Array.prototype.remove = function (subject) {
	var r = new Array();
	for(var i = 0, n = this.length; i < n; i++)
	{
		if(!(this[i]==subject))
		{
			r[r.length] = this[i];
		}
	}
	return r;
}
Array.prototype.contains = function (subject) {
	for(var i = 0, n = this.length; i < n; i++)
	{
		if((this[i]==subject))
		{
			return true;
		}
	}
	return false;
}

// JQUERY PLUGIN: I append each jQuery object (in an array of
// jQuery objects) to the currently selected collection.
jQuery.fn.appendEach = function(arrayOfWrappers) {

  // Map the array of jQuery objects to an array of
  // raw DOM nodes.
  var rawArray = jQuery.map(arrayOfWrappers, function(value, index) {

    // Return the unwrapped version. This will return
    // the underlying DOM nodes contained within each
    // jQuery value.
    return (value.get() );

  });
  // Add the raw DOM array to the current collection.
  this.append(rawArray);

  // Return this reference to maintain method chaining.
  return (this );

};