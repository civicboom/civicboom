
all: i18n js css

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

init-db:
	../admin_scripts/init_cbdb
	paster setup-app development.ini
	nosetests

pull-data:
	ssh -C civicboom.com /opt/cb/bin/dump_db > live-data.sql
	PGPASSWORD=civicboom psql -U civicboom -h localhost < live-data.sql
