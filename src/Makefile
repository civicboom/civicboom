
export PYTHONPATH := ../lib
export PGHOST     := localhost
export PGUSER     := civicboom
export PGPASSWORD := civicboom

GIT_TAG    := $(shell git describe)

help:
	# Usage: make <target>, where target is
	# site          -- the three below (this should be done after git clone)
	#   i18n        -- compile the translations
	#   js          -- compress javascript into _combined.head.js and foot.js
	#   css         -- compress folders of css into single files
	# sass          -- run a daemon to turn scss into css
	# test          -- run all nosetests
	# test-db       -- create a blank database and fill it with test data
	# live-db       -- create a blank database and fill it with live data
	# run           -- run the site in development mode
	# clean         -- reset the folder to clean git checkout
	# schemadiff    -- write out sql to upgrade the live schema
	# help2         -- more commands (less frequently used)

help2:
	# cdnpush       -- push static files to CDN
	# libs          -- fetch external libraries
	# gource        -- generate a video of developer activity
	# stats         -- run the interactive profile examiner
	# pep8          -- strict syntax checking
	# i18n-fr       -- generate a machine-translated french site
	# api-doc       -- build civicboom/public/api.html
	# milestone-doc -- build /docs/milestone.html
	# shell         -- python shell with the pylons environment loaded
	# test-coverage -- run all nosetests and produce coverage html docs
	# test-profile  -- run the test suite with profiling enabled (slow)
	# run-worker    -- run a local worker
	# stopsys       -- stop the system cb-website and cb-worker


##############################################################################
# release

releasetest:
	git tag
	echo "What is the new release tag?"; read NEW_TAG; git checkout master && git pull && git checkout develop && git flow release start $$NEW_TAG && echo "git flow release finish $$NEW_TAG" && echo "git push origin master $$NEW_TAG"
	git checkout develop

release:
	git tag
	echo "What is the new release tag?"; read NEW_TAG; git checkout master && git pull && git checkout develop && git flow release start $$NEW_TAG && git flow release finish $$NEW_TAG && git push origin master $$NEW_TAG
	git checkout develop


##############################################################################
# i18n

# Phase 1: extract messages into template
civicboom/i18n/civicboom.pot: $(shell find -name "*.py" -or -name "*.mako")
	python setup.py extract_messages
	#python setup.py update_catalog

# Phase 2: convert template into translated files
civicboom/i18n/en/LC_MESSAGES/civicboom.po: civicboom/i18n/civicboom.pot
	python setup.py init_catalog -l en
	../admin_scripts/site_to_english civicboom/i18n/en/LC_MESSAGES/civicboom.po

civicboom/i18n/zh/LC_MESSAGES/civicboom.po: civicboom/i18n/civicboom.pot
	python setup.py init_catalog -l zh
	../admin_scripts/site_to_x civicboom/i18n/zh/LC_MESSAGES/civicboom.po

civicboom/i18n/fr/LC_MESSAGES/civicboom.po: civicboom/i18n/civicboom.pot
	python setup.py init_catalog -l fr
	curl \
		-F pofile=@civicboom/i18n/en/LC_MESSAGES/civicboom.po \
		-F language=fr \
		-F output=pofile  \
		--output civicboom/i18n/fr/LC_MESSAGES/civicboom.po \
		http://pepipopum.dixo.net

# Phase 3: compile translations
i18n-en: civicboom/i18n/en/LC_MESSAGES/civicboom.po
	python setup.py compile_catalog

i18n-fr: civicboom/i18n/fr/LC_MESSAGES/civicboom.po
	python setup.py compile_catalog

i18n-zh: civicboom/i18n/zh/LC_MESSAGES/civicboom.po
	python setup.py compile_catalog

i18n-all: civicboom/i18n/en/LC_MESSAGES/civicboom.po civicboom/i18n/fr/LC_MESSAGES/civicboom.po civicboom/i18n/zh/LC_MESSAGES/civicboom.po
	python setup.py compile_catalog

# shortcuts
i18n: i18n-en


##############################################################################
# static files

