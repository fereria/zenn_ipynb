# -*- coding: utf-8 -*-

import glob
import os.path
import os
import codecs

import nbconvert
import nbformat

os.makedirs('articles', exist_ok=True)


for ipynb in glob.glob("./ipynb/*.ipynb"):

    with codecs.open(ipynb, 'r', 'utf-8') as f:
        lines = f.readlines()
    f = nbformat.reads("".join(lines), as_version=4)
    cell = f['cells'].pop(0)
    exec(cell['source'])
    header = ["---",
              f'title: "{title}"',
              f'emoji: "{emoji}"',
              f'type: "{text_type}"',
              "topics: " + "[" + ",".join([f"\"{x}\"" for x in topics]) + "]",
              "published: " + ("true" if published else "false"),
              "---"]

    exporter = nbconvert.TemplateExporter(template_file="template/markdown.tpl")
    (body, resources) = exporter.from_notebook_node(f)

    with codecs.open(f'articles/{os.path.splitext(os.path.basename(ipynb))[0]}.md', 'w', 'utf-8') as f:
        f.write("\n".join(header) + "\n" + body)
