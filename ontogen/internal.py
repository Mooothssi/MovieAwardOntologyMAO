from owlready2 import (AsymmetricProperty, SymmetricProperty, FunctionalProperty, IrreflexiveProperty,
                       InverseFunctionalProperty, ReflexiveProperty, TransitiveProperty)

# owlready2 stuff here

CHARACTERISTICS_MAPPING = {
    "owl:AsymmetricProperty": AsymmetricProperty,
    "owl:SymmetricProperty": SymmetricProperty,
    "owl:TransitiveProperty": TransitiveProperty,
    "owl:FunctionalProperty": FunctionalProperty,
    "owl:IrreflexiveProperty": IrreflexiveProperty,
    "owl:ReflexiveProperty": ReflexiveProperty,
    "owl:InverseFunctionalProperty": InverseFunctionalProperty
}

CONSTRAINT_DATATYPE_OPERATOR_MAP = {
    '>': 'min_exclusive',
    '>=': 'min_inclusive',
    '<': 'max_exclusive',
    '<=': 'max_inclusive',
    'pattern': 'pattern'
}
