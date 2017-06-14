argdown
=======

Argdown is an extension to Python’s argparse_ module that adds Markdown
documentation export.

The argparse module is great at generating command-line usage and help texts,
but pasting pre-formatted and indented terminal output into a ``readme.md`` is
quite ugly. argdown is a python module that provides a function
``argdown.md_help(parser)`` that accepts an ``ArgumentParser`` object and
returns a string of lovely help text.

Argdown requires a fully formed ArgumentParser object, after all the
add_argument()s have been executed. The only way to make sure the
ArgumentParser object is created in the same way that it would be during normal
script execution is to execute the script until the arguments are parsed. To do
this, argdown reads the input file(s) until it reads a line containing
``.parse_args(``. The rest of the file, being irrelevant to the command-line
invocation, is truncated, and a call to ``argdown.md_help()`` is inserted to
generate the Markdown from the parser. It is important to note that this means
the whole script up until the call to ``parse_args`` is executed in its entirety,
including any side-effects that may entail --- argdown does not attempt
to sanitize the code in any way.

Toy implementation
==================

If a file ``test.py`` reads ::

    import argparse
    import argdown

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('integers', metavar='N', type=int, nargs='+',
    help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
    const=sum, default=max,
    help='sum the integers (default: find the max)')

    args = parser.parse_args()


Then running ::

    argdown test.py


Will output ::

    # Arguments and Usage
    ## Usage
    ```
    usage: argdown [-h] [--sum] N [N ...]
    ```

    ## Arguments
    ### Quick reference table
    |Short|Long    |Default                |Description
    |-----|--------|-----------------------|----------------------------------------
    |`-h` |`--help`|                       |show this help message and exit
    |     |`--sum` |<built-in function max>|sum the integers (default: find the max)

    ### `-h`, `--help`
    show this help message and exit

    ### `--sum` (Default: <built-in function max>)
    sum the integers (default: find the max)

Which renders as:

-------------------

Arguments and Usage
===================
Usage
-----
::

    usage: - [-h] [--sum] N [N ...]

Arguments
---------
Quick reference table
.....................
======  ========== ======================= ===========================================
Short   Long       Default                 Description
======  ========== ======================= ===========================================
``-h``  ``--help``                         show this help message and exit
        ``--sum``  <built-in function max> sum the integers (default: find the max)
======  ========== ======================= ===========================================

``-h``, ``--help``
..................
show this help message and exit

``--sum`` (Default: <built-in function max>)
............................................
sum the integers (default: find the max)

-------------------

Known bugs
==========

There are no known bugs.

Unknown bugs
============

Probably a lot. This script was built to handle the subset of ``argparse``’s
features that I use, so I imagine there are areas in which ``argdown`` performs
poorly. Please open an issue if you find something.

Missing features
================

The quick reference table output isn’t great; see above where the ``Default``
column is included despite containing no content.

Currently, without ``truncate_help=False`` passed to ``argdown.md_help``, the
description field at the end of the table is truncated to the width of the
terminal to prevent the table from looking awful. I’d like to add a feature to
pass a dict of short descriptions to improve that in the future.

RST output, possibly.

License
=======

MIT, see ``license.txt``

.. _argparse: https://docs.python.org/3/library/argparse.html
.. _license.txt: blob/master/license.txt
