from .datatypes import Datatype
from .base import (Ontology, OwlEntity, OwlAnnotationProperty,
                   OwlDataProperty, absolutize_entity_name)
from .vars import (BASE_ENTITIES, COMMENT_ENTITY_NAME,
                   LABEL_ENTITY_NAME, PROPERTY_ENTITIES)
from .properties import OwlObjectProperty
from .classes import OwlIndividual, OwlClass, OwlThing