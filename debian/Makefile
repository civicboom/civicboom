all: cb-website.deb

# VERSION := 0.1.$(shell date +%Y%m%d.%H%M%S)
VERSION := $(shell git describe)

cb-website.deb: $(shell find ../admin_scripts ../apache ../debian ../downtime ../selenium ../src -type f)
	rm -rf fs-website
	mkdir -p fs-website/DEBIAN/
	cp control fs-website/DEBIAN/control
	cp postinst fs-website/DEBIAN/postinst
	sed -i s/VERSION/${VERSION}/ fs-website/DEBIAN/control
	mkdir -p fs-website/opt/cb/bin
	cp ../admin_scripts/* ./fs-website/opt/cb/bin/
	mkdir -p fs-website/opt/cb/share/website
	cp -r ../src/* ./fs-website/opt/cb/share/website/
	mkdir -p fs-website/opt/cb/share/downtime/
	cp ../downtime/* fs-website/opt/cb/share/downtime/
	mkdir -p fs-website/etc/apache2/sites-available/
	cp ../apache/civicboom.com-* fs-website/etc/apache2/sites-available/
	mkdir -p fs-website/etc/cron.d/
	cp crontab fs-website/etc/cron.d/cb-website
	fakeroot dpkg -b fs-website cb-website_${VERSION}.deb 
	ln -sf cb-website_${VERSION}.deb cb-website.deb


clean:
	rm -rf fs-* cb-*.deb 

