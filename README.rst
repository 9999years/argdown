argdown
#######

Argdown is an extension to Python’s argparse_ module that adds Markdown and RST
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
the whole script up until the call to ``parse_args`` is executed in its
entirety, including any side-effects that may entail --- argdown does not
attempt to sanitize the code in any way.

Arguments and Usage
###################
Usage
=====

::

    usage: argdown [-h] [-] [--license] [--header HEADER]
                   [--usage-header USAGE_HEADER] [--ref-header REF_HEADER]
                   [--args-header ARGS_HEADER] [-s] [-r] [-e HIERARCHY] [-d] [-t]
                   [--header-depth HEADER_DEPTH] [--encoding ENCODING]
                   [-f FUNCTION] [-v]
                   [src_file [src_file ...]]
    

Arguments
=========
Quick reference table
---------------------
+------+-------------------+-------------------------+---------------------------+
|Short |Long               |Default                  |Description                |
+------+-------------------+-------------------------+---------------------------+
|``-h``|``--help``         |                         |Show help                  |
+------+-------------------+-------------------------+---------------------------+
|``-`` |                   |                         |Read from STDIN            |
+------+-------------------+-------------------------+---------------------------+
|      |``--license``      |                         |Print license              |
+------+-------------------+-------------------------+---------------------------+
|      |``--header``       |``Arguments and Usage``  |Header text                |
+------+-------------------+-------------------------+---------------------------+
|      |``--usage-header`` |``Usage``                |Header text                |
+------+-------------------+-------------------------+---------------------------+
|      |``--ref-header``   |``Quick reference table``|Header text                |
+------+-------------------+-------------------------+---------------------------+
|      |``--args-header``  |``Arguments``            |Header text                |
+------+-------------------+-------------------------+---------------------------+
|``-s``|``--spacey``       |                         |Blank lines after headers  |
+------+-------------------+-------------------------+---------------------------+
|``-r``|``--rst``          |                         |Generate rst               |
+------+-------------------+-------------------------+---------------------------+
|``-e``|``--hierarchy``    |``#=-*+.``               |rst header order           |
+------+-------------------+-------------------------+---------------------------+
|``-d``|``--hide-default`` |                         |Hide default arg values    |
+------+-------------------+-------------------------+---------------------------+
|``-t``|``--truncate-help``|                         |Truncate help in this table|
+------+-------------------+-------------------------+---------------------------+
|      |``--header-depth`` |``1``                    |Header depth of top header |
+------+-------------------+-------------------------+---------------------------+
|      |``--encoding``     |``utf-8``                |Input file encoding        |
+------+-------------------+-------------------------+---------------------------+
|``-f``|``--function``     |``None``                 |Function to call in file   |
+------+-------------------+-------------------------+---------------------------+
|``-v``|``--version``      |                         |Show version               |
+------+-------------------+-------------------------+---------------------------+

``-h``, ``--help``
------------------
show this help message and exit

``-``
-----
Read from STDIN instead of a file.

``--license``
-------------
Print license information (MIT) and exit.

``--header`` (Default: Arguments and Usage)
-------------------------------------------
Header text for the `Arguments and Usage` section.

``--usage-header`` (Default: Usage)
-----------------------------------
Header text for the `Usage` section.

``--ref-header`` (Default: Quick reference table)
-------------------------------------------------
Header text for the `Quick reference table` section, a simple table of all the
arguments.

``--args-header`` (Default: Arguments)
--------------------------------------
Header text for the `Arguments` section, a detailed listing of all the
arguments.

``-s``, ``--spacey``
--------------------
Output a blank line after headers.

``-r``, ``--rst``
-----------------
Generate rst (reStructured Text) instead of Markdown.

``-e``, ``--hierarchy`` (Default: ``#=-*+.``)
---------------------------------------------
Order of header characters to use for rst output.

``-d``, ``--hide-default``
--------------------------
Don't output default values for the arguments.

``-t``, ``--truncate-help``
---------------------------
Truncate help in the `Quick reference table` section so that the table's width
doesn't exceed `--width`. Makes terminal output prettier but means you'll
probably have to re-write help messages.

``--header-depth`` (Default: 1)
-------------------------------
Header depth; number of hashes to output before the top-level header.

``--encoding`` (Default: utf-8)
-------------------------------
Encoding of all input files. Frankly, there's no excuse to ever use this
argument

``-f``, ``--function`` (Default: None)
--------------------------------------
Function to be called to parse args. For example, if the arg-parsing mechanism
is contained in a `console()` function (common if the script is a module and
has a console entry point defined), enter `--function console` if `console()`
must be called to define the argument parser.

``-v``, ``--version``
---------------------
show program's version number and exit


Toy test usage
##############

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

Known bugs
##########

There are no known bugs.

Unknown bugs
############

Probably a lot. This script was built to handle the subset of ``argparse``’s
features that I use, so I imagine there are areas in which ``argdown`` performs
poorly. Please open an issue if you find something.

Missing features
################

The quick reference table output isn’t great; see above where the ``Default``
column is included despite containing no content.

Currently, without ``truncate_help=False`` passed to ``argdown.md_help``, the
description field at the end of the table is truncated to the width of the
terminal to prevent the table from looking awful. I’d like to add a feature to
pass a dict of short descriptions to improve that in the future.

License
#######

MIT, see ``license.txt``

.. _argparse: https://docs.python.org/3/library/argparse.html
.. _license.txt: blob/master/license.txt
