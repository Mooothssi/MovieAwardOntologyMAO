# Ontogen
Part of [MAO Project](https://github.com/th-bunratta/MovieAwardOntologyMAO/tree/ontogen)
## To-dos
### Classes
- [x] `rdf:type`
   - [x] Characteristics
- [x] `rdfs:subClassOf` (Mostly done)
   - [x] `Object Property`
   - [x] `Classes`
- [x] `rdfs:equivalentClass` (Mostly done)
- [x] `owl:disjointWith` (Partially)
- [x] `owl:inverseOf`
- [x] `owl:oneOf`
- [x] `owl:Restriction` and class constructs
   - Protege Class Expressions
     - HasValue restriction
       - [x] `value` (Partially)
         - [x] Built-in data types (Mostly)
         - [x] Classes
     - Quantifier
       - [x] `some` (Mostly)
       - [x] `only` (Mostly)
     - Cardinality restriction
       - [x] `min`
       - [x] `max`
       - [x] `exactly`
     - Logical
       - [x] `and` (Mostly)
       - [x] `or` (Mostly)
       - [x] `not` (Partially)
     - Parentheses & Nested parentheses
       - [x] Nested parentheses
   

### Properties
- [x] `owl:ObjectProperty` (Mostly done)
- [x] `owl:DatatypeProperty` (Partially)
- [ ] `owl:AnnotationProperty`
    - [x] `rdfs:comment`
    - [x] `rdfs:label`

### Datatypes
- [ ] Custom `rdfs:Datatype`!
- [ ] `rdfs:Literal`
- [x] `xsd:string` (`owlready2` builtin as `str`)
- [x] `xsd:integer` (`owlready2` builtin as `int`)
- [x] `xsd:float` (`owlready2` builtin as `float`)

### Rules
- [x] `SWRL` expressions (for internal prefixes)

## Getting started
Feel free to run unit tests in `test_ontogen.py`

### Dependency requirements
- Python `3.8` or later
- `owlready2`
- `pyyaml`

### Loading an OWL Ontology
```python
from ontogen import Ontology
from settings import OWL_FILEPATH

onto: Ontology = Ontology.load_from_file(OWL_FILEPATH)
```

### Adding a rule to an OWL Ontology
```python
from ontogen import Ontology

onto: Ontology
onto.add_rule("mao:ActingSituation(?p) ^ mao:hasActor(?p, ?a) -> mao:actsIn(?a, ?p)", "ActsInRule")
```

### Using an YamlToOwlConverter to generate `OwlClass`es
```python
from ontogen import Ontology
from ontogen.converter import OwlClass, YamlToOwlConverter

onto: Ontology # An existing Ontology
converter = YamlToOwlConverter("data/mao.yaml")
film: OwlClass = converter.get_entity("mao:Film")
converter.to_owl_ontology(onto) # Save the results to the Ontology
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
An individual must be first `instantiated` before adding any assertions.
```python
from ontogen import Ontology, OwlClass

onto: Ontology
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

### Adding an Equivalent Class Expression to a Class
Adds an equivalent class expression in Protege's Manchester syntax for inference.
Must be actualized to save an expression into an Ontology.
```python
from ontogen import OwlClass

award_received_situation: OwlClass = OwlClass("mao:AwardReceivedSituation")
award_received_situation.add_equivalent_class_expression("NominationSituation and (win value true)")
```

## References
- Manchester Syntax
  - [W3 OWL2 Manchester Syntax](https://www.w3.org/TR/owl2-manchester-syntax/)
  - [Protege's Class Expressions Syntax](http://protegeproject.github.io/protege/class-expression-syntax/)