from owlready2 import (AsymmetricProperty, SymmetricProperty, FunctionalProperty, IrreflexiveProperty,
                       InverseFunctionalProperty, ReflexiveProperty, TransitiveProperty)

CHARACTERISTICS_MAPPING = {
    "owl:AsymmetricProperty": AsymmetricProperty,
    "owl:SymmetricProperty": SymmetricProperty,
    "owl:TransitiveProperty": TransitiveProperty,
    "owl:FunctionalProperty": FunctionalProperty,
    "owl:IrreflexiveProperty": IrreflexiveProperty,
    "owl:ReflexiveProperty": ReflexiveProperty,
    "owl:InverseFunctionalProperty": InverseFunctionalProperty
}