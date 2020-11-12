# Class Hierarchy
### Thing
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
### Annotation
| Language      | Label                |
| ------------- |:--------------------:|
| English       | Food                 |

### Description
SubClass Of:
  - Thing


## GorgonzolaTopping
### Annotation
| Language      | Label                |
| ------------- |:--------------------:|
| English       | GorgonzolaTopping    |

### Description
Disjoint With:
  - MozzarellaTopping
  - TomatoTopping

SubClass Of:
  - PizzaTopping


## Margherita
### Annotation
| Language      | Label         |
| ------------- |:-------------:|
| English       | Margherita    |
| Portuguese    | Margherita    |

### Description
SubClass Of:
  - NamedPizza
  - hasTopping only (MozzarellaTopping or TomatoTopping)
  - hasTopping some MozzarellaTopping
  - hasTopping some TomatoTopping


## MozzarellaTopping
### Annotation
| Language      | Label                |
| ------------- |:--------------------:|
| English       | MozzarellaTopping    |

### Description
Disjoint With:
  - GorgonzolaTopping
  - TomatoTopping

SubClass Of:
  - PizzaTopping


## NamedPizza:
### Description
SubClass Of
  - PizzaTopping


## MozzarellaTopping
### Description
Disjoint With:
  - PizzaBase
  - Topping

Equivalent To:
  - Food and (hasBase some PizzaBase)

SubClass Of
  - Food

### Object Property
  - hasBase
  - hasTopping


## PizzaBase
### Annotation
Comment: Pizza dough that used as
         a pizza base

| Language      | Label         |
| ------------- |:-------------:|
| English       | PizzaBase     |

### Description
Disjoint With:
  - Pizza
  - PizzaTopping

SubClass Of
  - Food


## PizzaTopping
### Annotation
Comment: Topping of pizza

| Language      | Label         |
| ------------- |:-------------:|
| English       | PizzaTopping  |

### Description
Disjoint With:
  - Pizza
  - PizzaBase

SubClass Of
  - Food


## Rosa
### Annotation
| Language      | Label         |
| ------------- |:-------------:|
| English       | Rosa          |
| Portuguese    | Rosa          |

### Description
SubClass Of
  - NamedPizza
  - hasTopping only (GorgonzolaTopping or MozzarellaTopping  or TomatoTopping)
  - hasTopping some GorgonzolaTopping
  - hasTopping some MozzarellaTopping
  - hasTopping some TomatoTopping


## Spiciness
### Annotation
Comment: Spiciness of Pizza

| Language      | Label         |
| ------------- |:-------------:|
| English       | Spiciness     |
| Portuguese    | Tempero       |

### Description
SubClass Of
  - Thing


## TomatoTopping
### Annotation
| Language      | Label         |
| ------------- |:-------------:|
| English       | TomatoTopping |
| Portuguese    | Tempero       |

### Description
Disjoint With:
  - GorgonzolaTopping
  - MozzarellaTopping

SubClass Of
  - PizzaTopping


# Annotation property
- Comment
- Label


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


# Data type
- Literal
- String