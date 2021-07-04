---
title: "Pythonで始めるUSDの基本 - Stage/Layer"
emoji: "😸"
type: "idea"
topics: ["Zenn","USD","Python"]
published: true
---
## はじめに
さて。
Maya2022からデフォルトでUSDのExportができるようになりました。
そのため、本格的にUSDの検証を始めている人も多いのではないでしょうか。

そうしてUSDを触り始めると、今までにないUSD特有の概念で
わかりにくい、どういうことかわからない、、、ということが出てくるのではないかと思います。
そんな中から今回は、
https://fereria.github.io/reincarnation_tech/11_Pipeline/01_USD/04_layer_stage/
おそらく多くの人が最初混乱するであろうUSDの基本 **ステージ/レイヤー** を
Pythonを利用しつつ詳しく解説していこうと思います。

## レイヤー

まずは、サンプルのファイルを開いてみます。




```python
import os
from pxr import Usd,Sdf

USD_ROOT = os.getcwd() + "/usd"
layer = Sdf.Layer.FindOrOpen(f"{USD_ROOT}/cube.usda")
print(layer)
print(layer.ExportToString())
```

> Sdf.Find('/work_dir/ipynb/usd/cube.usda')
> #usda 1.0
> (
>     defaultPrim = "cube"
> )
> 
> def Cube "cube"
> {
>     int testValue = 10
> }
> 
> 
> 

まず１つめが、なんのコンポジションも含まない、シンプルなキューブに、  
testValueというアトリビュートに10が設定されているレイヤーです。  
  
このレイヤーを開くには、Sdf.Layer.FindOrOpen を使用します。  
FindOrOpenを使用すると、レイヤーオブジェクトを取得することができます。  
このレイヤーから ExportToString() を使用すると、このレイヤーに  
記述されているシーングラフを、アスキーで見ることができます。




```python
refLayer = Sdf.Layer.FindOrOpen(f"{USD_ROOT}/reference.usda")
print(refLayer.ExportToString())
```

> #usda 1.0
> (
>     defaultPrim = "root"
> )
> 
> def Xform "root"
> {
>     def "CubeA" (
>         prepend references = @cube.usda@
>     )
>     {
>         int testValue = 100
>     }
> 
>     def "CubeB" (
>         prepend references = @cube.usda@
>     )
>     {
>     }
> }
> 
> 
> 

次に、もう一つのレイヤーを開いてみます。  
  
