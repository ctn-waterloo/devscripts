#!/usr/bin/env python
from __future__ import print_function

import sys
import io
import os
from nengo.utils.ipython import read_nb, write_nb


def remove_outputs(nb):
    """remove the outputs from a notebook"""

    if 'signature' in nb.metadata:
        del nb.metadata['signature']

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


def clear_file(fname):
    try:
        with io.open(fname, 'r') as f:
            nb = read_nb(f)
        remove_outputs(nb)
        with io.open(fname, 'w', encoding='utf8') as f:
            write_nb(nb, f, 'json')
            f.write(u'\n')
        print("wrote %s" % fname)
    except Exception as e:
        print("Skipping '%s' due to %s:\n  %s"
              % (fname, e.__class__.__name__, e))


def clear_files(fnames):
    for fname in fnames:
        if os.path.isdir(fname):
            clear_directory(fname)
        else:
            clear_file(fname)


def clear_directory(dname):
    assert os.path.isdir(dname)
    fnames = os.listdir(dname)
    fpaths = [os.path.join(dname, fname) for fname in fnames
              if not fname.startswith('.')]
    clear_files([fpath for fpath in fpaths
                 if os.path.isdir(fpath) or fpath.endswith('.ipynb')])


if __name__ == '__main__':
    fnames = sys.argv[1:]
    clear_files(fnames)
