# Copyright 2020 The Caer Authors. All Rights Reserved.
#
# Licensed under the MIT License (see LICENSE);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at <https://opensource.org/licenses/MIT>
#
# ==============================================================================

from glob import glob
import platform
import sys
import setuptools
import os
from caerimread import __version__

from setuptools.command.build_ext import build_ext as _build_ext
# Based on http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

def has_webp():
    return os.system("pkg-config --exists libwebp") == 0

exec(compile(open('caerimread/version.py').read(),
             'caerimread/version.py', 'exec'))
long_description = open('README.md').read()

undef_macros = []
define_macros = []
if os.environ.get('DEBUG'):
    undef_macros = ['NDEBUG']
    if os.environ.get('DEBUG') == '2':
        define_macros.append( ('_GLIBCXX_DEBUG','1') )
define_macros.append(('NPY_NO_DEPRECATED_API','NPY_1_7_API_VERSION'))
define_macros.append(('PY_ARRAY_UNIQUE_SYMBOL','CaerImread_PyArray_API_Symbol'))


EXCLUDE_WEBP = os.environ.get('EXCLUDE_WEBP')
if EXCLUDE_WEBP is None:
    EXCLUDE_WEBP = not has_webp()

if EXCLUDE_WEBP:
    define_macros.append( ('IMREAD_EXCLUDE_WEBP', '1') )

include_dirs = []
library_dirs = []

for pth in ('/usr/local/include', '/usr/X11/include'):
    if os.path.isdir(pth):
        include_dirs.append(pth)

for pth in ('/usr/local/lib', '/usr/X11/lib'):
    if os.path.isdir(pth):
        library_dirs.append(pth)

extensions = {
    'caerimread.cimread': [
        'caerimread/cimread.cpp',
        'caerimread/includes/formats.cpp',
        'caerimread/includes/numpy.cpp',
        'caerimread/includes/cbmp.cpp',
        'caerimread/includes/cjpeg.cpp',
        'caerimread/includes/clsm.cpp',
        'caerimread/includes/cpng.cpp',
        'caerimread/includes/ctiff.cpp',
        ],
}


libraries = ['png', 'jpeg', 'tiff']
if sys.platform.startswith('win'):
    libraries.append('zlib')

if not EXCLUDE_WEBP:
    extensions['imread.cimread'].append('imread/includes/cwebp.cpp')
    libraries.append('webp')

extra_args = []
if platform.platform().startswith('Darwin'):
    if int(platform.mac_ver()[0].split('.')[1]) >= 9:
        extra_args.append('-stdlib=libc++')

ext_modules = [
    setuptools.Extension(
        key,
        libraries = libraries,
        library_dirs=library_dirs,
        include_dirs=include_dirs,
        sources=sources,
        undef_macros=undef_macros,
        define_macros=define_macros,
        extra_compile_args=extra_args,
        extra_link_args=extra_args,
        ) for key, sources in extensions.items()]

packages = setuptools.find_packages()


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Multimedia',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: C++',
    'License :: OSI Approved :: MIT License'
]

if __name__ == '__main__':
    setuptools.setup(
        name = 'caerimread',
        version = __version__,
        description = 'imread: Image reading library',
        long_description = long_description,
        long_description_content_type = 'text/x-rst',
        author = 'Jason Dsouza',
        author_email = 'jasmcaus@gmail.com',
        license = 'MIT',
        platforms = ['Any'],
        classifiers = classifiers,
        url = 'https://github.com/jasmcaus/imread',
        packages = packages,
        ext_modules = ext_modules,
        cmdclass = {'build_ext': build_ext},
        setup_requires = ['numpy'],
        install_requires = ['numpy'],
    )
