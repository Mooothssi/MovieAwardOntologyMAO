# yamd

Generate .md documentation from .yaml specs.

```python
from dirs import ROOT_DIR
from yamd import convert_owl_yaml_to_md

convert_owl_yaml_to_md(ROOT_DIR / 'mao.yaml', ROOT_DIR / 'mao.md')
```
