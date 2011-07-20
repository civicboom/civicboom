ALL=web.css widget.css mobile.css common/icons.scss
TIMESTAMP := $(shell date +%s)

all: $(ALL)
	cp */*.png ./
	cp *.*.svg ./

clean:
	rm -f $(ALL) *.png */*.css

common/icons.scss: common/icons/*
	iconmapper -q -c common/icons.scss -p icons.png -a icons.png?ut=${TIMESTAMP} common/icons/*
	cp icons.png common/

web.css:    common/*.scss  common/icons.scss  web/*.scss     Makefile
	ls -1 common/*.scss web/*.scss | sed 's/\(.*\)/@import "\1";/' | sass --stdin --scss --style compressed web.css

widget.css: common/yui-3.2.0-reset-fonts.scss  common/icons.scss  widget/*.scss  Makefile
	ls -1 common/yui-3.2.0-reset-fonts.scss common/icons.scss widget/*.scss | sed 's/\(.*\)/@import "\1";/' | sass --stdin --scss --style compressed widget.css

mobile.css: common/*.scss  common/icons.scss  mobile/*.scss  Makefile
	ls -1 common/*.scss mobile/*.scss | sed 's/\(.*\)/@import "\1";/' | sass --stdin --scss --style compressed mobile.css
