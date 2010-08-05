all: cb-website.deb python-cbmisc.deb

VERSION := $(shell git describe)

# try and read dependencies from setup.py
# this is full of magic because grep sucks at handling newline characters
# the aim is to input setup.py, and output eg --> "Mako>=0.3.4" "gp.fileupload" "GeoFormAlchemy"
EASY_INSTALL_PACKAGES := $(shell python -c "import re;print re.sub('[ \n]','',re.match('.*install_requires=\[([^]]*)\].*',file('../src/setup.py').read(),re.DOTALL).group(1)).replace(',', ' ')")

cb-website.deb: $(shell find ../admin_scripts ../nginx ../selenium ../src -type f) _combined.js _combined.css
	rm -rf fs-website
	mkdir -p fs-website/DEBIAN/
	cp control fs-website/DEBIAN/control
	cp postinst fs-website/DEBIAN/postinst
	sed -i s/VERSION/${VERSION}/ fs-website/DEBIAN/control
	mkdir -p fs-website/opt/cb/bin
	cp ../admin_scripts/* ./fs-website/opt/cb/bin/
	mkdir -p fs-website/opt/cb/share/website
	cp -r ../src/* ./fs-website/opt/cb/share/website/
	cd ./fs-website/opt/cb/share/website/ && python setup.py compile_catalog
	mkdir -p fs-website/etc/nginx/sites-available/
	cp ../nginx/civicboom.com fs-website/etc/nginx/sites-available/
	mkdir -p fs-website/etc/cron.d
	cp crontab fs-website/etc/cron.d/cb-website
	mkdir -p fs-website/etc/init.d
	cp init.d fs-website/etc/init.d/cb-website
	mkdir -p fs-website/opt/cb/etc/ssl
	cp ../ssl/* fs-website/opt/cb/etc/ssl/
	cp _combined.js fs-website/opt/cb/share/website/civicboom/public/javascript/
	cp _combined.css fs-website/opt/cb/share/website/civicboom/public/styles/design09/
	fakeroot dpkg -b fs-website cb-website_${VERSION}_all.deb 
	ln -sf cb-website_${VERSION}_all.deb cb-website.deb

_combined.js: ../src/civicboom/public/javascript/[a-z]*.js ../src/civicboom/templates/web/html_header.mako
	( \
		cat ../src/civicboom/public/javascript/[a-z]*.js && \
		curl `cat ../src/civicboom/templates/web/html_header.mako | grep -oE "http.*\.js"` \
	) | yui-compressor --type js > _combined.js

_combined.css: ../src/civicboom/public/styles/design09/design09_*.css ../src/civicboom/templates/web/html_header.mako
	( \
		cat ../src/civicboom/public/styles/design09/design09_*.css && \
		curl `cat ../src/civicboom/templates/web/html_header.mako | grep -oE "http.*\.css"` \
	) | yui-compressor --type css > _combined.css

python-cbmisc.deb: ../src/setup.py
	mkdir -p fs-env/DEBIAN/
	echo ================================================ >/dev/null
	echo "Package: python-cbmisc" > fs-env/DEBIAN/control
	echo "Version: ${VERSION}" >> fs-env/DEBIAN/control
	echo "Architecture: all" >> fs-env/DEBIAN/control
	echo "Maintainer: Shish <shish@civicboom.com>" >> fs-env/DEBIAN/control
	echo "Description: a package to install a python virtualenv and easy_install packages into it" >> fs-env/DEBIAN/control
	echo ================================================ >/dev/null
	mkdir -p fs-env/opt/cb
	virtualenv fs-env/opt/cb
	./fs-env/opt/cb/bin/easy_install ${EASY_INSTALL_PACKAGES}
	mkdir -p ./fs-env/usr/lib/python2.6/dist-packages/
	cat fs-env/opt/cb/lib/python2.6/site-packages/easy-install.pth | \
		sed "s#./#/opt/cb/lib/python2.6/site-packages/#" \
		> fs-env/usr/lib/python2.6/dist-packages/cbmisc.pth
	echo ================================================ >/dev/null
	fakeroot dpkg -b fs-env python-cbmisc_${VERSION}.deb
	ln -sf python-cbmisc_${VERSION}.deb python-cbmisc.deb

clean:
	rm -rf fs-* *.deb _combined.* distribute*

