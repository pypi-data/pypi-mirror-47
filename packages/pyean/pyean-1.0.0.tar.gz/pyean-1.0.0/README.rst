pyean
==============

This library is modification for python-barcode only for ean13.
Credits for https://github.com/WhyNotHugo/python-barcode/issues



Requirements
------------

- Setuptools/distribute for installation.
- Python 3.5 or above
- Program to open SVG objects (your browser should do it)
- Optional: Pillow to render barcodes as images (PNG, JPG, ...)


Installation
------------

The best way is to use pip: ``pip install pyean``.

You can also install manually by downloading the tarball, extracting it, and
running ``python setup.py install``.


Provided Barcodes
-----------------


* EAN-13


Usage
-----

USAGE::

    import barcode
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN('5901234123457', "Label Text")
    fullname = ean.save('ean13_barcode')

Now open ean13_barcode.[svg|png] in a graphic app or simply in your browser
and see the created barcode. That's it.

Commandline::

    $ python-barcode create "My Text" outfile
    New barcode saved as outfile.svg.
    $ python-barcode create -t png "My Text" outfile
    New barcode saved as outfile.png.

    Try `python-barcode -h` for help.

Changelog
---------

v0.001
~~~~
* First release.
