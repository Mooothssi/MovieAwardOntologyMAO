
from ontogen.base import LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME

from ontogen.primitives.base import OwlAnnotationProperty, OwlDataProperty
from ontogen.primitives.classes import OwlClass
from ontogen.primitives.properties import OwlObjectProperty

BASE_ENTITIES = [OwlAnnotationProperty, OwlDataProperty, OwlObjectProperty, OwlClass]
PROPERTY_ENTITIES = {"dataProperty": OwlDataProperty,
                     "objectProperty": OwlObjectProperty}
BUILTIN_ENTITIES = {
    LABEL_ENTITY_NAME: OwlAnnotationProperty(LABEL_ENTITY_NAME),
    COMMENT_ENTITY_NAME: OwlAnnotationProperty(COMMENT_ENTITY_NAME)
}

OWL_READY_ENTITIES = {
    'classes': OwlClass
}
