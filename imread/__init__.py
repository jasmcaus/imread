from __future__ import print_function
try:
    from .imread import imread, imwrite, imread_multi, imread_from_blob, imwrite_multi
    from .imread import detect_format, supports_format
    from .imread import imload, imsave, imload_multi, imload_from_blob, imsave_multi
    from .imread_version import __version__
except ImportError as e:
    import sys
    print('''\
Could not import submodules (exact error was: {0}).

There are many reasons for this error the most common one is that you have
either not built the packages or have built (using `python setup.py build`) or
installed them (using `python setup.py install`) and then proceeded to test
mahotas-imread **without changing the current directory**.

Try installing and then changing to another directory before importing mahotas.
'''.format(e), file=sys.stderr)

