ALL=web.css widget.css mobile.css common/icons.css

all: $(ALL)

clean:
	rm -f $(ALL)

common/icons.css: common/icons/*
	iconmapper -c common/icons.css -p icons.png common/icons/*
	cp icons.png common/icons.png

web.css:    common/*.css  common/icons.css  web/*.css     Makefile
	cat common/*.css web/*.css    | yui-compressor --type css -o web.css

widget.css: common/*.css  common/icons.css  widget/*.css  Makefile
	cat common/*.css widget/*.css | yui-compressor --type css -o widget.css

mobile.css: common/*.css  common/icons.css  mobile/*.css  Makefile
	cat common/*.css mobile/*.css | yui-compressor --type css -o mobile.css

