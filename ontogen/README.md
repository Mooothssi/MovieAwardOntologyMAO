# Ontogen

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
onto: Ontology # owlready loaded OWL
i: OwlClass = OwlClass("mao:Film")
i.add_property_assertion("mao:hasTitle", "Parasite") # Create a property assertion
i.instantiate("Parasite", onto) # Create a mao:Film named Parasite
```