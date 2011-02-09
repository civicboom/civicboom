all: cb-website.deb python-cbmisc.deb

VERSION := $(shell git describe)

mdcp   = mkdir -p $(2) && cp -r $(1) $(2)$(3)
getver = dpkg-deb --info cb-website-$(1).deb | grep "Version: " | cut -d " " -f 3

cb-website.deb: cb-website-web.deb cb-website-api.deb cb-website-db.deb
	mkdir -p fs-meta/DEBIAN/
	echo ================================================ >/dev/null
	echo "Package: cb-website" > fs-meta/DEBIAN/control
	echo "Version: ${VERSION}" >> fs-meta/DEBIAN/control
	echo "Architecture: all" >> fs-meta/DEBIAN/control
	echo "Maintainer: Shish <shish@civicboom.com>" >> fs-meta/DEBIAN/control
	echo "Depends: cb-website-web(>=$(shell $(call getver,web))), " >> fs-meta/DEBIAN/control
	echo "         cb-website-api(>=$(shell $(call getver,api))), " >> fs-meta/DEBIAN/control
	echo "         cb-website-db(>=$(shell $(call getver,db)))"     >> fs-meta/DEBIAN/control
	echo "Description: a metapackage to get the whole civicboom server" >> fs-meta/DEBIAN/control
	echo ================================================ >/dev/null
	fakeroot dpkg -b fs-meta cb-website_${VERSION}_all.deb
	ln -sf cb-website_${VERSION}_all.deb cb-website.deb

cb-website-api.deb: $(shell find ../admin_scripts ../docs ../selenium ../src -type f)
	cd ../src/ && $(MAKE) site
	rm -rf fs-api
	$(call mdcp, api/*              , fs-api/DEBIAN/                   )
	$(call mdcp, api/crontab        , fs-api/etc/cron.d/,cb-website-web )
	$(call mdcp, api/init.d         , fs-api/etc/init.d/,cb-website     )
	$(call mdcp, ../admin_scripts/* , fs-api/opt/cb/bin/               )
	$(call mdcp, ../docs/*          , fs-api/opt/cb/share/doc/website/ )
	$(call mdcp, ../src/*           , fs-api/opt/cb/share/website/     )
	sed -i s/VERSION/${VERSION}/ fs-api/DEBIAN/control
	fakeroot dpkg -b fs-api cb-website-api_${VERSION}_all.deb 
	ln -sf cb-website-api_${VERSION}_all.deb cb-website-api.deb

cb-website-web.deb: $(shell find ../nginx)
	rm -rf fs-web
	$(call mdcp, web/*                         , fs-web/DEBIAN/                    )
	$(call mdcp, ../nginx/civicboom.com        , fs-web/etc/nginx/sites-available/ )
	$(call mdcp, ../ssl/wild.civicboom.com.key , fs-web/opt/cb/etc/ssl/            )
	cat ../ssl/wild.civicboom.com.crt ../ssl/rapidssl-ca.crt > fs-web/opt/cb/etc/ssl/wild.civicboom.com.pem
	sed -i s/VERSION/${VERSION}/ fs-web/DEBIAN/control
	fakeroot dpkg -b fs-web cb-website-web_${VERSION}_all.deb 
	ln -sf cb-website-web_${VERSION}_all.deb cb-website-web.deb

cb-website-db.deb: $(shell find db)
	rm -rf fs-db
	$(call mdcp, db/*       , fs-db/DEBIAN/                    )
	$(call mdcp, db/crontab , fs-db/etc/cron.d/,cb-website-db  )
	sed -i s/VERSION/${VERSION}/ fs-db/DEBIAN/control
	fakeroot dpkg -b fs-db cb-website-db_${VERSION}_all.deb 
	ln -sf cb-website-db_${VERSION}_all.deb cb-website-db.deb

python-cbmisc.deb: ../src/setup.py
	mkdir -p fs-env/DEBIAN/
	echo ================================================ >/dev/null
	echo "Package: python-cbmisc" > fs-env/DEBIAN/control
	echo "Version: ${VERSION}" >> fs-env/DEBIAN/control
	echo "Architecture: $(shell dpkg-architecture -qDEB_BUILD_ARCH)" >> fs-env/DEBIAN/control
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

