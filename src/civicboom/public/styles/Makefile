ALL=web.css widget.css mobile.css
TIMESTAMP := $(shell date +%s)

all: $(ALL)
	cp */*.png ./
	cp */*.svg ./

clean:
	rm -f $(ALL) *.png */*.css

common/_icons.scss: common/icons/*
	iconmapper -q -c common/_icons.scss -p icons.png -a icons.png?ut=${TIMESTAMP} common/icons/*
	pngcrush icons.png common/icons.png

web.scss:    common/*.scss  common/_icons.scss  web/*.scss     Makefile
	ls -1 common/*.scss web/*.scss | sed 's/\(.*\)/@import "\1";/' > web.scss

widget.scss: common/_yui-3.2.0-reset-fonts.scss  common/_icons.scss  widget/*.scss  Makefile
	ls -1 common/_yui-3.2.0-reset-fonts.scss common/_icons.scss widget/*.scss | sed 's/\(.*\)/@import "\1";/' > widget.scss

mobile.scss: common/_yui-3.2.0-reset-fonts.scss  mobile/*.scss  Makefile
	ls -1 common/_yui-3.2.0-reset-fonts.scss mobile/*.scss | sed 's/\(.*\)/@import "\1";/' > mobile.scss

%.css: %.scss
	sass --style compressed $< $@
