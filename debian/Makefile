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

cb-website-api.deb: Makefile $(shell find ../admin_scripts ../docs ../selenium ../src ./api -type f)
	$(MAKE) -C ../src/ site
	rm -rf fs-api
	$(call mdcp, api/*                    , fs-api/DEBIAN/                   )
	$(call mdcp, api/cb-website.conf      , fs-api/etc/init/                 )
	$(call mdcp, api/cb-worker.conf       , fs-api/etc/init/                 )
	$(call mdcp, ../admin_scripts/cb-task , fs-api/opt/cb/bin/               )
	$(call mdcp, ../admin_scripts/nosete* , fs-api/opt/cb/bin/               )
	$(call mdcp, ../docs/*                , fs-api/opt/cb/share/doc/website/ )
	$(call mdcp, ../src/*                 , fs-api/opt/cb/share/website/     )
	$(call mdcp, ../src/production.ini    , fs-api/opt/cb/share/website-api/ )
	sed -i s/VERSION/${VERSION}/ fs-api/DEBIAN/control
	echo ${VERSION} > fs-api/opt/cb/share/website/.version
	fakeroot dpkg -b fs-api cb-website-api_${VERSION}_all.deb 
	ln -sf cb-website-api_${VERSION}_all.deb cb-website-api.deb

cb-website-web.deb: Makefile $(shell find ../nginx ./web)
	rm -rf fs-web
	$(call mdcp, web/*                          , fs-web/DEBIAN/                    )
	$(call mdcp, ../nginx/civicboom.com         , fs-web/etc/nginx/sites-available/ )
	$(call mdcp, ../nginx/errors                , fs-web/opt/cb/share/website-web/  )
	$(call mdcp, ../nginx/civicboom.com         , fs-web/opt/cb/share/website-web/  )
	$(call mdcp, ../nginx/ssl/wild.c*m.com.key  , fs-web/opt/cb/etc/ssl/            )
	cat ../nginx/ssl/wild.civicboom.com.crt ../nginx/ssl/rapidssl-ca.crt ../nginx/ssl/rapidssl-ca-cross.crt > fs-web/opt/cb/etc/ssl/wild.civicboom.com.pem
	sed -i s/VERSION/${VERSION}/ fs-web/DEBIAN/control
	fakeroot dpkg -b fs-web cb-website-web_${VERSION}_all.deb 
	ln -sf cb-website-web_${VERSION}_all.deb cb-website-web.deb

cb-website-db.deb: Makefile $(shell find ./db ../admin_scripts)
	rm -rf fs-db
	$(call mdcp, ../admin_scripts/init_cbdb      , fs-db/opt/cb/bin/   )
	$(call mdcp, ../admin_scripts/clean-sess*    , fs-db/opt/cb/bin/   )
	$(call mdcp, db/*                            , fs-db/DEBIAN/       )
	sed -i s/VERSION/${VERSION}/ fs-db/DEBIAN/control
	fakeroot dpkg -b fs-db cb-website-db_${VERSION}_all.deb 
	ln -sf cb-website-db_${VERSION}_all.deb cb-website-db.deb

python-cbmisc.deb: Makefile ../lib/Makefile ../lib/cbutils/
	rm -rf fs-env
	mkdir -p fs-env/DEBIAN/
	echo ================================================ >/dev/null
	echo "Package: python-cbmisc" > fs-env/DEBIAN/control
	echo "Version: ${VERSION}" >> fs-env/DEBIAN/control
	#echo "Architecture: $(shell dpkg-architecture -qDEB_BUILD_ARCH)" >> fs-env/DEBIAN/control
	echo "Architecture: all" >> fs-env/DEBIAN/control
	echo "Maintainer: Shish <shish@civicboom.com>" >> fs-env/DEBIAN/control
	echo "Depends: binutils" >> fs-env/DEBIAN/control
	echo "Description: a package with some non-debian-packaged python bits in" >> fs-env/DEBIAN/control
	echo ================================================ >/dev/null
	mkdir -p fs-env/usr/local/lib/python2.7/dist-packages
	$(MAKE) -C ../lib
	cp -r ../lib/* fs-env/usr/local/lib/python2.7/dist-packages/
	echo ================================================ >/dev/null
	fakeroot dpkg -b fs-env python-cbmisc_${VERSION}.deb
	ln -sf python-cbmisc_${VERSION}.deb python-cbmisc.deb

clean:
	rm -rf fs-* *.deb *.css *.js distribute*
	cd ../src/ && $(MAKE) clean
