HEAD    := $(shell find head   -name "*.js" | sort)
FOOT    := $(shell find foot   -name "*.js" | sort)
MOBILE  := $(shell find mobile -name "*.js" | sort)

all: _combined.head.js _combined.foot.js _combined.mobile.js

_combined.head.js: Makefile $(HEAD)
	cat $(HEAD) | yui-compressor --type js -o _combined.head.js

_combined.foot.js: Makefile $(FOOT)
	cat $(FOOT) | yui-compressor --type js -o _combined.foot.js

_combined.mobile.js: Makefile $(MOBILE)
	cat $(MOBILE) | yui-compressor --type js -o _combined.mobile.js

clean:
	rm -f _combined.*.js


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
