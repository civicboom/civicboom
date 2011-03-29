
PYTHONPATH=../lib
GIT_TAG:=$(shell git describe)

help:
	# Usage: make <target>, where target is
	# site       -- i18n + js + css + libs (this should be done after git clone)
	# i18n       -- compile the translations
	# i18n-fr    -- generate a machine-translated french site
	# js         -- compress javascript into _combined.head.js and foot.js
	# css        -- compress folders of css into single files
	# test-db    -- create a blank database and fill it with test data
	# live-db    -- create a blank database and fill it with live data
	# run        -- run the site in development mode
	# clean      -- reset the folder to clean git checkout
	# gource     -- generate a video of developer activity
	# profile    -- run the test suite with profiling enabled (slow)
	# stats      -- run the interactive profile examiner
	# pep8       -- strict syntax checking
	# api-doc    -- build civicboom/public/api.html
	# libs       -- fetch external libraries
	# shell      -- python shell with the pylons environment loaded
	# cdnpush    -- push static files to CDN

site: i18n js css libs

i18n:
	python setup.py extract_messages
	#python setup.py update_catalog
	python setup.py init_catalog -l en
	../admin_scripts/site_to_english civicboom/i18n/en/LC_MESSAGES/civicboom.po
	python setup.py compile_catalog

i18n-fr: i18n
	curl \
		-F pofile=@civicboom/i18n/en/LC_MESSAGES/civicboom.po \
		-F language=fr \
		-F output=pofile  \
		--output civicboom/i18n/fr/LC_MESSAGES/civicboom.po \
		http://pepipopum.dixo.net
js:
	cd civicboom/public/javascript && $(MAKE)

css:
	cd civicboom/public/styles && $(MAKE)

skel-db:
	../admin_scripts/init_cbdb

test-db: skel-db
	paster setup-app development.ini
	nosetests

test:
	nosetests

data/live-data.pgdump:
	mkdir -p data
	ssh -C civicboom.com /opt/cb/bin/dump_db > data/live-data.pgdump

live-db: skel-db data/live-data.pgdump
	sudo -u postgres pg_restore -d civicboom data/live-data.pgdump

run:
	paster serve --reload development.ini

clean:
	git clean -d -f -x
	rm -f /tmp/prof.out

gource:
	gource \
		-s 0.03 --auto-skip-seconds 0.1 --file-idle-time 500 --max-files 500 \
		--file-filter tinymce --highlight-all-users \
		--multi-sampling -1280x720 --stop-at-end --output-ppm-stream - ../ | \
		ffmpeg -y -b 3000K -r 24 -f image2pipe -vcodec ppm -i - -vcodec mpeg4 gource.mp4

profile:
	time python -m cProfile -o /tmp/prof.out /usr/bin/nosetests

stats:
	python -m pstats /tmp/prof.out

pep8:
	# 2XX = whitespace inside lines
	# 293 = whitespace at end of line (warning only if blank line)
	# 301 = expected 1 blank line, found 0
	# 303 = too many blank lines
	# 501 = line too long
	# 701 = multiple statments one line (colons)
	pep8 -r --ignore=E2,E301,E303,E501,E701,W293 civicboom

api-doc:
	../admin_scripts/gendoc -i civicboom/controllers/ -t ../docs -o civicboom/public/api.html

py-libs:
	make -C ../lib

libs: py-libs

shell:
	paster shell

cdnpush: js css
	./bundle-static.py \
		--output static-${GIT_TAG}.zip \
		--exclude-file civicboom/public/cdn-exclude.txt \
		civicboom/public
	scp static-${GIT_TAG}.zip static.civicboom.com:~/
	ssh static.civicboom.com unzip -o static-${GIT_TAG}.zip -d /opt/cb/var/www/static/${GIT_TAG}
