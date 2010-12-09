all: cb-website.deb cb-website-web.deb cb-website-api.deb cb-website-db.deb python-cbmisc.deb

VERSION := $(shell git describe)

cb-website.deb: cb-website-web.deb cb-website-api.deb cb-website-db.deb
	mkdir -p fs-meta/DEBIAN/
	echo ================================================ >/dev/null
	echo "Package: cb-website" > fs-meta/DEBIAN/control
	echo "Version: ${VERSION}" >> fs-meta/DEBIAN/control
	echo "Architecture: all" >> fs-meta/DEBIAN/control
	echo "Maintainer: Shish <shish@civicboom.com>" >> fs-meta/DEBIAN/control
	echo "Depends: cb-website-web(>=0.3.34-3), cb-website-api(>=0.3.34-7), cb-website-db(>=0.3.34-6)" >> fs-meta/DEBIAN/control
	echo "Description: a metapackage to get the whole civicboom server" >> fs-meta/DEBIAN/control
	echo ================================================ >/dev/null
	fakeroot dpkg -b fs-meta cb-website_${VERSION}_all.deb
	ln -sf cb-website_${VERSION}_all.deb cb-website.deb

cb-website-api.deb: $(shell find ../admin_scripts ../docs ../selenium ../src -type f)
	rm -rf fs-api
	mkdir -p fs-api/DEBIAN/
	cp api/* fs-api/DEBIAN/
	sed -i s/VERSION/${VERSION}/ fs-api/DEBIAN/control
	mkdir -p fs-api/opt/cb/bin
	cp ../admin_scripts/* ./fs-api/opt/cb/bin/
	mkdir -p fs-api/opt/cb/share/doc/website
	cp -r ../docs/* ./fs-api/opt/cb/share/doc/website/
	mkdir -p fs-api/opt/cb/share/website
	cp -r ../src/* ./fs-api/opt/cb/share/website/
	cd ./fs-api/opt/cb/share/website/ && python setup.py compile_catalog
	mkdir -p fs-api/etc/cron.d
	cp api/crontab fs-api/etc/cron.d/cb-website-api
	mkdir -p fs-api/etc/init.d
	cp api/init.d fs-api/etc/init.d/cb-website
	cd fs-api/opt/cb/share/website/civicboom/public/javascript/ && make
	cd fs-api/opt/cb/share/website/civicboom/public/styles/ && make
	../admin_scripts/site_to_english ../src/civicboom/i18n/en/LC_MESSAGES/civicboom.po
	fakeroot dpkg -b fs-api cb-website-api_${VERSION}_all.deb 
	ln -sf cb-website-api_${VERSION}_all.deb cb-website-api.deb

cb-website-web.deb: $(shell find ../nginx)
	rm -rf fs-web
	mkdir -p fs-web/DEBIAN
	cp web/* fs-web/DEBIAN/
	sed -i s/VERSION/${VERSION}/ fs-web/DEBIAN/control
	mkdir -p fs-web/etc/nginx/sites-available/
	cp ../nginx/civicboom.com fs-web/etc/nginx/sites-available/
	mkdir -p fs-web/opt/cb/etc/ssl
	cp ../ssl/* fs-web/opt/cb/etc/ssl/
	fakeroot dpkg -b fs-web cb-website-web_${VERSION}_all.deb 
	ln -sf cb-website-web_${VERSION}_all.deb cb-website-web.deb

cb-website-db.deb: $(shell find db)
	rm -rf fs-db
	mkdir -p fs-db/DEBIAN
	cp db/* fs-db/DEBIAN/
	mkdir -p fs-db/etc/cron.d
	cp db/crontab fs-db/etc/cron.d/cb-website-db
	sed -i s/VERSION/${VERSION}/ fs-db/DEBIAN/control
	fakeroot dpkg -b fs-db cb-website-db_${VERSION}_all.deb 
	ln -sf cb-website-db_${VERSION}_all.deb cb-website-db.deb

python-cbmisc.deb: ../src/setup.py
	mkdir -p fs-env/DEBIAN/
	echo ================================================ >/dev/null
	echo "Package: python-cbmisc" > fs-env/DEBIAN/control
	echo "Version: ${VERSION}" >> fs-env/DEBIAN/control
	echo "Architecture: all" >> fs-env/DEBIAN/control
	echo "Maintainer: Shish <shish@civicboom.com>" >> fs-env/DEBIAN/control
	echo "Depends: binutils" >> fs-env/DEBIAN/control
	echo "Description: a package to install a python virtualenv and easy_install packages into it" >> fs-env/DEBIAN/control
	echo ================================================ >/dev/null
	mkdir -p fs-env/opt/cb
	virtualenv fs-env/opt/cb
	./fs-env/opt/cb/bin/easy_install $(shell python helper.py find_packages)
	mkdir -p ./fs-env/usr/lib/python2.6/dist-packages/
	cat fs-env/opt/cb/lib/python2.6/site-packages/easy-install.pth | \
		sed "s#./#/opt/cb/lib/python2.6/site-packages/#" \
		> fs-env/usr/lib/python2.6/dist-packages/cbmisc.pth
	echo ================================================ >/dev/null
	fakeroot dpkg -b fs-env python-cbmisc_${VERSION}.deb
	ln -sf python-cbmisc_${VERSION}.deb python-cbmisc.deb

clean:
	rm -rf fs-* *.deb *.css *.js distribute*

