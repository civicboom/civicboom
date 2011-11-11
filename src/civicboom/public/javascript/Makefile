HEAD=\
	modernizr-1.7.js \
	swfobject.js \
	jquery-1.6.4.js \
	prototypes.js \
	misc.head.js \
	url_encode.js \
	cb_frag.js \

FOOT=\
	jquery.ui.js \
	jquery.ui.stars-3.0.1.js \
	jquery.ui.timepicker-addon.js \
	jquery.html5-0.0.1.js \
	jquery.scrollTo.js \
	jquery.simplemodal-1.4.1.js \
	jquery.uploadify.v2.1.4.js \
	jquery.simple-color-picker.js \
	jquery.ba-hashchange.min.js \
	jquery.limit-1.2.js \
	jquery.getUrlParam.js \
	jquery.cookie.js \
	jquery.jcarousel.js \
	jquery.swfobject.1-1-1.js \
	invite.js \
	mobile.js \
	rpx.js \
	misc.foot.js \
	gears_init.js \
	geo.js \
	OpenLayers.js \
	minimap.js \

MOBILE=\
	jquery-1.6.2.js \
	jquery.mobile.cb_settings.js \
	jquery.mobile-1.0rc2.js \
	geo.js \
	#jquery.ui.datepicker.mobile.js \

all: _combined.head.js _combined.foot.js _combined.mobile.js

_combined.head.js: Makefile $(HEAD)
	cat $(HEAD) | yui-compressor --type js -o _combined.head.js

_combined.foot.js: Makefile $(FOOT)
	cat $(FOOT) | yui-compressor --type js -o _combined.foot.js

_combined.mobile.js: Makefile $(MOBILE)
	cat $(MOBILE) | yui-compressor --type js -o _combined.mobile.js

clean:
	rm -f _combined.head.js _combined.foot.js _combined.mobile.js


#
# things to be called manually to update when necessary
#

#jquery.ui.js:
#	git clone git://github.com/jquery/jquery-ui.git
#	cd jquery-ui && git checkout 1.8.14
#	cd jquery-ui/ui/ && cat \
#		jquery.ui.core.js \
#		jquery.ui.widget.js \
#		jquery.ui.mouse.js \
#		jquery.ui.position.js \
#		jquery.ui.autocomplete.js \
##		jquery.ui.datepicker.js \
#		jquery.ui.button.js \
#		jquery.ui.tabs.js \
#		jquery.ui.slider.js \
#		jquery.ui.accordion.js \
#		> ../../jquery.ui.js
#	rm -rf jquery-ui

OpenLayers.js:
	svn checkout http://svn.openlayers.org/tags/openlayers/release-2.10/ openlayers
	cp OpenLayers.cfg ./openlayers/build/
	cd openlayers/build && ./buildUncompressed.py OpenLayers
	mv openlayers/build/OpenLayers.js ./
	patch OpenLayers.js OpenLayers.patch
	rm -rf openlayers

# the janrain API suggests we link to their servers, but their slow
# servers are blocking our page rendering speed. Hacky solution:
# bundle their JS within ours
rpx.js:
	wget https://s3.amazonaws.com/static.rpxnow.com/js/lib/rpx.js
