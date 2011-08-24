
all: $(shell ls -1 | sed "s#\(.*\).rst#html/\1.html#")

html/%.html: %.rst
	mkdir -p html
	rst2html $< $@
