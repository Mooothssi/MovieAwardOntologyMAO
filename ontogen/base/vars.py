from datetime import date


LABEL_ENTITY_NAME = "rdfs:label"
COMMENT_ENTITY_NAME = "rdfs:comment"

BUILTIN_NAMES = (LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME)

GENERATED_TYPES = {}
DATATYPE_MAP = {
    'xsd:boolean': bool,
    'xsd:string': str,
    'xsd:integer': int,
    'xsd:float': float,
    'xsd:decimal': float,
    'xsd:date': date
}