js:
	$(MAKE) -C civicboom/public/javascript

css:
	$(MAKE) -C civicboom/public/styles

sass:
	cd civicboom/public/styles
	sass --line-numbers --watch .:. >/tmp/sass.log 2>&1 &


##############################################################################
# testing

test:
	nosetests --verbose

test-coverage:
	nosetests --verbose --with-coverage --cover-erase --cover-html --cover-html-dir=../coverage/

test-profile:
	time python -m cProfile -o /tmp/prof.out /usr/bin/nosetests --verbose

data:
	mkdir -p data

data/skel-data.pgdump: civicboom/model/*.py data
	../admin_scripts/init_cbdb
	nosetests
	sudo -u postgres pg_dump -Fc civicboom > data/skel-data.pgdump

test-db: data/skel-data.pgdump
	sudo -u postgres pg_restore --clean -d civicboom < data/skel-data.pgdump

live-db: data/skel-data.pgdump
	mkdir -p data
	ssh db1.civicboom.com sudo -u postgres pg_dump -Fc civicboom > data/live-data.pgdump
	psql civicboom -c "truncate table spatial_ref_sys, geometry_columns;"
	sudo -u postgres pg_restore -d civicboom data/live-data.pgdump


##############################################################################
# run

run:
	paster serve --reload development.ini

run-worker:
	./cb-worker


##############################################################################
# CDN

cdnpush-ssh: js css
	echo removing cache breaker from icons.css
	sed -i "s/icons.png?ut=[0-9]*/icons.png/g" civicboom/public/styles/*.css
	../admin_scripts/upload-cdn-ssh.py \
		--ini production.ini \
		--version ${GIT_TAG} \
		--exclude-file civicboom/public/cdn-exclude.txt \
		civicboom/public

cdnpush-rs: js css
	echo removing cache breaker from icons.css
	sed -i "s/icons.png?ut=[0-9]*/icons.png/g" civicboom/public/styles/*.css
	../admin_scripts/upload-cdn-rs.py \
		--ini production.ini \
		--version ${GIT_TAG} \
		--exclude-file civicboom/public/cdn-exclude.txt \
		civicboom/public

cdnpush: cdnpush-rs


##############################################################################
# other

site: i18n js css api-doc

clean:
	git clean -d -f -x
	rm -f /tmp/prof.out

gource:
	cd .. && gource \
		-s 0.03 --auto-skip-seconds 0.1 --file-idle-time 500 --max-files 500 \
		--file-filter tiny_mce --highlight-all-users \
		--multi-sampling -1280x720 --stop-at-end --output-ppm-stream - | \
		ffmpeg -y -b 3000K -r 24 -f image2pipe -vcodec ppm -i - -vcodec mpeg4 gource.mp4

stats:
	python -m pstats /tmp/prof.out

pep8:
	# 2XX = whitespace inside lines
	# 291 = whitespace-only line
	# 303 = too many blank lines
	# 501 = line too long
	pep8 -r --ignore=E2,E303,E501,W291 civicboom

civicboom/public/doc/index.html: ../docs/api.*.html civicboom/controllers/*.py
	mkdir -p civicboom/public/doc/
	../docs/gen_api_doc -i civicboom/controllers/ -t ../docs -o civicboom/public/doc/index.html

api-doc: civicboom/public/doc/index.html

milestone-doc:
	../docs/gen_milestone_doc -s https://dev.civicboom.com/redmine/projects/civicboom/issues.json?query_id=6 -o ../docs/milestone.html

py-libs:
	$(MAKE) -C ../lib

libs: py-libs

shell:
	paster shell

schemadiff:
	pg_dump -U civicboom -h localhost -s civicboom > civicboom_dev.sql
	ssh db1.civicboom.com sudo -u postgres pg_dump -s civicboom > civicboom_live.sql
	java -jar ~/apgdiff-2.3/apgdiff-2.3.jar --add-transaction civicboom_live.sql civicboom_dev.sql > update.sql

stopsys:
	sudo initctl stop cb-website
	sudo initctl stop cb-worker
