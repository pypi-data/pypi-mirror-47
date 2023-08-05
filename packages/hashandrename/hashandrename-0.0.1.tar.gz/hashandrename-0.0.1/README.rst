This module is used to hash a set of files and rename them such that the
hashes are embedded in their filenames.

Usage:

``python -m hashandrename filea.txt fileb.txt --rename --hashalg md5``

will generate the files

``filea_md5_[md5hash].txt`` and ``filea_md5_[md5hash].txt``.
