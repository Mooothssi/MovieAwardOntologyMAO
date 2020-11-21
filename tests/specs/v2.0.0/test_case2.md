version v2.0.0

# IRI
http://www.co-ode.org/roberts/family-tree.owl#

# Prefixes
## family
http://www.co-ode.org/roberts/family-tree.owl#

## owl
http://www.w3.org/2002/07/owl#

## rdf
http://www.w3.org/1999/02/22-rdf-syntax-ns#

## rdfs
http://www.w3.org/2000/01/rdf-schema#

## xsd
http://www.w3.org/2001/XMLSchema#


# Class Hierarchy
- Thing
  - Gender
  - Person
    - Ancestor
    - Parent
    - Spouse

# Property Hierarchy
### Object Property
- TopObjectProperty
  - hasGender
  - isAncestorOf
  - isBloodRelationOf
    - hasAncestor
      - hasParent
    - hasAunt
    - isSiblingOf
  - isInlawOf
    - isSpouseOf
  - isParentOf

### Data Property
- TopDataProperty
  - hasBirthYear
  - hasName
    - hasFamilyName
    - hasFirstGivenName
    - knownAs


# Classes
## Thing
## Ancestor
### Description
Subclass of:
  - Person

Equivalent to:
  - Person and (isAncestorOf some Person)

### Object Properties
  - isAncestorOf

## Gender
### Description
Subclass of:
  - Thing

Disjoint with:
  - Person

Equivalent to:
  - {Female, Male, Non-binary}

## Parent
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | Parent |
| None     | Parent |

### Description
Subclass of:
  - Person

Equivalent to:
  - Person and (isParentOf some Person)

### Object Properties
  - isParentOf

## Person
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | Person |
| None     | Person |

### Description
Subclass of:
  - Thing

Disjoint with:
  - Gender

Equivalent to:
  - (hasParent some Person) and (hasGender some Gender)

### Object Properties
  - hasParent
  - hasGender

### Data Properties
  - hasBirthYear
  - hasName

## Spouse
### Annotations
Label

| Language | Label |
|----------|-------|
| None     | Spouse |

### Description
Subclass of:
  - Person

Equivalent to:
  - Person and (isSpouseOf some Person)

### Object Properties
  - isSpouseOf


# Object Properties
## topObjectProperty
## hasAncestor
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - isBloodRelationOf

## hasAunt
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - isBloodRelationOf

## hasGender
### Description
Domain:
  - Person

Range:
  - Gender

## hasParent
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - hasAncestor

## isAncestorOf
## isBloodRelationOf
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - topObjectProperty

## isInlawOf
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - topObjectProperty

## isParentOf
Sub-properties:
  - topObjectProperty

## isSiblingOf
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - isBloodRelationOf

## isSpouseOf
### Description
Domain:
  - Person

Range:
  - Person

Sub-properties:
  - isInLawOf


# Data Properties
## topDataProperty
## hasBirthYear
### Description
Domain:
  - Person

Range:
  - xsd:integer

## hasFamilyName
### Description
Domain:
  - Person

Range:
  - xsd:string

Sub-properties:
  - hasName

## hasFirstGivenName
### Description
Domain:
  - Person

Range:
  - xsd:string

Sub-properties:
  - hasName

## hasName
### Description
Domain:
  - Person

Range:
  - xsd:string

## knownAs
### Description
Domain:
  - Person

Range:
  - xsd:string

Sub-properties:
  - hasName


# Individuals
## Female
### Description
Individual of class:
  - Gender

## Male
### Description
Individual of class:
  - Gender

## Non-binary
### Description
Individual of class:
  - Gender

# Rules
## aunt
```
family:Person(?p) ^ family:Person(?a) ^ family:Person(?c) ^ family:isSiblingOf(?p,?a) ^ family:isParentOf(?p,?c) ^ family:hasGender(?a,family:Female) -> family:hasAunt(?c,?a)
```

