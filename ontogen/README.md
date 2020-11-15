# Ontogen

## To-dos
### Classes
- [x] `rdfs:type` (Mostly done)
- [x] `rdfs:subClassOf` (Mostly done)
- [ ] `rdfs:equivalentClass`
- [ ] `owl:disjointWith`

### Properties
- [x] `owl:ObjectProperty` (Partially)
- [x] `owl:DatatypeProperty` (Mostly done)
- [ ] `owl:AnnotationProperty`
    - [ ] `rdfs:comment`
    - [ ] `rdfs:label`

### Datatypes
- [ ] `rdfs:Literal`
- [x] `xsd:string` (`owlready2` builtin as `str`)
- [x] `xsd:integer` (`owlready2` builtin as `int`)
- [x] `xsd:float` (`owlready2` builtin as `float`)

## Getting started
Feel free to run unit tests in `test_ontogen.py`

### (`owlready2`) Loading an OWL Ontology
```python
from owlready2 import get_ontology, Ontology

from settings import OWL_FILEPATH

onto: Ontology = get_ontology(f"file:////{OWL_FILEPATH}")
onto.load()
```

### Using an YamlToOwlConverter to generate `OwlClass`es
```python
from ontogen.owlready_converter import YamlToOwlConverter

converter = YamlToOwlConverter("data/mao.yaml")
film: OwlClass = converter.get_entity("mao:Film")
...
```

### Creating an Individual from an Ontology Class
An individual must be first `instantiate()`d before adding any assertions.
```python
from owlready2 import Ontology

from ontogen import OwlClass

onto: Ontology # `owlready2` loaded OWL
# mao:Film rdfs:subclassOf owl:Thing
parasite_film: OwlClass = OwlClass("mao:Film") # or selectively `converter.get_entity("mao:Film")` 
parasite_film.instantiate("Parasite", onto) # Create an mao:Film individual named Parasite in a given OWL Ontology
```

### Adding a property assertion to an Individual
```python
from ontogen import OwlClass

parasite_film: OwlClass
parasite_film.add_property_assertion("mao:hasTitle", "Parasite") # Create a property assertion for an individual
```