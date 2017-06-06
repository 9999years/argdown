# argdown.py

Python’s [`argparse`][1] module is great at generating command-line usage and
help texts, but pasting pre-formatted and indented terminal output into a
`readme.md` is quite ugly. argdown is a python module that provides a function
`argdown.md_help(parser)` that accepts an `ArgumentParser` object and returns a
string of lovely help text.

# Toy implementation

``` python
import argparse
import argdown

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
    const=sum, default=max,
    help='sum the integers (default: find the max)')

print(argdown.md_help(parser))
```

Which outputs

~~~
# Arguments and Usage
## Usage
```
usage: - [-h] [--sum] N [N ...]
```

## Arguments
### Quick reference table
|Short|Long  |Default                |Description
|-----|------|-----------------------|-------------------------------------------
|-h   |--help|                       |show this help message and exit
|     |--sum |<built-in function max>|sum the integers (default: find the max)

### `-h`, `--help`
show this help message and exit

### `--sum` (Default: <built-in function max>)
sum the integers (default: find the max)
~~~

Which renders as:

> # Arguments and Usage
> ## Usage
> ```
> usage: - [-h] [--sum] N [N ...]
> ```
> 
> ## Arguments
> ### Quick reference table
> Short|Long  |Default                |Description
> -----|------|-----------------------|-------------------------------------------
> -h   |--help|                       |show this help message and exit
> |     |--sum |<built-in function max>|sum the integers (default: find the max)
> 
> ### `-h`, `--help`
> show this help message and exit
> 
> ### `--sum` (Default: <built-in function max>)
> sum the integers (default: find the max)

# Known bugs

There are no known bugs.

# Unknown bugs

Probably a lot. This script was built to handle the subset of `argparse`’s
features that I use, so I imagine there are areas in which `argdown` performs
poorly. Please open an issue if you find something.

# Missing features

The quick reference table output isn’t great; see above where the `Default`
column is included despite containing no content.

Currently, without `truncate_help=False` passed to `argdown.md_help`, the
description field at the end of the table is truncated to the width of the
terminal to prevent the table from looking awful. I’d like to add a feature to
pass a dict of short descriptions to improve that in the future.

# License

MIT, see [`license.txt`](blob/master/license.txt)

[1]: https://docs.python.org/3/library/argparse.html
