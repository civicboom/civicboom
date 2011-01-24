
help:
	# Usage: make <target>, where target is
	# site       -- i18n + js + css  (this should be done after git clone)
	# i18n       -- compile the translations
	# js         -- compress javascript into _combined.head.js and foot.js
	# css        -- compress folders of css into single files
	# test-db    -- create a blank database and fill it with test data
	# live-db    -- create a blank database and fill it with live data
	# run        -- run the site in development mode
	# clean      -- reset the folder to clean git checkout

site: i18n js css

i18n:
	python setup.py extract_messages
	#python setup.py update_catalog
	python setup.py init_catalog -l en
	../admin_scripts/site_to_english civicboom/i18n/en/LC_MESSAGES/civicboom.po
	python setup.py compile_catalog

js:
	cd civicboom/public/javascript && $(MAKE)

css:
	cd civicboom/public/styles && $(MAKE)

skel-db:
	../admin_scripts/init_cbdb

test-db: skel-db
	paster setup-app development.ini
	nosetests

data/live-data.sql:
	mkdir -p data
	ssh -C civicboom.com /opt/cb/bin/dump_db > data/live-data.sql

live-db: skel-db data/live-data.sql
	sudo -u postgres psql -q -f data/live-data.sql

run:
	paster serve --reload development.ini

clean:
	git clean -d -f -x
