from datetime import date
from typing import Union

LABEL_ENTITY_NAME = "rdfs:label"
COMMENT_ENTITY_NAME = "rdfs:comment"

BUILTIN_NAMES = (LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME, "title")
# BUILTIN_DATA_TYPES = (str, int, float)
BUILTIN_DATA_TYPES = Union[str, int]
GENERATED_TYPES = {}
DATATYPE_MAP = {
    'xsd:boolean': bool,
    'xsd:string': str,
    'xsd:integer': int,
    'xsd:float': float,
    'xsd:decimal': float,
    'xsd:date': date,
    'rdfs:Literal': str
}
