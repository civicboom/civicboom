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
    install_requires=[
        # for a full list of dependencies, see
        # - debian/api/control (for packaged things)
        # - lib/ (for things bundled into python-cbmisc)
        "SQLAlchemy",
        "Pylons",
        "Mako",
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
