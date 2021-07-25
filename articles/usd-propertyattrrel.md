---
title: "Pythonで始めるUSDの基本(3) - Attribute/Property/Relationship"
emoji: "😸"
type: "tech"
topics: ["USD","Python","3DCG"]
published: true
---
前回でUSDのPrimとスキーマについて見てきました。

USDのPrimは、親子化可能なコンテナオブジェクトで  
そのコンテナには「スキーマ」と呼ばれる型（役割）を指定することができます。  
そして、このスキーマを指定することで、Primには様々なプロパティが追加され、  
MeshやCamera、Lightのような3Dに必要とされるデータを表現することができます。  
  
というふうに説明しましたが、前回はさらっと書いただけの「プロパティ」について
今回は詳しく説明していきたいと思います。  

## Propertyとは

まず、Primには、プロパティを指定することができます。  

![](https://gyazo.com/dc73d9895b520f06fd6a69e13d2e42c8.png)

この「プロパティ」は、大きく分けて2種類あります。  
１つめがアトリビュート。  
これは、intだったりstringだったりといった型を持った値です。




```python
from pxr import Usd,Sdf,UsdGeom

stage = Usd.Stage.CreateInMemory()
layer = stage.GetRootLayer()

cube = UsdGeom.Cube.Define(stage,'/sampleCube')
prim = cube.GetPrim()
# UsdAttributeオブジェクトを取得
attr = prim.GetAttribute('size')
print(attr)
attr.Set(2) # 設定
print(attr.Get()) # 取得
```

```bat : >> Result
Usd.Prim(</sampleCube>).GetAttribute('size')
2.0

```

スキーマが指定されているPrimの場合、そのスキーマで指定されている
取得・設定することができます。  
:::message
スキーマはPluginで作成されていて、  
https://fereria.github.io/reincarnation_tech/11_Pipeline/10_USDTips/00_create_custom_schema/  
schema.usda で、Attributeの定義がされています。  
ここで指定されているAttributeが、Primにスキーマを指定した際に設定できます。  
:::

### CustomAttribute

Attributeは、スキーマに定義されたものを使用する以外にCustomAttributeという形で  
追加することができます。  


----



```python

```




```python
prim = stage.DefinePrim('/sample')

attr = prim.CreateAttribute('sampleInt',Sdf.ValueTypeNames.Int)
attrStr = prim.CreateAttribute('sampleStr',Sdf.ValueTypeNames.String)
# Attribute取得
attr.Set(100)
attrStr.Set("Hello World")
# 結果表示
print(attr.Get())
print(stage.ExportToString())
```

```bat : >> Result
100
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "sample"
{
    custom int sampleInt = 100
    custom string sampleStr = "Hello World"
}



```

まず、なんのスキーマも持たない空のPrimを作成し、そのPrimに対してAttributeを追加しました。  
USDのAttributeは、Sdf.ValueTypeNamesで指定した型のAttributeを作成することができます。  
（Pythonで指定するばあいは[以前まとめたこのページ](https://fereria.github.io/reincarnation_tech/11_Pipeline/10_USDTips/01_usd_py_docs/#usdattributetype)参照）  
↑のページをみるとわかりますが、USDのAttributreはあらゆる型に対応しているので、  
必要に応じてAttributeを追加することで、様々な情報を持つことができます。  
  
USDでは、スキーマという形で決まったデータを扱うこともできますが、  
それに＋して、CustomAttributeのように、自分で追加したい情報を自由に追加することができます。  
また、スキーマなしのPrimに対して、Attributeを追加して  
AssetInfo用のPrimを作る...、あるいはXMLのTagのような扱い方をすることもできます。    

## Relationship

もう一つがRelationshipです。  
これは、別のPrimをリレーションでつなぐことができます。  





```python
prim = stage.DefinePrim("/base")
# Relation先
relPrim = stage.DefinePrim("/RelA")
relPrimB = stage.DefinePrim("/RelB")
# Relation作成 追加
rel = prim.CreateRelationship("rel")
rel.AddTarget(relPrim.GetPath())
rel.AddTarget(relPrimB.GetPath())
# RelationでつながっているPrimを取得
for path in rel.GetTargets():
    print(stage.GetPrimAtPath(path))
```

```bat : >> Result
Usd.Prim(</RelA>)
Usd.Prim(</RelB>)

```

Relationshipで、特定のPrimをつないだ例です。  

![](https://gyazo.com/732c0f707c30faa9e0bd41d0d071f4a2.png)

図に表すとこのようになっています。  
例にあるとおり、Relationshipは、ある特定のPrimまでのSdfPathを設定・取得することができます。  
これを利用することで、例えばあるSkelに対してのAnimationデータであったり  
あるMeshに対してアサインされているMaterialであったりのような、  
別のPrimへコネクションするような構造を作ることができます。




```python
from pxr import UsdShade,Gf

stage = Usd.Stage.CreateInMemory()
rootLayer = stage.GetRootLayer()

# Mesh作成
sphere = UsdGeom.Sphere.Define(stage, '/AssetName/Geom/sphere')

matPath = Sdf.Path("/AssetName/Looks/SampleMaterial")
mat = UsdShade.Material.Define(stage, matPath)
shader = UsdShade.Shader.Define(stage, matPath.AppendChild('SampleShader'))
shader.CreateIdAttr('UsdPreviewSurface')
shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1,0,0))
mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
UsdShade.MaterialBindingAPI(sphere.GetPrim()).Bind(mat)
print(stage.ExportToString())

```

```bat : >> Result
#usda 1.0
(
    doc = """Generated from Composed Stage of root layer 
"""
)

def "AssetName"
{
    def "Geom"
    {
        def Sphere "sphere"
        {
            rel material:binding = </AssetName/Looks/SampleMaterial>
        }
    }

    def "Looks"
    {
        def Material "SampleMaterial"
        {
            token outputs:surface.connect = </AssetName/Looks/SampleMaterial/SampleShader.outputs:surface>

            def Shader "SampleShader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (1, 0, 0)
                token outputs:surface
            }
        }
    }
}



```

例として、Materialをアサインした例の場合。  
```rel material:binding = </AssetName/Looks/SampleMaterial>```
MeshからMaterialまでのコネクションは rel material:binding となっているのがわかるかと思います。  
これが、いわゆるRelationshipで、 = のあとのSdfPath /AssetName/Looks/SampleMaterial のPrimとRelationshipを  
作ることで、マテリアルアサインをしています。  

## まとめ

初回のStage/Layer、前回のPrim/スキーマ、そして今回のProperty（Attribute/Relationship）で  
Pythonを使用してUSDを操作する基本が見えてきたのではないかと思います。  

![](https://gyazo.com/778837cc8d17b1cf901c3846be446273.png)

Stage/Layer/Prim/Property をまとめるとこのような感じになります。  
他にも色々要素はあるのですが、基本的な構造・関係性はあまり変わりませんので  
これをおさえておくと、Mayaから出力したUSDをPythonで操作したり...といったことも  
だいぶやりやすくなるのではと思います。



----



```python

```
