# Ontogen

## How to start
Run unit tests in `test_ontogen.csv`

### Creating an instance from an Ontology Class
```python
onto: Ontology # owlready loaded OWL
i: OwlClass = OwlClass("mao:Film")
i.add_property_assertion("mao:hasTitle", "Parasite") # Create a property assertion
i.instantiate("Parasite", onto) # Create a mao:Film named Parasite
```