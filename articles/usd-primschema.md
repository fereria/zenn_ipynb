---
title: "Pythonで始めるUSDの基本(2) - Primとスキーマ"
emoji: "🦜"
type: "tech"
topics: ["USD","Python","3DCG"]
published: false
---
前回のStage/Layer解説に続いて、第二回目はUsdPrimについて詳しく説明していきたいと思います。

## Primとは

Primとは、Mayaでいうところのノードにあたるもので、USDのデータを保持するコンテナオブジェクトです。  
このPrimは、3Dのシーングラフを構成するのに必要なノードの情報をプロパティとして持つことができます。

そしてそのPrimをステージ内に親子階層で持つことで、シーングラフを表現することができます。  

### シンプルなPrimを定義する




```python
from pxr import Usd,UsdGeom,Sdf,UsdLux

stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()
```




```python
# シンプルなPrimを作る
path = Sdf.Path("/samplePrim")
prim = stage.DefinePrim(path)

print(stage.ExportToString())
```

```bat : >> Result
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "samplePrim"
{
}



```

まず、シンプルなPrimを作成します。  
Primは、「SdfPath」と呼ばれるパスでその名前空間（ネームスペース）の位置を表します。  
この場合は、 simplePrim がパスになります。  
  
![](https://gyazo.com/b8c00fac1318a3b232965cf27a2dab7d.png)

図に表すとこのようになります。  
この段階では、何も入っていない入れ物ができた段階です。  




```python
print(prim.GetAttributes())
print(prim.GetTypeName())
```

```bat : >> Result
[]


```

そのため、このようにアトリビュートを取得しようとしたり、Primのタイプを取得しようとしても、  
アトリビュートはなにもないし、そのPrimがどのような型なのか取得しようとしても  
何も定義されていません。  

## スキーマ

上の例のように DefinePrim で定義したPrimは  
いわゆる「コンテナ」であり、このPrim自体には役割はありません。  
このPrimに対して「役割」を与えるのが「スキーマ」です。  
  
例えば、Cubeを作成してみます。  
作成するには、UsdGeomCubeスキーマを利用します。  




```python
# Cubeを作る
cube = UsdGeom.Cube.Define(stage,'/sampleCube')
# Cubeスキーマを適応したPrimを取得
cubePrim = cube.GetPrim()
print(stage.ExportToString())
```

```bat : >> Result
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "samplePrim"
{
}

def Cube "sampleCube"
{
}



```

他のPrimと違い、 def の定義の右に Cube とついているのがわかります。  
これが、このPrimに定義されているスキーマです。    
  
スキーマには、「Cube」や「Sphere」のようなプリミティブであったり  
移動などをするためのXform、メッシュをあつかう Mesh、カメラのスキーマ等  
3Dで扱うのに必要な様々な定義が用意されています。  
Primにこのスキーマを適応することで、様々なシーングラフを構成します。  

![](https://gyazo.com/27673cbde7bf2d4fcac5e7188049932a.png)  
 
 このusdをusdviewで確認すると、このようなCubeが表示されます。  
 これは、Cubeスキーマを適応した結果  
 このsampleCubePrimがCubeスキーマ（Cubeを表示する）という振る舞いをするようになった結果です。  




```python
print(cube.GetSizeAttr().Get()) # Cubeの大きさを取得
cube.GetSizeAttr().Set(10) # 大きさを変更する
```

```bat : >> Result
10.0

```




```bat: >> Result
True
```



このスキーマには、そのスキーマの「ふるまい」に必要になるプロパティ（アトリビュート・リレーション）と  
扱うために必要な関数が定義されています。  
たとえば、このCubeスキーマであれば [UsdGeomCube](https://graphics.pixar.com/usd/docs/api/class_usd_geom_cube.html) を確認すると、Cubeの大きさを指定するための  
アトリビュートがあり、 GetSizeAttr で、Cubeの大きさを指定できるようになっています。  




```python
import pprint
# Primに定義されたAttributeを取得する
pprint.pprint(cubePrim.GetAttributes())
# PrimTypeを取得
print(cubePrim.GetTypeName())
```

```bat : >> Result
[Usd.Prim(</sampleCube>).GetAttribute('doubleSided'),
 Usd.Prim(</sampleCube>).GetAttribute('extent'),
 Usd.Prim(</sampleCube>).GetAttribute('orientation'),
 Usd.Prim(</sampleCube>).GetAttribute('primvars:displayColor'),
 Usd.Prim(</sampleCube>).GetAttribute('primvars:displayOpacity'),
 Usd.Prim(</sampleCube>).GetAttribute('purpose'),
 Usd.Prim(</sampleCube>).GetAttribute('size'),
 Usd.Prim(</sampleCube>).GetAttribute('visibility'),
 Usd.Prim(</sampleCube>).GetAttribute('xformOpOrder')]
Cube

```

スキーマが定義されたPrimのアトリビュートを確認すると、このようになります。  
「UsdGeomCube」スキーマを定義すれば、このスキーマに対応したAttributeが追加されているのがわかります。  

同じように、ライトやカメラを作りたい場合は  




```python
camera = UsdGeom.Camera.Define(stage,'/sampleCamera')
light = UsdLux.DomeLight.Define(stage,'/domeLight')
print(camera)
print(light)
```

```bat : >> Result
UsdGeom.Camera(Usd.Prim(</sampleCamera>))
UsdLux.DomeLight(Usd.Prim(</domeLight>))

```

このように作成することができ、それぞれのスキーマは[UsdGeomCamera](https://graphics.pixar.com/usd/docs/api/class_usd_geom_camera.html) [UsdLuxDomeLight](https://graphics.pixar.com/usd/docs/api/class_usd_lux_dome_light.html) といった、そのスキーマクラスのオブジェクトを経由して設定をすることができます。

## 親子化

Primというコンテナに対して、スキーマを定義することで    
3Dの各ノードを作成できることがわかりました。    
    
このPrimは親子化することができて、これによってシーングラフを表現することができます。  




```python
stage = Usd.Stage.CreateInMemory()

path = Sdf.Path('/move')
move = UsdGeom.Xform.Define(stage,path)
UsdGeom.Cube.Define(stage,path.AppendChild('CubeA'))
UsdGeom.Cube.Define(stage,path.AppendChild('CubeB'))
print(stage.ExportToString())
```

```bat : >> Result
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def Xform "move"
{
    def Cube "CubeA"
    {
    }

    def Cube "CubeB"
    {
    }
}



```

![](https://gyazo.com/4e6d088f43cedc9c01cc0457275e3be7.png)

USDのシーングラフは、SdfPathを使用することでそのPrimのネームスペースを定義して、  
ルートを/ として、ファイルパスと同様に /move/CubeA /move/CubeB のようになります。  
SdfPathを使用すれば、指定のネームスペース以下のパスをつくることも可能です。

### Child/Parent

親子化されたPrimは、以下のようにすることで子Prim・親Primをそれぞれ取得することができます。  




```python
# 子Primを取得
prim = move.GetPrim()
for child in prim.GetChildren():
    print(child)
    
# 親Primを取得
childPrim = stage.GetPrimAtPath("/move/CubeB")
print(childPrim.GetParent())

# 全Primを取得
for i in stage.Traverse():
    print(i)
```

```bat : >> Result
Usd.Prim(</move/CubeA>)
Usd.Prim(</move/CubeB>)
Usd.Prim(</move>)
Usd.Prim(</move>)
Usd.Prim(</move/CubeA>)
Usd.Prim(</move/CubeB>)

```

親子化したPrimを取得した例です。  




```python
prim = move.GetPrim()
api = UsdGeom.XformCommonAPI(prim)
api.SetTranslate((0,5,0))
print(stage.ExportToString())
```

```bat : >> Result
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def Xform "move"
{
    double3 xformOp:translate = (0, 5, 0)
    uniform token[] xformOpOrder = ["xformOp:translate"]

    def Cube "CubeA"
    {
    }

    def Cube "CubeB"
    {
    }
}



```

![](https://gyazo.com/619435fdef7a1152d84769832f2da594.png)

親子化したPrimをまとめて動かすこともできて、その場合はXformスキーマを使用して  
そのPrimに対してXformを指定すればまとめて動かすことができます。  

## まとめ

前回のStage・Layerに続いて、USDの基本になるPrimとスキーマについて見てきました。  
Primとスキーマの関係性は若干わかりにくいので  
stage.DefinePrim(path) してつくれるPrimと  、
各スキーマのクラスから UsdGeom.Xform.Define()した場合の違いを理解すると  
わかりやすいのかなとおもいます。   
Primはコンテナ、スキーマはその属性（タイプ）、そしてそのタイプに応じてPrimにはプロパティが指定されます。  
それによって、様々なシーングラフを表すことができるのが、USDの基本構造になります。  
  
というわけで、次回はこれを踏まえてプロパティ（アトリビュート/リレーション）を  
詳しく説明していこうと思います。  
  
続く！  


----



```python

```
