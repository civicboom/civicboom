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