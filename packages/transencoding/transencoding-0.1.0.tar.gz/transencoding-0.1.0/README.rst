transencoding
=============

Convert encoding of given file from one encoding to another.

Install
-------

::

    pip install transencoding


Usage
-----

::

    E:\transencoding>python transencoding.py --help
    Usage: transencoding.py [OPTIONS] [INPUT]

    Options:
    -f, --from-code TEXT  Encoding of original text  [required]
    -t, --to-code TEXT    encoding for output  [required]
    -o, --output TEXT     output file
    --help                Show this message and exit.

Example
-------


将utf8.txt中的utf8编码的文本转化为gbk编码，并保存到gbk.txt文件中。

::

    E:\transencoding>python transencoding.py -f utf8 -t gbk utf8.txt > gbk.txt

