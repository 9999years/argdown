import argparse

# so i can nicely format my help messages and not worry about weird
# formatting for the user (sorry!)
def desc(description):
    if description[0] == '\n':
        return description[1:].replace('\n', ' ')
    else:
        return description.replace('\n', ' ')

version = '1.0.0'

# set up arguments
parser = argparse.ArgumentParser(
    description='Render an arbitrary Julia set or a grid of Julia sets'
    'with differing constants c from a user-entered equation.',
    prog='julia.py'
)

parser.add_argument('--fn', '-f', metavar='zₙ₊₁', type=str,
    default=None, help=desc('''
The Julia set's function for iteration. Enter `random` to generate a random
complex rational function P(z)/Q(z), where P(z) and Q(z) are complex polynomials
of maximum degree 3 and 6, respectively.'''))

parser.add_argument('-c', '--constant', metavar='constant', type=str,
    default=None, help=desc('''
The constant c for the function zₙ₊₁(z, c). Enter `random` to select a random
value for c. Default: 0 + 0i'''))

parser.add_argument('-a', '--aspect', metavar='aspect', type=float,
    default=1.0, help=desc('''
The output image's w/h aspect ratio.  Ex.: -a 2 implies an image twice as wide
as it is tall. Default: 1.0'''))

parser.add_argument('-w', '--width', metavar='width', type=int,
    default='500', help='''The output image\'s width.''')

parser.add_argument('-i', '--iterations', metavar='iterations', type=int,
    default=32, help='The iterations to calculate the set to.')

parser.add_argument('-r', '--c-range', metavar='c-range', type=float,
    default=1.5, help=desc('''
The range of c values to use --- only relevant if the cell count option is used
to render a grid of sets; the c values for each sets will range from (c_r -
crange, c_i - crange·i) to (c_r + crange, c_i + crange·i), where c_r and c_i
are the real and imaginary components of the constant supplied with -c. Default:
1.5'''))

parser.add_argument('-n', '--cell-count', metavar='cell count', type=int,
    default=1, help=desc('''
The number of rows and columns to render. A cell count of 1 will render a
single set, and other values will render grids of Julia sets. The different
values of c are determined by --c-range or -r. Default: 1'''))

parser.add_argument('-e', '--center', metavar='center', type=float,
    default=[0, 0], nargs=2, help=desc('''
The coordinate the graph is centered around, entered as two floats separated by
a space. (Not a comma! No parenthesis! It's technically two separate arguments
consumed by one option.) Default: 0 0'''))

parser.add_argument('-z', '--zoom', metavar='zoom', type=float,
    default=1, help=desc('''
How zoomed in the render is. The distance between the center-point and the top
/ bottom of the rendered area is 1 / zoom. Larger values of will produce a more
zoomed-in image, smaller values (<1) will produce a more zoomed-out image.
Default: 1'''))

parser.add_argument('-g', '--gradient', metavar='gradient speed', type=float,
    default=1, help=desc('''
The plotter colors images by smoothly interpolating the orbit escape times for
each value of z₀ in the, governed by a sine function. This option adds a
multiplier within the sine function to increase the oscillation speed, which
may help to enhance details in lightly colored images. Default: 1.0'''))

parser.add_argument('-u', '--cutoff', '--escape-radius',
    metavar='escape', type=float, default=30, help=desc('''
The orbit escape radius --- how large |zₙ| must be before it's considered to
have diverged. Usually ≈ 30 for Julia sets, 2 for the Mandelbrot set. Default:
30.0'''))

parser.add_argument('-o', '--output', metavar='directory', type=str,
        default='./output/', help=desc('''
Output directory to write images to. Default: ./output/'''))

parser.add_argument('--info-dir',
    metavar='directory', type=str, default='./info/', help=desc('''
Directory to write information files to, relative to the output directory. If
it’s not a first-level directory within the output directory, HTML output will
look funny. Default: ./info/'''))

parser.add_argument('--no-info', action='store_false',
    help='''Don't write the HTML info file.''')

parser.add_argument('--no-render', action='store_true', help=desc('''
Generates appropriate HTML information files but doesn't render an
image (useful with `--filename` if the info for an image has been lost to
the sands of time...)'''))

parser.add_argument('--no-progress', action='store_false', help=desc('''
Don't output progress percentage and finish ETA. May increase
performance.'''))

parser.add_argument('--filename', metavar='pathspec', type=str, help=desc('''
Filename base for the output image. Relative to the output directory. Shouldn't
include extensions. Defaults: The current Unix timestamp'''))

parser.add_argument('--no-convert', action='store_false', help=desc('''
Don't shell out to `magick` to convert the .ppm to a .png after rendering.'''))

parser.add_argument('--no-open', action='store_false', help=desc('''
Don't open HTML output in a browser after completing rendering.'''))

parser.add_argument('-s', '--silent', action='store_true', help=desc('''
Don't log info, show progress, convert the .ppm to a .png, or open the file when
finished rendering.  Equivalent to `--no-open --no-convert --no-progress
--no-info`.'''))

parser.add_argument('--license', action='store_true',
    help='Print license information (MIT) and exit.')

parser.add_argument('-v', '--version', action='version',
    version=f'%(prog)s {version}')
