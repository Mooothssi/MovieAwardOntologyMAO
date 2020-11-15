# Ontogen

## To-dos
- [x] `owl:datatypeProperty` (Mostly done)
- [x] `owl:objectProperty` (Partially)
- [x] `rdfs:type` (Mostly done)
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

### Creating an Individual from an Ontology Class
An individual must be first `instantiate()`d before adding any assertions.
```python
from owlready2 import Ontology

from ontogen import OwlClass

onto: Ontology # `owlready2` loaded OWL
parasite_film: OwlClass = OwlClass("mao:Film") # mao:Film rdfs:subclassOf owl:Thing
parasite_film.instantiate("Parasite", onto) # Create an mao:Film individual named Parasite in a given OWL Ontology
```

### Creating an Individual from an Ontology Class
```python
from ontogen import OwlClass

parasite_film: OwlClass
parasite_film.add_property_assertion("mao:hasTitle", "Parasite") # Create a property assertion for an individual
```