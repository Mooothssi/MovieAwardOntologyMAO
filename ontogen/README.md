# Ontogen

## To-dos
- [x] `owl:objectProperty` (Partially)
- [x] `rdfs:type` (Mostly)
- [ ] `rdfs:subClassOf`

## Getting started
Run unit tests in `test_ontogen.csv`

### (`owlready2`) Loading an OWL Ontology
```python
from owlready2 import get_ontology, Ontology
from settings import OWL_FILEPATH

onto: Ontology = get_ontology(f"file:////{OWL_FILEPATH}")
onto.load()
```

### Creating an instance from an Ontology Class
```python
from owlready2 import Ontology

from ontogen import OwlClass

onto: Ontology # owlready loaded OWL
i: OwlClass = OwlClass("mao:Film") # mao:Film rdfs:subclassOf owl:Thing
i.add_property_assertion("mao:hasTitle", "Parasite") # Create a property assertion for an individual
i.instantiate("Parasite", onto) # Create an mao:Film individual named Parasite in a given OWL Ontology
```