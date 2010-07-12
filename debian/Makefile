all: cb-website.deb

# VERSION := 0.1.$(shell date +%Y%m%d.%H%M%S)
VERSION := $(shell git describe)

cb-website.deb: $(shell find ../admin_scripts ../debian ../nginx ../selenium ../src -type f | grep -vE "(fs-website)")
	rm -rf fs-website
	mkdir -p fs-website/DEBIAN/
	cp control fs-website/DEBIAN/control
	cp postinst fs-website/DEBIAN/postinst
	sed -i s/VERSION/${VERSION}/ fs-website/DEBIAN/control
	mkdir -p fs-website/opt/cb/bin
	cp ../admin_scripts/* ./fs-website/opt/cb/bin/
	mkdir -p fs-website/opt/cb/share/website
	cp -r ../src/* ./fs-website/opt/cb/share/website/
	mkdir -p fs-website/etc/nginx/sites-available/
	cp ../nginx/civicboom.com fs-website/etc/nginx/sites-available/
	mkdir -p fs-website/etc/cron.d
	cp crontab fs-website/etc/cron.d/cb-website
	mkdir -p fs-website/etc/init.d
	cp init.d fs-website/etc/init.d/cb-website
	mkdir -p fs-website/opt/cb/etc/ssl
	cp ../ssl/* fs-website/opt/cb/etc/ssl/
	fakeroot dpkg -b fs-website cb-website_${VERSION}_all.deb 
	ln -sf cb-website_${VERSION}_all.deb cb-website.deb


clean:
	rm -rf fs-* cb-*.deb 

