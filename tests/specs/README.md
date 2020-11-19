# YAML ontology specification

## Description


## Version
### v1.0.0
Specification
```YAML

```


### v1.0.1
Specification
```YAML

```
**Changes in this version**
- Add version number of the specification
- Support an array only

### v1.1.0
Specification
```YAML
version: v1.1.0

# Prefixes used in an ontology
prefixes:
  dc: "http://purl.org/dc/elements/1.1/"
  dcterms: "http://purl.org/dc/terms/"
  owl: "http://www.w3.org/2002/07/owl#"
  rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  rdfs: "http://www.w3.org/2000/01/rdf-schema#"
  xsd: "http://www.w3.org/2001/XMLSchema#"

# Description of an ontology
annotaions:
  rdfs:label:
    - v1.1.0 example^^xsd:string
    - v1.1.0 example^^rdfs:Literal@en
  dc:title:
    - v1.1.0^^rdfs:Literal@en
  dcterms:licence:
    - Put license info here^^xsd:string

# Classes section
owl:Class:
  owl:Thing: ""
  example:Class1:
    annotations:
      rdfs:comment:
        - >
          This is Class 1^^rdfs:Literal@en
      rdfs:label:
        - Class1^^rdfs:Literal@en
    dataProperty:
      - hasNumber
    objectProperty: 
      - hasClass3
    owl:disjointWith:
      - Class2
    owl:equivalentClass:
      - Thing and (hasClass3 some Class3)
    rdfs:subClassOf:
      - owl:Thing
  example:Class2:
    annotations:
      rdfs:label:
        - Class2^^rdfs:Literal@en
    owl:disjointWith:
      - Class1
    rdfs:subClassOf:
      - owl:Thing
  example:Class3:
    annotations:
      rdfs:label:
        - Class3^^rdfs:Literal@en
    rdfs:subClassOf:
      - owl:Thing

# Annotation properties section
owl:AnnotationProperty:
  dc:title:
    annotations:
      rdfs:comment:
        - >
          A name given to the resource^^rdfs:Literal@en
  dcterms:licence:
    annotations:
      rdfs:comment:
        - >
          A legal document giving official permission to do something with the resource.^^rdfs:Literal@en
      rdfs:label:
        - License^^rdfs:Literal@en

# Data properties section
owl:DataProperty:
  owl:topDataProperty: ""
  example:hasNumber:
    rdfs:domain:
      - Thing
    rdfs:range:
      - xsd:integer
    rdfs:subPropertyOf:
      - topDataProperty
    rdf:type:
      - owl:FunctionalProperty

# Object properties section
owl:ObjectProperty:
  owl:topObjectProperty: ""
  example:hasClass3:
    rdfs:domain:
      - Class1
    rdfs:range: 
      - Class3
    rdfs:subPropertyOf:
      - topObjectProperty
  example:isClass3Of:
    owl:inverseOf:
      - hasClass3
    rdfs:domain:
      - Class1
    rdfs:range: 
      - Class3
    rdfs:subPropertyOf:
      - topObjectProperty

# Individuals section
owl:Individual:
  example:Individual_Class1:
    rdf:type:
      - Class1

# Information about custom datatypes
rdfs:Datatype:
  example:specialInt:
    owl:equivalentClass:
      - xsd:integer[>=5, <=10]
    annotations:
      rdfs:comment:
        - >
          Just an example of how to specify a custom datatype in this YAML specification^^rdfs:Literal@en
```
**Changes in this version**
- Add prefixes section
- Add individuals section
