# -*- coding: utf-8 -*-

import glob
import subprocess
import os.path
import os

os.makedirs('articles', exist_ok=True)


for ipynb in glob.glob("./ipynb/*.ipynb"):

    p = subprocess.Popen(['python',
                         '-m', 'nbconvert',
                          '--to', 'markdown',
                          '--output', f'../articles/{os.path.splitext(os.path.basename(ipynb))[0]}.md',
                          '--template', 'template/jupyter_template.tpl',
                          ipynb])
    p.wait()
