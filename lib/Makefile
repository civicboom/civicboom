
all: magic.py pexif.py twitter formalchemy geoalchemy repoze

magic.py:
	wget --no-check-certificate https://github.com/ahupp/python-magic/raw/a75cf0a4a7790eb106155c947af9612f15693b6e/magic.py

pexif.py:
	wget http://pexif.googlecode.com/svn/trunk/pexif.py

twitter:
	wget http://pypi.python.org/packages/source/t/twitter/twitter-1.6.1.tar.gz
	tar xzf twitter-1.6.1.tar.gz
	mv twitter-1.6.1/twitter ./
	rm -rf twitter-1.6.1.tar.gz twitter-1.6.1

formalchemy:
	wget https://github.com/FormAlchemy/formalchemy/tarball/1.4 -O FormAlchemy-1.4.tar.gz
	tar xzf FormAlchemy-1.4.tar.gz
	mv FormAlchemy-formalchemy-67f7f90/formalchemy ./
	rm -rf formalchemy/tests
	rm -rf FormAlchemy-1.4.tar.gz FormAlchemy-formalchemy-67f7f90

geoalchemy:
	wget http://pypi.python.org/packages/source/G/GeoAlchemy/GeoAlchemy-0.5.tar.gz
	tar xzf GeoAlchemy-0.5.tar.gz
	mv GeoAlchemy-0.5/geoalchemy ./
	rm -rf geoalchemy/tests
	rm -rf GeoAlchemy-0.5.tar.gz GeoAlchemy-0.5
	patch -p0 geoalchemy/base.py < geoalchemy.pickle.patch

repoze:
	mkdir repoze
	wget https://raw.github.com/repoze/repoze.profile/master/repoze/profile/__init__.py -O repoze/__init__.py
	wget https://raw.github.com/repoze/repoze.profile/master/repoze/profile/profiler.py -O repoze/profiler.py
	wget https://raw.github.com/repoze/repoze.profile/master/repoze/profile/profiler.html -O repoze/profiler.html
	patch -p0 repoze/profiler.py < repoze.fixtag.patch

clean:
	rm -rf twitter formalchemy geoalchemy repoze
	rm -f *.py *.pyc *.tar.gz*
