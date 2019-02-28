#!/usr/bin/env python
from __future__ import print_function

import argparse
import io
import os
import sys

import nbformat
from nbformat import write as write_nb


def read_nb(nb):
    return nbformat.read(nb, as_version=4)


def remove_outputs(nb):
    """remove the outputs from a notebook"""

    # --- Remove bad metadata
    # Should pass `nengo/tests/test_examples.py:test_minimal_metadata`
    if 'kernelspec' in nb.metadata:
        del nb.metadata['kernelspec']
    if 'signature' in nb.metadata:
        del nb.metadata['signature']

    language_info = getattr(nb.metadata, 'language_info', {})
    badinfo = (
        "codemirror_mode",
        "file_extension",
        "mimetype",
        "nbconvert_exporter",
        "version",
    )
    for badkey in badinfo:
        if badkey in language_info:
            del language_info[badkey]

    # --- Clean up cells
    worksheets = nb.worksheets if hasattr(nb, 'worksheets') else [nb]
    for ws in worksheets:
        empty = []  # empty cells

        for cell in ws.cells:
            source_key = ('input'
                          if cell.cell_type == 'code' and 'input' in cell
                          else 'source')
            source = getattr(cell, source_key, None)
            if source is not None and len(source) == 0:
                empty.append(cell)
                continue

            if cell.cell_type == 'code':
                # remove any output (print statements, plots, etc.)
                cell.outputs = []

                # reset cell execution number
                if 'prompt_number' in cell:  # notebook version < 4
                    del cell['prompt_number']
                if 'execution_count' in cell:  # notebook version >= 4
                    cell['execution_count'] = None

                # clear non-useful metadata
                clear_cell_metadata_entry(cell, 'collapsed')
                clear_cell_metadata_entry(cell, 'deletable', value=True)
                clear_cell_metadata_entry(cell, 'editable', value=True)

            elif cell.cell_type == 'markdown':
                # clear non-useful metadata
                clear_cell_metadata_entry(cell, 'deletable', value=True)
                clear_cell_metadata_entry(cell, 'editable', value=True)

            # clear whitespace at ends of lines
            if source is not None:
                assert isinstance(source, str)
                lines = source.split('\n')
                for k, line in enumerate(lines):
                    lines[k] = line.rstrip(' ')

                cell[source_key] = '\n'.join(lines)

        # remove empty cells
        for cell in empty:
            ws.cells.remove(cell)


def clear_cell_metadata_entry(cell, key, value='_ANY_'):
    metadata = cell['metadata']
    if key in metadata and (value == '_ANY_' or metadata[key] == value):
        del metadata[key]


def clear_file(fname, target_version):
    with io.open(fname, 'r', encoding='utf-8') as f:
        nb = read_nb(f)
    remove_outputs(nb)
    with io.open(fname, 'w', encoding='utf-8') as f:
        write_nb(nb, f, version=target_version)
    print("wrote %s" % fname)


def clear_paths(fnames, target_version):
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
    clear_paths([fpath for fpath in fpaths
                 if os.path.isdir(fpath) or fpath.endswith('.ipynb')],
                target_version=target_version)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Clear all outputs in Jupyter notebooks.")
    parser.add_argument(
        '--target-version', type=int, default=4,
        help="Version of notebook format to save.")
    parser.add_argument(
        'fnames', nargs='*',
        help="Files to process. Will recursively descend into directories. "
        "If not provided, notebook will be read from stdin and written to "
        "stdout.")
    args = parser.parse_args()

    if len(args.fnames) > 0:
        clear_paths(args.fnames, target_version=args.target_version)
    else:
        nb = read_nb(sys.stdin)
        remove_outputs(nb)
        write_nb(nb, sys.stdout, version=args.target_version)
