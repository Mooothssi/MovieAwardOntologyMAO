# YAML ontology specification

## Description
The specification for representing an ontology as a YAML file. This YAML file will be used to generate documentation (as a Markdown) and python classes.

## Version
### v1.0.0
#### Specification
```YAML
# Description of an ontology
annotaions:
  rdfs:label:
    - v1.0.0 example^^xsd:string
    - v1.1.0 example^^rdfs:Literal@en
  dc:title:
    - v1.0.0^^rdfs:Literal@en
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
      owl:Restriction:
        - Thing and (hasClass3 some Class3)
    rdfs:subClassOf: owl:Thing
  example:Class2:
    annotations:
      rdfs:label:
        - Class2^^rdfs:Literal@en
    owl:disjointWith:
      - Class1
    rdfs:subClassOf: owl:Thing
  example:Class3:
    annotations:
      rdfs:label:
        - Class3^^rdfs:Literal@en
    rdfs:subClassOf: owl:Thing

# Annotation properties section
owl:AnnotationProperty:
  dc:title:
    annotations:
      rdfs:comment:
        - A name given to the resource^^rdfs:Literal@en
  dcterms:licence:
    annotations:
      rdfs:comment:
        - A legal document giving official permission to do something with the resource.^^rdfs:Literal@en
      rdfs:label:
        - License^^rdfs:Literal@en

# Data properties section
owl:DataProperty:
  owl:topDataProperty: ""
  example:hasNumber:
    rdf:type:
      - owl:FunctionalProperty
    rdfs:domain:
      - Thing
    rdfs:range:
      - xsd:integer
    rdfs:subPropertyOf:
      - topDataProperty

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

# Information about custom datatypes
rdfs:Datatype:
  example:specialInt:
    owl:equivalentClass:
      - xsd:integer[>=5, <=10]
    annotations:
      rdfs:comment:
        - Just an example of how to specify a custom datatype in this YAML specification^^rdfs:Literal@en
```
- No specified version number
- Consist of `annotations`, `owl:Class`, `owl:annotationProperty`, `owl:dataProperty`, `owl:objectProperty`, and `rdfs:Datatype` sections
- Allow the value of any key to be either string or array

### v1.0.1
#### Specification
```YAML
version: v1.0.1

# the rest of the spec is the same as v1.0.0
...
```
#### Changes in this version
- Add version number of the specification
- Only allow the value of key to be an array

### v1.1.0
#### Specification
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
#### Changes in this version
- Add prefixes section
  - Allow essential prefixes such as `owl`, `rdf`, `rdfs`, and `xsd` to be ignored in the spec
- Add individuals section
  - Only keep information about the individual that is used in class definition
- Remove `owl:restriction` from `owl:equivalentClass` and `rdfs:subClassOf`