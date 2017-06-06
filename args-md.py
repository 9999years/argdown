import argparse
# warnings
import sys
# resolving paths
import os
# output
import textwrap

import scrap_args

# unstable!!!!!!!
version = '0.0.1'

def md_help(parser, *, depth=1, header='Arguments and Usage',
        usage_header='Usage', ref_header='Quick reference table',
        args_header='Arguments', spacey=False, show_default=True):
    space = '\n' if spacey else ''
    out = ('#' * depth + f' {header}\n{space}'
        +  '#' * (depth + 1)
        + f' {usage_header}\n{space}'
        f'```\n{parser.format_usage()}```\n{space}'
        +  '#' * (depth + 1) + f' {args_header}\n{space}'
        +  '#' * (depth + 2) + f' {ref_header}\n{space}')

    used_actions = {}
    cols = os.environ['COLUMNS'] if 'COLUMNS' in os.environ else 80
    args_detailed = ''
    table = ''

    class TableWidths(dict):
        def maximize(self, key, val):
            self[key] = max(self[key], len(val))

    table_widths = TableWidths({
            'short': 0,
            'long': 0,
            'default': 0
    })

    for k in parser._option_string_actions:
        action = parser._option_string_actions[k]
        # print(repr(action) + '\n')
        this_id = id(action)
        if this_id in used_actions:
            continue
        used_actions[this_id] = True

        for opt in action.option_strings:
            # --, long option
            if len(opt) > 1 and opt[1] in parser.prefix_chars:
                table_widths.maximize('long', opt)
            # short opt
            elif len(opt) > 0 and opt[0] in parser.prefix_chars:
                table_widths.maximize('short', opt)

        # don't show defaults for options
        default_str = ''
        if show_default and (not isinstance(action.default, bool)
            and not isinstance(action.const, bool)):
            table_widths.maximize('default', repr(action.default))
            default_str = f' (Default: {repr(action.default)})'

        args_detailed += ('#' * (depth + 2)
            + ' `' + '`, `'.join(action.option_strings)
            + f'`{default_str}\n{space}'
            + textwrap.fill(action.help, width=cols) + '\n\n')

    out += args_detailed
    return out

print(md_help(scrap_args.parser, spacey=True))
