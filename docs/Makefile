
all: $(shell ls -1 | sed "s#\(.*\).rst#html/\1.html#")

html/all.html: *.rst
	( \
	    for n in *.rst ; do cat $$n && echo && echo ; done \
	) | rst2html > html/all.html

html:
	mkdir -p html

html/%.html: %.rst html
	rst2html $< $@

clean:
	rm -rf html
