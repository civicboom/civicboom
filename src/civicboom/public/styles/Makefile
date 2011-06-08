ALL=web.css widget.css mobile.css common/icons.css
TIMESTAMP := $(shell date +%s)

all: $(ALL)
	cp */*.png ./

clean:
	rm -f $(ALL) *.png

common/icons.css: common/icons/*
	iconmapper -q -c common/icons.css -p icons.png -a icons.png?ut=${TIMESTAMP} common/icons/*
	cp icons.png common/

web.css:    common/*.css  common/icons.css  web/*.css     Makefile
	sass --scss --update .:.
	cat common/*.css web/*.css | yui-compressor --type css -o web.css

widget.css: common/yui-3.2.0-reset-fonts.css  common/icons.css  widget/*.css  Makefile
	sass --scss --update .:.
	cat common/yui-3.2.0-reset-fonts.css common/icons.css widget/*.css | yui-compressor --type css -o widget.css

mobile.css: common/*.css  common/icons.css  mobile/*.css  Makefile
	sass --scss --update .:.
	cat common/*.css mobile/*.css | yui-compressor --type css -o mobile.css

