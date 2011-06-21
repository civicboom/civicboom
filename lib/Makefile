
all: magic.py pexif.py twitter formalchemy geoalchemy

magic.py:
	wget --no-check-certificate https://github.com/ahupp/python-magic/raw/a75cf0a4a7790eb106155c947af9612f15693b6e/magic.py

pexif.py:
	wget http://pexif.googlecode.com/svn/trunk/pexif.py

twitter:
	wget http://pypi.python.org/packages/source/t/twitter/twitter-1.5.2.tar.gz
	tar xzf twitter-1.5.2.tar.gz
	mv twitter-1.5.2/twitter ./
	rm -rf twitter-1.5.2.tar.gz twitter-1.5.2

formalchemy:
	wget http://formalchemy.googlecode.com/files/FormAlchemy-1.3.3.tar.gz
	tar xzf FormAlchemy-1.3.3.tar.gz
	mv FormAlchemy-1.3.3/formalchemy ./
	rm -rf formalchemy/tests
	rm -rf FormAlchemy-1.3.3.tar.gz FormAlchemy-1.3.3

geoalchemy:
	wget http://pypi.python.org/packages/source/G/GeoAlchemy/GeoAlchemy-0.5.tar.gz
	tar xzf GeoAlchemy-0.5.tar.gz
	mv GeoAlchemy-0.5/geoalchemy ./
	rm -rf geoalchemy/tests
	rm -rf GeoAlchemy-0.5.tar.gz GeoAlchemy-0.5

clean:
	rm -rf magic.py twitter formalchemy geoalchemy
	rm -f *.py *.pyc *.tar.gz*
