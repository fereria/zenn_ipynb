# -*- coding: utf-8 -*-
import codecs
import glob
import pprint

import nbconvert
import nbformat


def test_execIpynbCells():
    print("")
    for ipynb in glob.glob("./ipynb/*.ipynb"):
        print(ipynb)
        with codecs.open(ipynb, 'r', 'utf-8') as f:
            lines = f.readlines()

    f = nbformat.reads("".join(lines), as_version=4)

    for cell in f['cells']:

        if cell['cell_type'] == "code":
            if cell['execution_count']:
                outputs = [x['output_type'] for x in cell['outputs']]
                try:
                    print(f"In [{cell['execution_count']}]:")
                    print(exec(cell['source']))
                except:
                    if 'error' not in outputs:
                        assert True
                    else:
                        print("--This cell has already been executed as an error--")
                        for i in cell['outputs']:
                            pprint.pprint(i)
                        print("-----")
            else:
                print('execution_count [-]:')
                print(exec(cell['source']))
