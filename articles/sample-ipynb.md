---
title: "ipynbでZennの記事を書こう"
emoji: "😸"
type: "idea"
topics: ["Zenn","JupyterNotebook"]
published: true
---
この記事は、Notebookを使用して書いています。

:::message
元になっているipynbは
https://github.com/fereria/zenn_ipynb/blob/master/ipynb/sample-ipynb.ipynb
こちらで、ipynbをGitにPushすると、GithubActionsが実行されて
自動でmarkdownに変換→mdをpushしています。
:::

## HeaderFormatterの書き方

![](https://gyazo.com/3e428097b74fc40bc7877c5f37b0a6af.png)

Markdownで書いてもよいですが、NotebookらしくPythonで記述できるようにしました。

```python
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
```

ipynbからの変換は、コマンドラインではなくPythonスクリプトを使用します。
１セル目はFormatterであるとして、CellをPopして
その内容をHeaderとして使用します。

あとは、nbconvertのTemplateExporterを使用すれば markdownにすることができます。




```python
print("Hello World!!!")
```

> Hello World!!
> 

Pythonの実行結果を表示した例。
Notebookを使用するメリットとして、このようにコマンドをその場で実行し
その実行結果を残せることがあります。

テストしつつ、そのまま記事になるのはとても良さそうです。

記事は、VSCodeで書くこともできますが、JupyterLabで書くこともできます。

![](https://gyazo.com/698a75b8de7a9bde36add7558534515a.png)

JupyterLabで書いている場合の参考例。
こちらも問題なく記事を書くことができます。

![](https://gyazo.com/0a7214a933a81196a28025e3aef17cc2.png)

JupyterLabの環境は、Dockerコンテナを使用して構築されています。
このコンテナは、GithubActionsを使用して記事を反映する際に使用するものと同じになります。

https://github.com/fereria/zenn_ipynb/tree/master/docker

```
docker-compose -f "docker\docker-compose.yml" up -d --build
```
docker-compose を使用すれば、USD入りの執筆環境JupyterNotebookが起動して、
http://localhost:8888
で接続することができます。

## まとめ

通常の記事であれば、VSCodeでMarkdownを使用して書くほうが楽ですが、
スクリプトをごりごり検証しながら記事を書くような場合は、Notebook上で記事を作成できるのは
とてもメリットがあります。

しばらくは色々検証して、より書きやすい環境にアップデートしていければなとおもいます。

https://github.com/fereria/zenn_ipynb
公開用のGithubはこちら。
