# Class Hierarchy
### Thing
- Gender
- Person
  - Ancestor
  - Parent
  - Spouse


# Property Hierarchy
## Data Property
### topDataProperty
- hasBirthYear
- hasName
  - hasFamilyName
  - hasFirstGivenName
  - knownAs


## Object Property
### topObjectProperty
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
### Annotation
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
### Annotation
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
### Annotation
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
  - owl:FunctionalProperty

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
### Description
Inverse Of:
  - isAncestorOf

Domain:
  - Person

Range: Person

SubProperty Of:
  - isBloodRelationOf

### Characteristics
Characteristics:
  - Transitive


## hasAunt
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - isBloodRelationOf


## hasGender
### Description
Domain:
  - Person

Range:
  - Gender

Characteristics:
  - Functional


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


## :isAncestorOf
### Description
Inverse Of:
  - hasAncestor

SubProperty Of:
  - topObjectProperty


## isBloodRelationOf
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - topObjectProperty

### Characteristics
  - Symmetric


## isInLawOf
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - topObjectProperty

### Characteristics
  - SymmetricProperty


## :isParentOf
### Description
Inverse Of:
  - hasParent

SubProperty Of:
  - topObjectProperty


## isSiblingOf
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - isBloodRelationOf

### Characteristics
  - owl:SymmetricProperty
  - owl:TransitiveProperty


## isSpouseOf
### Description
Domain:
  - Person

Range:
  - Person

SubProperty Of:
  - isInLawOf

### Characteristics
  - SymmetricProperty


# Data type
- Interger
- Literal
- String


# Rule:
## hasAunt:
<pre>
  family:Person(?p) ^ family:Person(?a) ^ family:Person(?c) ^
  family:isSiblingOf(?p,?a) ^ family:isParentOf(?p,?c) ^ family:hasGender(?a,family:Female)
  -> family:hasAunt(?c,?a)
</pre>