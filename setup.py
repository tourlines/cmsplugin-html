from distutils.core import setup
import cmsplugin_html


setup(
    name=cmsplugin_html.__title__,
    author=cmsplugin_html.__author__,
    version=cmsplugin_html.__version__,
    packages=['cmsplugin_html', 'cmsplugin_javascript'],
    include_package_data=True,
    description='',
    author_email='rsoares@tourlines.com.br',
    url='https://github.com/tourlines/cmsplugin-html',
    download_url='https://github.com/tourlines/cmsplugin-html/archive/master.zip',
    keywords='',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django CMS',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
