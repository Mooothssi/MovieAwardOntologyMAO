
from ontogen.base import LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME

from . import OwlAnnotationProperty, OwlDataProperty
from .classes import OwlClass
from .properties import OwlObjectProperty

BASE_ENTITIES = [OwlAnnotationProperty, OwlDataProperty, OwlObjectProperty, OwlClass]
PROPERTY_ENTITIES = {#"annotations": OwlAnnotationProperty,
                     "dataProperty": OwlDataProperty,
                     "objectProperty": OwlObjectProperty}
BUILTIN_ENTITIES = {
    LABEL_ENTITY_NAME: OwlAnnotationProperty(LABEL_ENTITY_NAME),
    COMMENT_ENTITY_NAME: OwlAnnotationProperty(COMMENT_ENTITY_NAME)
}
