# Ontology description
## Annotations
### label
  - pizza

### title
  - pizza

### licence
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
### Object Property
- hasBase
- hasTopping


# Class
## Food
### Annotations
| Language      | Label                |
| ------------- |:--------------------:|
| English       | Food                 |

### Description
Subclass Of:
  - Thing


## GorgonzolaTopping
### Annotations
| Language      | Label                |
| ------------- |:--------------------:|
| English       | GorgonzolaTopping    |

### Description
Disjoint With:
  - MozzarellaTopping
  - TomatoTopping

Subclass Of:
  - PizzaTopping


## Margherita
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | Margherita    |
| Portuguese    | Margherita    |

### Description
Subclass Of:
  - NamedPizza
  - hasTopping only (MozzarellaTopping or TomatoTopping)
  - hasTopping some MozzarellaTopping
  - hasTopping some TomatoTopping


## MozzarellaTopping
### Annotations
| Language      | Label                |
| ------------- |:--------------------:|
| English       | MozzarellaTopping    |

### Description
Disjoint With:
  - GorgonzolaTopping
  - TomatoTopping

Subclass Of:
  - PizzaTopping


## NamedPizza:
### Description
Subclass Of:
  - Pizza


## Pizza
### Description
Disjoint With:
  - PizzaBase
  - Topping

Equivalent To:
  - Food and (hasBase some PizzaBase)

Subclass Of:
  - Food

### Object Property
  - hasBase
  - hasTopping


## PizzaBase
### Annotations
Comment: Pizza dough that used as a pizza base

| Language      | Label         |
| ------------- |:-------------:|
| English       | PizzaBase     |

### Description
Disjoint With:
  - Pizza
  - PizzaTopping

Subclass Of:
  - Food


## PizzaTopping
### Annotations
Comment: Topping of pizza

| Language      | Label         |
| ------------- |:-------------:|
| English       | PizzaTopping  |

### Description
Disjoint With:
  - Pizza
  - PizzaBase

Subclass Of:
  - Food


## Rosa
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | Rosa          |
| Portuguese    | Rosa          |

### Description
Subclass Of:
  - NamedPizza
  - hasTopping only (GorgonzolaTopping or MozzarellaTopping  or TomatoTopping)
  - hasTopping some GorgonzolaTopping
  - hasTopping some MozzarellaTopping
  - hasTopping some TomatoTopping


## Spiciness
### Annotations
Comment: Spiciness of Pizza

| Language      | Label         |
| ------------- |:-------------:|
| English       | Spiciness     |
| Portuguese    | Tempero       |

### Description
Subclass Of:
  - Thing


## TomatoTopping
### Annotations
| Language      | Label         |
| ------------- |:-------------:|
| English       | TomatoTopping |

### Description
Disjoint With:
  - GorgonzolaTopping
  - MozzarellaTopping

Subclass Of:
  - PizzaTopping


# Annotation property
## title
### Annotations
Comment: A name given to the resource

## licence
### Annotations
Comment: A legal document giving official permission to do something with the resource.

Label: License


# Object property
## hasBase
### Description
Domain:
  - Pizza

Range:
  - PizzaBase


## hasTopping
### Characteristics
  - Inverse functional

### Description
Domain:
  - Pizza

Range:
  - PizzaTopping
