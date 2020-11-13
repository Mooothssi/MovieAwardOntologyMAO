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

SubClass Of: Person

### Object Property
  - isAncestorOf


## Gender
### Description
Disjoint With: Person

Equivalent To:
  - {Female, Male, Non-binary}

SubClass Of: Thing


## Parent
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | Parent        |

### Description
Equivalent To:
  - Person and (isParentOf some Person)

SubClass Of: Person

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

SubClass Of: Thing

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

SubcClass Of: Person

### Object Property
  - isSpouseOf

# Annotation property
- Label


# Data Property

## hasBirthYear
### Characteristics
  - Functional

### Description
Domain:
  - Person

Range:
  - Integer

SubProperty Of:
  - topDataProperty


## hasFamilyName
### Description
Domain:
  - Person

Range:
  - String

SubProperty Of:
  - hasName


## hasFirstGivenName:
### Description
Domain:
  - Person

Range:
  - String

SubProperty Of:
  - hasName


## hasName:
### Description
Domain:
  - Person

Range:
  - String

SubProperty Of:
  - topDataProperty


## knownAs:
### Description
Domain:
  - Person

Range:
  - String

SubProperty Of:
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

SubProperty Of:
  - isBloodRelationOf


## hasAunt
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
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

SubProperty Of:
  - hasAncestor


## isAncestorOf
### Description
Inverse Of:
  - hasAncestor

SubProperty Of:
  - topObjectProperty


## isBloodRelationOf
### Characteristics
  - Symmetric

### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - topObjectProperty


## isInLawOf
### Characteristics
  - Symmetric
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - topObjectProperty


## isParentOf
### Description
Inverse Of:
  - hasParent

SubProperty Of:
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

SubProperty Of:
  - isBloodRelationOf


## isSpouseOf
### Characteristics
  - Symmetric

### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - isInLawOf


# Data type
- Interger
- Literal
- String


# Rule
## hasAunt:
<pre>
  family:Person(?p) ^ family:Person(?a) ^ family:Person(?c) ^
  family:isSiblingOf(?p,?a) ^ family:isParentOf(?p,?c) ^ family:hasGender(?a,family:Female)
  -> family:hasAunt(?c,?a)
</pre>