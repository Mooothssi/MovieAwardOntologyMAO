# Class Hierarchy
-Thing
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
SubClass Of:
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

SubClass Of:
  - PizzaTopping


## Margherita
### Annotations
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
### Annotations
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
  - Pizza


## Pizza
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
### Annotations
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
### Annotations
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
### Annotations
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
### Annotations
Comment: Spiciness of Pizza

| Language      | Label         |
| ------------- |:-------------:|
| English       | Spiciness     |
| Portuguese    | Tempero       |

### Description
SubClass Of
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