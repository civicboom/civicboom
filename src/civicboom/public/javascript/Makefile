COMMON=\
	Modernizr.js swfobject.js \
	jquery-1.4.2.js jquery.ui.js \
	jquery.html5-0.0.1.js jquery.ui.stars-3.0.1.js \
	jquery.scrollTo.js jquery.simplemodal.1.4.1.min.js jquery.uploadify.v2.1.4.js \
	misc.js toggle_div.js url_encode.js cb_frag.js

MAPS=\
	gears_init.js geo.js \
	OpenLayers.js \
	minimap.js

OUT=_combined.common.js _combined.maps.js

all: $(OUT)

clean:
	rm -f $(OUT)

_combined.common.js: $(COMMON)
	cat $(COMMON) | yui-compressor --type js -o _combined.common.js

_combined.maps.js: $(MAPS)
	cat $(MAPS)   | yui-compressor --type js -o _combined.maps.js


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
