---
<<<<<<< HEAD
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
=======
title: "ipynbでZennの記事を書こう" # 記事のタイトル
emoji: "😸" # アイキャッチとして使われる絵文字（1文字だけ）
type: "idea" # tech: 技術記事 / idea: アイデア記事
topics: ["Zenn","Jupyter"] # タグ。["markdown", "rust", "aws"]のように指定する
published: false # 公開設定（falseにすると下書き）
---

Zennで記事を書くときに、Pythonのコードを使う場合は、
普通に記事を書くよりも、Notebookをそのまま公開したいときなんかもある...と思ったので、
GithubActionの勉強を兼ねて、ipynbをPushすることで、Zennの記事を投稿できるようにしてみる。

以下のコードは、以前書いたもの。
>>>>>>> cf9784c560e7876a637e9c3d6f1ae926b71232ee


#### [2]:


```python
from pxr import Usd,Sdf
```


#### [3]:


```python
ROOT_PATH = "d:/work/py37/USD/clip/"
```


#### [6]:


```python
# Clipを作る
a = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.1.usda')
b = Sdf.Layer.FindOrOpen(ROOT_PATH + 'A/clip.2.usda')
print(a.ExportToString())
print(b.ExportToString())
```

:::message
#usda 1.0

def "ModelA"
{
    double a.timeSamples = {
        1: 1,
    }
    double b = 10
}


#usda 1.0

def "ModelA"
{
    double a.timeSamples = {
        2: 100,
    }
}


:::


#### [7]:


```python
# ClipのレイヤーからManifestを作る。
# Manifestは、ClipsAPIを使用するときに、クリップでアクセスアトリビュートの
# インデックスを作るためのファイル。
# ClipのうちTimeSampleを持つアトリビュートの定義を作る。
manifest = Usd.ClipsAPI.GenerateClipManifestFromLayers([a,b],'/Model')
```


#### [8]:


```python
# 結果は、アノニマスレイヤーとして取得できるので
# このアノニマスレイヤーを保存して使用する。
print(manifest.ExportToString())
manifest.Export(ROOT_PATH + "/manifest_sample.usda")
```

:::message
#usda 1.0


:::

:::message:::


実行した結果は、GithubActionsでMarkdownに変換＆GitへPushされる。
Push先を、Zennの対象フォルダにすることで、NotebookをZennの記事として投稿できる。

公開用のブランチを分けることで、mainでPullしないと衝突する..みたいなことは防ぐ。
