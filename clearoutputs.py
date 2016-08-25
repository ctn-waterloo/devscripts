#!/usr/bin/env python
from __future__ import print_function

import io
import os
import sys

from nengo.utils.ipython import read_nb, write_nb


def remove_outputs(nb):
    """remove the outputs from a notebook"""

    if 'signature' in nb.metadata:
        del nb.metadata['signature']

    worksheets = nb.worksheets if hasattr(nb, 'worksheets') else [nb]
    for ws in worksheets:
        empty = []  # empty cells

        for cell in ws.cells:
            if cell.cell_type == 'code':
                source = cell.input if hasattr(cell, 'input') else cell.source
                if len(source) == 0:
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


def clear_file(fname, target_version):
    with io.open(fname, 'r') as f:
        nb = read_nb(f)
    remove_outputs(nb)
    with io.open(fname, 'w', encoding='utf8') as f:
        write_nb(nb, f, version=target_version)
        f.write(u'\n')
    print("wrote %s" % fname)


def clear_files(fnames, target_version):
    for fname in fnames:
        if os.path.isdir(fname):
            clear_directory(fname, target_version=target_version)
        else:
            clear_file(fname, target_version=target_version)


def clear_directory(dname, target_version):
    assert os.path.isdir(dname)
    fnames = os.listdir(dname)
    fpaths = [os.path.join(dname, fname) for fname in fnames
              if not fname.startswith('.')]
    clear_files([fpath for fpath in fpaths
                 if os.path.isdir(fpath) or fpath.endswith('.ipynb')],
                target_version=target_version)


if __name__ == '__main__':
    fnames = sys.argv[1:]
    clear_files(fnames, target_version=3)
