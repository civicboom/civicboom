ALL=web.css widget.css mobile.css

all: $(ALL)

clean:
	rm -f $(ALL)

web.css:    common/*.css  web/*.css     Makefile
	cat common/*.css web/*.css    | yui-compressor --type css -o web.css

widget.css: common/*.css  widget/*.css  Makefile
	cat common/*.css widget/*.css | yui-compressor --type css -o widget.css

mobile.css: common/*.css  mobile/*.css  Makefile
	cat common/*.css mobile/*.css | yui-compressor --type css -o mobile.css

