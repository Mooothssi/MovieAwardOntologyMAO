version v1.0.1

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

