# MAO Project

Movie Awards Ontology (MAO)

## Submission
[MAO's CQs](https://docs.google.com/document/d/1fCCBBOLLUXRpFNAixN0ijBHhyUXKfc0Geao4H-j9m3k/edit?usp=sharing): the competency questions of Movie Awards Ontology (MAO)

[Documentation](https://github.com/th-bunratta/MovieAwardOntologyMAO/blob/master/mao.md): the documentation about MAO ontology


## Requirements

Running: Python 3.6+  
Testing: Python 3.8+

## Modules

- **sa-autowrite**

   for `sqlalchemy` model autogeneration from raw CSV files
- [**ontogen**](ontogen/README.md)
   
   for converting `.yaml` specs to RDF `.owl`

## Getting Started

Install requirements

```shell script
pip install -r requirements.txt
```

Generate .owl from .yaml specs. 

```python
from dirs import ROOT_DIR

from ontogen import Ontology
from ontogen.converter import OntogenConverter

# Load ontology from YAML specs
converter = OntogenConverter.load_from_spec(ROOT_DIR / "mao.yaml")

# Save the results to an in-memory Ontology
onto: Ontology = converter.sync_with_ontology()
# Save the results to an RDF/XML file Ontology. Can be 'xml' or 'ttl'
onto.save_to_file(ROOT_DIR / "mao.owl")
```
