try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
import os

setup(
    name='civicboom',
    version=os.popen('git describe').read(),
    description='',
    author='',
    author_email='',
    url='',
    # IMPORTANT NOTE: the package build script does magic with the next few
    # lines of text -- the first array is packages which need to be fetched
    # from the python package index, the second array is packages which are
    # supplied by debian
    install_requires=[
        "python_magic",
        "FormAlchemy",
        "GeoAlchemy",
        "twitter>=1.4.2",
    ] + [
        "SQLAlchemy>=0.6.5", # debian experimental has 0.6.6
        "Pylons>=1.0.0",     # debian experimental
        "Mako>=0.3.4",       # debian experimental has 0.3.6
        #"recaptcha-client", # AllanC - I wrote our own one out of frustration, turned out to be the validator triggering twice :(
        #"GeoFormAlchemy",   # now using a custom geometry renderer with our own location picker component
        "pyDNS",
        "python_memcached",
        "boto",
        "Babel",
        "PIL",
    ],

    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'civicboom': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors={'civicboom': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
            ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = civicboom.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
