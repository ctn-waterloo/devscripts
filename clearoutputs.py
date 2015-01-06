#!/usr/bin/env python
from __future__ import print_function

import sys
import io
import os
from IPython.nbformat.current import read, write


def remove_outputs(nb):
    """remove the outputs from a notebook"""
    for ws in nb.worksheets:
        empty = []  # empty cells

        for cell in ws.cells:
            if cell.cell_type == 'code':
                if len(cell.input) == 0:
                    empty.append(cell)
                else:
                    cell.outputs = []
                    if 'prompt_number' in cell:
                        del cell['prompt_number']
            else:
                if 'source' in cell and len(cell.source) == 0:
                    empty.append(cell)

        # remove empty cells
        for cell in empty:
            ws.cells.remove(cell)


if __name__ == '__main__':
    fnames = sys.argv[1:]

    for fname in fnames:
        try:
            with io.open(fname, 'r') as f:
                nb = read(f, 'json')
            remove_outputs(nb)
            with io.open(fname, 'w', encoding='utf8') as f:
                write(nb, f, 'json')
                f.write(u'\n')
            print("wrote %s" % fname)
        except Exception as e:
            print("Skipping '%s' due to %s:\n  %s"
                  % (fname, e.__class__.__name__, e))
