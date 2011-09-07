
export PYTHONPATH := ../lib
export PGHOST     := localhost
export PGUSER     := civicboom
export PGPASSWORD := civicboom
export PGOPTIONS  := --client-min-messages=warning

GIT_TAG    := $(shell git describe)

help:
	# Usage: make <target>, where target is
	# site          -- the below (this should be done after git clone)
	#   i18n        -- compile the translations
	#   js          -- compress javascript into _combined.head.js and foot.js
	#   css         -- compress folders of css into single files
	#   ini         -- generate production / demo / test.ini files
	# sass          -- run a daemon to turn scss into css
	# test          -- run all nosetests
	# blank-db      -- create a blank database
	# test-db       -- create a blank database and fill it with test data
	# live-db       -- create a blank database and fill it with live data
	# run           -- run the site in development mode
	# clean         -- reset the folder to clean git checkout
	# schemadiff    -- write out sql to upgrade the live schema
	# help2         -- more commands (less frequently used)

help2:
	# cdnpush       -- push static files to CDN
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
	# run-demo      -- run in standalone demo mode - no internet needed
	# stopsys       -- stop the system cb-website and cb-worker
	# tv            -- compile telemetry DB


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

#         POT
#       /  |  \
#     /    |    \
# PO.en  PO.fr  PO.zh
#   |      |      |
# MO.en  MO.fr  MO.zh
#     \    |    /
#       \  |  /
#         All

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


##############################################################################
# static files

js:
	$(MAKE) -C civicboom/public/javascript

css:
	$(MAKE) -C civicboom/public/styles

sass:
	cd civicboom/public/styles
	sass --line-numbers --watch .:. >/tmp/sass.log 2>&1 &

# redirecting stdout means that the file is created even if the process fails.
# the mv on the second line only happens if it succeeds
%.ini: %.inidiff development.ini
	inipatch development.ini $< > $@.tmp && mv $@.tmp $@


##############################################################################
# testing

test:
	nosetests --verbose

test-coverage:
	nosetests --verbose --with-coverage --cover-erase --cover-html --cover-html-dir=./data/coverage/


##############################################################################
# database

# clean:
#   vanilla postgres install, no trace of civicboom
#
# empty:
#   user created
#   log database (with table)
#   main database (no tables, no postgis)
#
# blank-db:
#   add main tables from SQLAlchemy schema + postgis from source
#
# test-db:
#   add main tables + postgis from test snapshot
#
# live-db:
#   add main tables + postgis from live snapshot

db-clean:
	echo "DROP OWNED BY civicboom CASCADE" | sudo -u postgres psql -q || true
	sudo -u postgres dropdb civicboom || true
	sudo -u postgres dropdb civicboom_log || true
	sudo -u postgres dropdb civicboom_gis || true
	sudo -u postgres dropuser civicboom || true

db-empty: db-clean
	echo "create user civicboom with password '${PGPASSWORD}';" | sudo -u postgres psql -q
	sudo -u postgres createdb -E utf8 -O civicboom civicboom
	sudo -u postgres createdb -E utf8 -O civicboom civicboom_log
	#
	echo " \
		CREATE TABLE events( \
			id UUID PRIMARY KEY NOT NULL, \
			node VARCHAR(64) NOT NULL, \
			date_sent TIMESTAMP NOT NULL DEFAULT now(), \
			module VARCHAR(250) NOT NULL, \
			line_num INTEGER NOT NULL, \
			username VARCHAR(64) NOT NULL, \
			persona VARCHAR(64) NOT NULL, \
			url TEXT NOT NULL, \
			address INET NOT NULL, \
			priority INT NOT NULL, \
			message TEXT NOT NULL \
		); \
		CREATE INDEX events__date_sent ON events(date_sent); \
		CREATE INDEX events__module ON events(module); \
		CREATE INDEX events__username ON events(username); \
		CREATE INDEX events__priority ON events(priority); \
	" | psql -U civicboom -d civicboom_log -h localhost >/dev/null

