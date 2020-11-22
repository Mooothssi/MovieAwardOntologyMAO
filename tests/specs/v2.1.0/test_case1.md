version v2.1.0

# IRI
http://www.co-ode.org/ontologies/pizza/pizza.owl#

# Prefixes
## dc
http://purl.org/dc/elements/1.1/

## dcterms
http://purl.org/dc/terms/

## pizza
http://www.co-ode.org/ontologies/pizza/pizza.owl#


# Ontology Description
### Annotations
Label

| Language | Label |
|----------|-------|
| None     | pizza |

Title

| Language | Title |
|----------|-------|
| English  | pizza |

Licence
  - Creative Commons Attribution 3.0 (CC BY 3.0)

# Class Hierarchy
- Thing
  - Food
    - Pizza
      - NamedPizza
        - Margherita
        - Rosa
    - PizzaBase
    - PizzaTopping
      - GorgonzolaTopping
      - MozzarellaTopping
      - TomatoTopping
  - Spiciness

# Property Hierarchy
## Object Property
- TopObjectProperty
  - hasTopping
  - hasBase

## Data Property
- TopDataProperty

## Annotation Property
- licence
- title

# Classes
## Thing
## Food
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | Food  |

### Description
Subclass of:
  - owl:Thing

## GorgonzolaTopping
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | GorgonzolaTopping |

### Description
Subclass of:
  - PizzaTopping

Disjoint with:
  - MozzarellaTopping
  - TomatoTopping

## Margherita
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | Margherita |
| Portugese | Margherita |

### Description
Subclass of:
  - NamedPizza
  - hasTopping only (MozzarellaTopping or TomatoTopping)
  - hasTopping some MozzarellaTopping
  - hasTopping some TomatoTopping

## MozzarellaTopping
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | MozzarellaTopping |

### Description
Subclass of:
  - PizzaTopping

Disjoint with:
  - GorgonzolaTopping
  - TomatoTopping

## NamedPizza
### Description
Subclass of:
  - Pizza

## Pizza
### Description
Subclass of:
  - Food

Disjoint with:
  - PizzaBase
  - PizzaTopping

Equivalent to:
  - Food and (hasBase some PizzaBase)

### Object Properties
  - hasBase
  - hasTopping

## PizzaBase
### Annotations
Comment
  - Pizza dough that used as a pizza base
### Description
Subclass of:
  - Food

Disjoint with:
  - Pizza
  - PizzaTopping

## PizzaTopping
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | PizzaTopping |

Comment
  - Topping of pizza
### Description
Subclass of:
  - Food

Disjoint with:
  - Pizza
  - PizzaBase

## Rosa
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | Rosa  |
| Portugese | Rosa  |

### Description
Subclass of:
  - NamedPizza
  - hasTopping only (GorgonzolaTopping or MozzarellaTopping or TomatoTopping)
  - hasTopping some GorgonzolaTopping
  - hasTopping some MozzarellaTopping
  - hasTopping some TomatoTopping

## Spiciness
### Annotations
Comment
  - Spiciness of Pizza
Label

| Language | Label |
|----------|-------|
| English  | Spiciness |
| Portugese | Tempero |

### Description
Subclass of:
  - Thing

## TomatoTopping
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | TomatoTopping |

### Description
Subclass of:
  - PizzaTopping

Disjoint with:
  - GorgonzolaTopping
  - MozzarellaTopping


# Object Properties
## topObjectProperty
## hasBase
### Description
Domain:
  - Pizza

Range:
  - PizzaBase

Sub-properties:
  - topObjectProperty

## hasTopping
### Description
Domain:
  - Pizza

Range:
  - PizzaTopping

Sub-properties:
  - topObjectProperty

# Annotation Properties
## title
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | A name given to the resource |

## licence
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | A legal document giving official permission to do something with the resource. |

Label

| Language | Label |
|----------|-------|
| English  | License |

