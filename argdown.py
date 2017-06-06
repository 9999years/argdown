import argparse as _argparse
# table col
import os as _os
# output
import textwrap as _textwrap

version = '1.0.0'

def md_help(parser, *, depth=1, header='Arguments and Usage',
        usage_header='Usage', ref_header='Quick reference table',
        args_header='Arguments', spacey=False, show_default=True,
        truncate_help=True):
    space = '\n' if spacey else ''
    out = ('#' * depth + f' {header}\n{space}'
        +  '#' * (depth + 1)
        + f' {usage_header}\n{space}'
        f'```\n{parser.format_usage()}```\n\n'
        +  '#' * (depth + 1) + f' {args_header}\n{space}'
        +  '#' * (depth + 2) + f' {ref_header}\n{space}')

    used_actions = {}
    cols = _os.environ['COLUMNS'] if 'COLUMNS' in _os.environ else 80
    args_detailed = ''

    options = []

    class TableWidths():
        def __init__(self, **kwargs):
            for key, val in kwargs.items():
                setattr(self, key, val)
        def maximize(self, key, val):
            setattr(self, key, max(getattr(self, key), len(val)))

    table = ''
    table_widths = TableWidths(
        short=len('Short'),
        long=len('Long'),
        default=len('Default'),
        help=0
    )

    i = 0
    for k in parser._option_string_actions:
        action = parser._option_string_actions[k]
        # print(repr(action) + '\n')
        this_id = id(action)
        if this_id in used_actions:
            continue
        used_actions[this_id] = True

        options.append({
            'long': '',
            'short': '',
            'default': '',
            'help': action.help
        })

        for opt in action.option_strings:
            # --, long option
            if len(opt) > 1 and opt[1] in parser.prefix_chars:
                table_widths.maximize('long', opt)
                options[i]['long'] = opt
            # short opt
            elif len(opt) > 0 and opt[0] in parser.prefix_chars:
                table_widths.maximize('short', opt)
                options[i]['short'] = opt

        # don't show defaults for options
        default_str = ''
        if (show_default and
            not (isinstance(action.default, bool)
            or isinstance(action, _argparse._VersionAction)
            or isinstance(action, _argparse._HelpAction))):
            default = repr(action.default)
            table_widths.maximize('default', default)
            options[i]['default'] = default
            default_str = f' (Default: {default})'

        args_detailed += ('#' * (depth + 2)
            + ' `' + '`, `'.join(action.option_strings)
            + f'`{default_str}\n{space}'
            + _textwrap.fill(action.help, width=cols) + '\n\n')
        i += 1

    # with proper lengths, we can make the table
    table_widths.help = (cols
        - table_widths.short
        - table_widths.long
        - table_widths.default
        - 4)

    options.insert(0, {
        'short': 'Short',
        'long': 'Long',
        'default': 'Default',
        'help': 'Description'
    })
    options.insert(1, {
        'short':   '-' * table_widths.short,
        'long':    '-' * table_widths.long,
        'default': '-' * table_widths.default,
        'help':    '-' * table_widths.help,
    })
    for opt in options:
        table += (f'|{{short:{table_widths.short}}}|'
            f'{{long:{table_widths.long}}}|'
            f'{{default:{table_widths.default}}}|'
            '{help'
                + (f':.{table_widths.help}' if truncate_help else '')
            + '}\n'
        ).format(**opt)

    out += table + '\n' + args_detailed
    return out
