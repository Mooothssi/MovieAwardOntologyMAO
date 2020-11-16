# Ontogen

## To-dos
### Classes
- [x] `rdfs:type` (Mostly done)
- [x] `rdfs:subClassOf` (Mostly done)
   - [x] `Object Property`
   - [x] `Classes`
- [ ] `rdfs:equivalentClass`
- [x] `owl:disjointWith` (Partially)
- [ ] `owl:Restriction` and class constructs
   - Protege Class Expressions
     - HasValue restriction
       - [ ] `value`
     - Quantifier
       - [ ] `some` (Existential)
       - [ ] `only` (Universal)
     - Cardinality restriction
       - [ ] `min`
       - [ ] `max`
       - [ ] `exactly` (Exact)
     - Logical
       - [ ] `and`
       - [ ] `or` (triple)
       - [ ] `not` (double)
     - Parentheses & Nested parentheses
   

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

### Rules
- [ ] `SWRL` expressions

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
from ontogen.converter import OwlClass, YamlToOwlConverter

converter = YamlToOwlConverter("data/mao.yaml")
film: OwlClass = converter.get_entity("mao:Film")
...
```

### Saving (Actualizing) a newly-defined Class to an Ontology
```python
from ontogen import Ontology, OwlClass

onto: Ontology
mao_film: OwlClass = OwlClass("mao:Film")
# Realise mao:Film class into the given `onto` Ontology
mao_film.actualize(onto)
```


### Creating an Individual from an Ontology Class
An individual must be first `actualized` and `instantiated` before adding any assertions.
```python
from ontogen import Ontology, OwlClass

onto: Ontology # `owlready2` loaded OWL
# mao:Film rdfs:subclassOf owl:Thing
parasite_film: OwlClass = OwlClass("mao:Film") # or selectively `converter.get_entity("mao:Film")`
# Create an mao:Film individual named Parasite in a given OWL Ontology
parasite_film.instantiate(onto, "Parasite") 
```

### Adding a Property Assertion to an Individual
```python
from ontogen import OwlClass

parasite_film: OwlClass
parasite_film.add_property_assertion("mao:hasTitle", "Parasite") # Create a property assertion for an individual
```