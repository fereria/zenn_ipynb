---
title: "テストコード"
emoji: "😸"
type: "idea"
topics: ["Zenn","JupyterNotebook"]
published: false
---
```python
from pxr import Usd,Sdf
```




```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/testPrim")
attr = prim.CreateAttribute("testVal",Sdf.ValueTypeNames.String).Set("Hoge")
print(stage.ExportToString())
```

> #usda 1.0
> (
>     doc = """Generated from Composed Stage of root layer 
> """
> )
> 
> def "testPrim"
> {
>     custom string testVal = "Hoge"
> }
> 
> 
> 




```python
# 実行済 ( execution_countありの場合) は、エラーでもテストはエラーにしない
raise
```

> 
> ---------------------------------------------------------------------------
> 
> RuntimeError                              Traceback (most recent call last)
> 
> <ipython-input-13-c9896f4b2c48> in <module>
>       1 # 実行済 ( execution_countありの場合) は、エラーでもテストはエラーにしない
> ----> 2 raise
> 
> 
> RuntimeError: No active exception to reraise
> 

Markdownになっているセルはテストしない




```python
print('hello world')
```

> hello world
> 
