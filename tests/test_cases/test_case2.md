# Class Hierarchy
- Thing
  - Gender
  - Person
    - Ancestor
    - Parent
    - Spouse


# Property Hierarchy
## Data Property
- topDataProperty
  - hasBirthYear
  - hasName
    - hasFamilyName
    - hasFirstGivenName
    - knownAs


## Object Property
- topObjectProperty
  - hasGender
  - isBloodRelationOf
    - hasAncestor
      - hasParent
    - hasAunt
    - isSiblingOf
  - isInLawOf
    - isSpouseOf
  - isAncestorOf
  - isParentOf


# Class
## Ancestor
### Description
Equivalent To:
  - Person and (isAncestorOf some Person)

Subclass Of: Person

### Object Property
  - isAncestorOf


## Gender
### Description
Disjoint With: Person

Equivalent To:
  - {Female, Male, Non-binary}

Subclass Of: Thing


## Parent
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | Parent        |

### Description
Equivalent To:
  - Person and (isParentOf some Person)

Subclass Of: Person

### Object Property
  - isParentOf


## Person
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | Person        |

### Data Property
  - hasBirthYear
  - hasName

### Description
Equivalent To:
  - (hasParent some Person) and (hasGender some Gender)

Disjoint With: Gender

Subclass Of: Thing

### Object Property
  - hasParent
  - hasGender


## Spouse
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | Spouse        |

### Description
Equivalent To:
  - Person and (isSpouseOf some Person)

Subclass Of: Person

### Object Property
  - isSpouseOf


# Data Property

## hasBirthYear
### Characteristics
  - Functional

### Description
Domain:
  - Person

Range:
  - Integer

Subproperty Of:
  - topDataProperty


## hasFamilyName
### Description
Domain:
  - Person

Range:
  - String

Subproperty Of:
  - hasName


## hasFirstGivenName:
### Description
Domain:
  - Person

Range:
  - String

Subproperty Of:
  - hasName


## hasName:
### Description
Domain:
  - Person

Range:
  - String

Subproperty Of:
  - topDataProperty


## knownAs:
### Description
Domain:
  - Person

Range:
  - String

Subproperty Of:
  - hasName


# Object property

## hasAncestor
### Characteristics
  - Transitive

### Description
Inverse Of:
  - isAncestorOf

Domain:
  - Person

Range: Person

Subproperty Of:
  - isBloodRelationOf


## hasAunt
### Description
Domain:
  - Person

Range:
  - Person

Subproperty Of:
  - isBloodRelationOf


## hasGender
### Characteristics:
  - Functional

### Description
Domain:
  - Person

Range:
  - Gender


## hasParent
### Description
Inverse Of:
  - isParentOf

Domain:
  - Person

Range:
  - Person

Subproperty Of:
  - hasAncestor


## isAncestorOf
### Description
Inverse Of:
  - hasAncestor

Subproperty Of:
  - topObjectProperty


## isBloodRelationOf
### Characteristics
  - Symmetric

### Description
Domain:
  - Person

Range:
  - Person

Subproperty Of:
  - topObjectProperty


## isInLawOf
### Characteristics
  - Symmetric
### Description
Domain:
  - Person

Range:
  - Person

Subproperty Of:
  - topObjectProperty


## isParentOf
### Description
Inverse Of:
  - hasParent

Subproperty Of:
  - topObjectProperty


## isSiblingOf
### Characteristics
  - Symmetric
  - Transitive

### Description
Domain:
  - Person

Range:
  - Person

Subproperty Of:
  - isBloodRelationOf


## isSpouseOf
### Characteristics
  - Symmetric

### Description
Domain:
  - Person

Range:
  - Person

Subproperty Of:
  - isInLawOf


# Data type

## personAge
### Annotations
Comment: Age of person which is the integer between 0 to 150

### Description
Datatype Definitions:
  - integer[>=0, <=150]


# Rule
## hasAunt:
```
  family:Person(?p) ^ family:Person(?a) ^ family:Person(?c) ^ family:isSiblingOf(?p,?a) ^ family:isParentOf(?p,?c) ^ family:hasGender(?a,family:Female) -> family:hasAunt(?c,?a)
```