test-db:
	if [ -f data/data-skel.pgdump ] ; \
	then $(MAKE) db-empty ; sudo -u postgres pg_restore -d civicboom < data/data-skel.pgdump ; \
	else $(MAKE) blank-db ; nosetests civicboom/tests/functional/test_stub.py || true ; sudo -u postgres pg_dump -Fc civicboom > data/data-skel.pgdump ; \
	fi

live-db:
	$(MAKE) db-empty
	ssh db1.civicboom.com sudo -u postgres pg_dump -Fc civicboom > data/data-live.pgdump
	sudo -u postgres pg_restore -d civicboom < data/data-live.pgdump

blank-db:
	$(MAKE) db-empty
	sudo -u postgres psql -q -d civicboom -f /usr/share/postgresql/9.0/contrib/postgis-1.5/postgis.sql
	sudo -u postgres psql -q -d civicboom -f /usr/share/postgresql/9.0/contrib/postgis-1.5/spatial_ref_sys.sql
	echo " \
		alter table spatial_ref_sys owner to civicboom; \
		alter table geometry_columns owner to civicboom; \
		alter view geography_columns owner to civicboom; \
	" | sudo -u postgres psql -q -d civicboom
	paster setup-app development.ini


##############################################################################
# run

run:
	paster serve --reload development.ini

run-demo:
	paster serve --reload demo.ini

run-worker:
	./cb-worker


##############################################################################
# CDN

cdnpush: js css ini
	echo removing cache breaker from icons.css
	sed -i "s/icons.png?ut=[0-9]*/icons.png/g" civicboom/public/styles/*.css
	../admin_scripts/upload-cdn-rs.py \
		--ini production.ini \
		--version ${GIT_TAG} \
		--exclude-file civicboom/public/cdn-exclude.txt \
		civicboom/public


##############################################################################
# other

clean: db-clean
	git clean -d -f -x

gource:
	cd .. && gource \
		-s 0.03 --auto-skip-seconds 0.1 --file-idle-time 500 --max-files 500 \
		--file-filter tiny_mce --highlight-all-users \
		--multi-sampling -1280x720 --stop-at-end --output-ppm-stream - | \
		ffmpeg -y -b 3000K -r 24 -f image2pipe -vcodec ppm -i - -vcodec mpeg4 gource.mp4

stats:
	python -m pstats ./data/prof.out

pep8:
	# 2XX = whitespace inside lines
	# 291 = whitespace-only line
	# 303 = too many blank lines
	# 501 = line too long
	pep8 -r --ignore=E2,E303,E501,W291 civicboom

civicboom/public/doc/index.html: ../docs/api.*.html civicboom/controllers/*.py
	mkdir -p civicboom/public/doc/
	../docs/gen_api_doc -i civicboom/controllers/ -t ../docs -o civicboom/public/doc/index.html

milestone-doc:
	../docs/gen_milestone_doc -s https://dev.civicboom.com/redmine/projects/civicboom/issues.json?query_id=6 -o ../docs/milestone.html

shell:
	paster shell

update.sql: civicboom/model/*.py
	pg_dump -U civicboom -h localhost -s civicboom > data/schema-dev.sql
	ssh db1.civicboom.com sudo -u postgres pg_dump -s civicboom > data/schema-live.sql
	java -jar ~/apgdiff-2.3/apgdiff-2.3.jar --add-transaction data/schema-live.sql data/schema-dev.sql > update.sql

stopsys:
	sudo initctl stop cb-website
	sudo initctl stop cb-worker

data/cbtv.db: data/cbtv.log
	../lib/cbutils/cbtv.py -i ./data/cbtv.log -d ./data/cbtv.db

tv: data/cbtv.db
	../lib/cbutils/cbtv.py -d ./data/cbtv.db


##############################################################################
# human readable aliases

api-doc: civicboom/public/doc/index.html

schemadiff: update.sql

ini: production.ini demo.ini test.ini

i18n: i18n-en

site: i18n js css api-doc ini
