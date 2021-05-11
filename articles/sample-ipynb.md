---
title: "ipynbでZennの記事を書こう"
emoji: "😸"
type: "idea"
topics: ["Zenn","JupyterNotebook"]
published: false
---
Zennで記事を書くときに、Pythonのコードを使う場合は、  
普通に記事を書くよりも、Notebookをそのまま公開したいときなんかもある...と思ったので、  
GithubActionの勉強を兼ねて、ipynbをPushすることで、Zennの記事を投稿できるようにしてみる。  
  
以下のコードは、以前書いたもの。  

まず、モジュールをロードします。


----



```python
from pxr import Usd,Sdf
```


----



```python
ROOT_PATH = "d:/work/py37/USD/clip/"
```

次にValueClip用のレイヤーをロードします。  


----



```python
# Clipを作る
a = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.1.usda')
b = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.2.usda')
print(a.ExportToString())
print(b.ExportToString())
```

```
>>> #usda 1.0
... 
... def "ModelA"
... {
...     double a.timeSamples = {
...         1: 1,
...     }
...     double b = 10
... }
... 
... 
... #usda 1.0
... 
... def "ModelA"
... {
...     double a.timeSamples = {
...         2: 100,
...     }
... }
... 
... 
... 
```


----



```python
# ClipのレイヤーからManifestを作る。
# Manifestは、ClipsAPIを使用するときに、クリップでアクセスアトリビュートの
# インデックスを作るためのファイル。
# ClipのうちTimeSampleを持つアトリビュートの定義を作る。
manifest = Usd.ClipsAPI.GenerateClipManifestFromLayers([a,b],'/Model')
```


----



```python
# 結果は、アノニマスレイヤーとして取得できるので
# このアノニマスレイヤーを保存して使用する。
print(manifest.ExportToString())
manifest.Export(ROOT_PATH + "/manifest_sample.usda")
```

```
>>> #usda 1.0
... 
... 
... 
```




```
>>> True
```



実行した結果は、GithubActionsでMarkdownに変換＆GitへPushされる。
Push先を、Zennの対象フォルダにすることで、NotebookをZennの記事として投稿できる。

公開用のブランチを分けることで、mainでPullしないと衝突する..みたいなことは防ぐ。
