#!/usr/bin/env python
import sys
import io
import os
from IPython.nbformat.current import read, write


def remove_outputs(nb):
    """remove the outputs from a notebook"""
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                if 'prompt_number' in cell:
                    del cell['prompt_number']


if __name__ == '__main__':
    fname = sys.argv[1]
    with io.open(fname, 'r') as f:
        nb = read(f, 'json')
    remove_outputs(nb)
    with io.open(fname, 'w', encoding='utf8') as f:
        write(nb, f, 'json')
        f.write(u'\n')
    print "wrote %s" % fname
