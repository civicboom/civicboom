ALL=web.css widget.css mobile.css common/icons.css
TIMESTAMP := $(shell date +%s)

all: $(ALL)
	cp */*.png ./

clean:
	rm -f $(ALL) *.png */*.css

common/icons.css: common/icons/*
	iconmapper -q -c common/icons.css -p icons.png -a icons.png?ut=${TIMESTAMP} common/icons/*
	cp icons.png common/

web.css:    common/*.scss  common/icons.css  web/*.scss     Makefile
	sass --scss --update .:.
	cat common/*.css web/*.css | yui-compressor --type css -o web.css

widget.css: common/yui-3.2.0-reset-fonts.scss  common/icons.css  widget/*.scss  Makefile
	sass --scss --update .:.
	cat common/yui-3.2.0-reset-fonts.css common/icons.css widget/*.css | yui-compressor --type css -o widget.css

mobile.css: common/*.scss  common/icons.css  mobile/*.scss  Makefile
	sass --scss --update .:.
	cat common/*.css mobile/*.css | yui-compressor --type css -o mobile.css

