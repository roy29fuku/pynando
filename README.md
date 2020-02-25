# pynando

wrapper for Nando (Nanbyo data ontology)

```
from pynando.nando import Nando

# get nanbyo (指定難病)
nanbyo = Nando('nanbyo)

# get shoman (小児特定慢性疾病)
shoman = Nando('shoman')
```

You can access each nando_node by id
```
shoman_1 = shoman['1']
print(shoman_1)
```

```
id: 1
name_ja: 球脊髄性筋萎縮症
synonyms_ja:
name_en: Spinal and bulbar muscular atrophy
synonyms_en:
children:
```