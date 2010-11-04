COMMON=\
	Modernizr.js IE9.js yui-min.js \
	jquery-1.4.2.js jquery.ui-1.8.4.js \
	jquery.html5-0.0.1.js jquery.ui.stars-3.0.1.js \
	misc.js toggle_div.js url_encode.js

MAPS=\
	gears_init.js geo.js \
	OpenLayers.js

OUT=_combined.common.js _combined.maps.js

all: $(OUT)

clean:
	rm -f $(OUT)

_combined.common.js: $(COMMON)
	cat $(COMMON) | yui-compressor --type js -o _combined.common.js

_combined.maps.js: $(MAPS)
	cat $(MAPS)   | yui-compressor --type js -o _combined.maps.js
