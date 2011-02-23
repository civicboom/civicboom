HEAD=\
	Modernizr.js swfobject.js jquery-1.5.js \
	misc.js url_encode.js cb_frag.js

FOOT=\
	jquery.ui.js jquery.ui.stars-3.0.1.js \
	jquery.html5-0.0.1.js jquery.scrollTo.js jquery.simplemodal.1.4.1.min.js \
	jquery.uploadify.v2.1.4.js jquery.simple-color-picker.js \
	gears_init.js geo.js OpenLayers.js minimap.js

OUT=_combined.head.js _combined.foot.js

all: $(OUT)

clean:
	rm -f $(OUT)

_combined.head.js: $(HEAD)
	cat $(HEAD) | yui-compressor --type js -o _combined.head.js

_combined.foot.js: $(FOOT)
	cat $(FOOT) | yui-compressor --type js -o _combined.foot.js


#
# things to be called manually to update when necessary
#

jquery.ui.js:
	git clone git://github.com/jquery/jquery-ui.git
	cd jquery-ui && git checkout 1.8.6
	cd jquery-ui/ui/ && cat \
		jquery.ui.core.js jquery.ui.widget.js jquery.ui.position.js \
		jquery.ui.autocomplete.js jquery.ui.datepicker.js \
		> ../../jquery.ui.js
	rm -rf jquery-ui

OpenLayers.js:
	svn checkout http://svn.openlayers.org/tags/openlayers/release-2.10/ openlayers
	cp OpenLayers.cfg ./openlayers/build/
	cd openlayers/build && ./buildUncompressed.py OpenLayers
	mv openlayers/build/OpenLayers.js ./
	rm -rf openlayers