このレイヤーには、「リファレンス」のコンポジションが含まれていて、  
![](https://gyazo.com/5b1e6a112f161fcde70768434e1ddf9a.png)    
そして、CubeAには「testValue」というアトリビュートに100という値がセットされている  
事がわかります。

ですが、このレイヤーだけでは  
**「あくまでも現在開いているレイヤーの記述のみ」**がわかるだけで  
「このリファレンスされている別のレイヤーと合成した結果どのようなシーングラフが出来上がるか」わかりません。

このように、レイヤーとは「最終的に合成されるシーングラフの元になるもの」のことです。

## ステージ
  
レイヤーを開いただけでは、あくまでもそのレイヤーに記述された情報のみが  
表示されるだけで、最終的に合成されたシーングラフはわかりません。  
では、その複数のレイヤーから合成された「最終的な結果」がなにかというと  
それが「ステージ」と呼ばれるものです。




```python
stage = Usd.Stage.Open(refLayer)
print(stage.ExportToString())
```

> #usda 1.0
> (
>     defaultPrim = "root"
>     doc = """Generated from Composed Stage of root layer /work_dir/ipynb/usd/reference.usda
> """
> )
> 
> def Xform "root"
> {
>     def Cube "CubeA"
>     {
>         int testValue = 100
>     }
> 
>     def Cube "CubeB"
>     {
>         int testValue = 10
>     }
> }
> 
> 
> 

先程のレイヤーを、ステージで開いてみます。  
開いているのは reference.usda で、

![](https://gyazo.com/081754363bef018a7e576919358882e4.png)  

このような構造になっています。
このステージの結果を、同じく ExportToString() してみるとどうなるかというと

![](https://gyazo.com/4dfa81e881286cd97f48999efd461c57.png)

結果はこのようになりました。  
先ほどとは違い、Stage.Openで開いたレイヤー以下のレイヤーに書かれた情報(testValueの値や、Primタイプ)  
が、全て合成された状態になっていることがわかります。  
  
つまり、このステージというのは  
ルートレイヤー（この場合は reference.usda）と、このルートレイヤー以下にあるコンポジションを  
**合成した結果できあがった結果**のことを指しています。  

そのため、USDで合成された結果のシーングラフを操作したい場合はUsd.Stageを使用するし、  
そのステージ内のあるレイヤー（usdファイル）の情報を取得したい場合は  
Sdf.Layer を使用するようにすれば、目的の情報にたどり着くことができます。  

## プリムとプリムスペック

レイヤーとステージの関係についてなんとなく分かってきたところで  
プリムとプリムスペックについて説明します。  
  
まず、プリムというのはなにかというとMayaでいうところのNodeにあたるものです。  
上の例ならば、rootやCubeAなどがプリムにあたります。  




```python
primA = stage.GetPrimAtPath('/root/CubeA')
print(primA)
```

> Usd.Prim(</root/CubeA>)
> 

ステージからGetPrimAtPathを使用することで、指定したパスのプリムを  
取得することができます。  
  
繰り返しになりますが、  
「ステージ」とは「複数のレイヤーの合成した結果出来上がったシーングラフ」です。  
つまり、ステージ上にあるプリムを GetPrimAtPathで取得した場合に  
取得できるものは「プリム」であり、  
**いくつかのレイヤーによって合成された結果できあがったもの**になります。  
  
![](https://gyazo.com/73c7410706978f80cf6e006ea6103345.png)

## スペック

たとえばCubeAを例に上げると、  
reference.usda の CubeA と cube.usda の cube という2つが合成された結果  
CubeAが出来上がっています。  

このCubeAというプリムがどのように構成されているかを分解してみると、

![](https://gyazo.com/e5af205028ffac2596622035d2b784e6.png)

このようになっています。

それぞれのレイヤーの、シーングラフに組み立てられる前の
reference.usda の CubeA や、 cube.usda の cubeなどの要素をPrimSpecと呼びます。
これは、合成される前の「主張＝オピニオン」です。

レイヤーから、Primを取得してそのPrimのAttributeを取得した例です。




```python
for attr in primA.GetAttributes():
    print(attr)
```

> Usd.Prim(</root/CubeA>).GetAttribute('doubleSided')
> Usd.Prim(</root/CubeA>).GetAttribute('extent')
> Usd.Prim(</root/CubeA>).GetAttribute('orientation')
> Usd.Prim(</root/CubeA>).GetAttribute('primvars:displayColor')
> Usd.Prim(</root/CubeA>).GetAttribute('primvars:displayOpacity')
> Usd.Prim(</root/CubeA>).GetAttribute('purpose')
> Usd.Prim(</root/CubeA>).GetAttribute('size')
> Usd.Prim(</root/CubeA>).GetAttribute('testValue')
> Usd.Prim(</root/CubeA>).GetAttribute('visibility')
> Usd.Prim(</root/CubeA>).GetAttribute('xformOpOrder')
> 

対してPrimから取得した場合はこのようになります。

![](https://gyazo.com/3d29ea4284f03aad537d9333e5b9253a.png)

Primから取得した場合、コンポジションした結果から生まれるものなので  
すべてのAttributeを取得した場合、UsdGeomCubeスキーマののアトリビュートと  
reference.usda に記述されたアトリビュートの合成した結果のAttributeのリストが取得できます。  




```python
spec = refLayer.GetPrimAtPath('/root/CubeA')
for attr in spec.attributes:
    # このレイヤーに書かれているAttributeのみが表示される
    print(attr)
```

> Sdf.Find('/work_dir/ipynb/usd/reference.usda', '/root/CubeA.testValue')
> 

対して、プリムスペックからアトリビュートを取得した場合はどうなるかというと  

![](https://gyazo.com/1d2309444757ac7a1c92f31260731e67.png)

あくまでもこの **レイヤーに記述された「意見（オピニオン）」** のみがリストされるので、結果このようになります。 

## まとめ

ここまで出た用語をまとめてみます。  

レイヤーはUSDファイルのことで、シーングラフを構築するときの **「元情報」** です。  
レイヤー単体では最終的なシーングラフはわかりません。  

このレイヤーをコンポジションして組み立てられた結果できたものを **「ステージ」** と呼びます。

各レイヤーごとに書かれた 「このプリムはこうあってほしい」という Primの元になるPrim を **プリムスペック** と呼びます。  
そして、そのプリムスペックに書かれた情報のことを **オピニオン（＝意見）** と呼びます。  
  
レイヤーからだとなにが取得できて、ステージからだと何が取得できるのか  
というのは、USDを調べた直後はわかりにくいですが  
この違いを理解することで、USDをPythonやSOLARISのなどで扱う場合の理解しやすくなるのではないかと思います。  

## PrimからPrimSpecを取得する（おまけ）

最後に応用編。  
PrimとPrimSpec、レイヤーとステージを理解したところで  
PrimからそのPrimを構成するレイヤーやSpecを取得してみます。  




```python
query =Usd.PrimCompositionQuery(primA)

# Compositionを取得する
for comp in query.GetCompositionArcs():
    print(comp.GetArcType())
    node = comp.GetTargetNode()
    # Target=されているNode、Introducing=しているNodeを取得できる
    # NodeRefとは、シーンディスクリプションを合成するためのノード（コンポジション）を取得できる
    if node.IsRootNode():
        layer = node.layerStack.layers[1]
        # Rootの場合はアノニマスレイヤーがLayerStackに含まれているので
    else:
        layer = node.layerStack.layers[0]
    primSpec = layer.GetPrimAtPath(node.path)
    print(primSpec)
    # AttributeSpec
    for i in primSpec.attributes:
        print(i)
```

> Pcp.ArcTypeRoot
> Sdf.Find('/work_dir/ipynb/usd/reference.usda', '/root/CubeA')
> Sdf.Find('/work_dir/ipynb/usd/reference.usda', '/root/CubeA.testValue')
> Pcp.ArcTypeReference
> Sdf.Find('/work_dir/ipynb/usd/cube.usda', '/cube')
> Sdf.Find('/work_dir/ipynb/usd/cube.usda', '/cube.testValue')
> 

取得するには PrimCompositionQueryを使用します。  
これは、関数名のとおり「あるPrimのコンポジションをすべて列挙」することができます。  
コンポジション関係はPCPというモジュールを使用するのですが、  
そのあたりは詳細は [PCPでコンポジションアークの構造を解析・編集対象を取得する](https://fereria.github.io/reincarnation_tech/11_Pipeline/30_USD_Programming/01_Python/04_pcp_compositionArc/)で  
詳しく書いてありますのでそちらを参照。
