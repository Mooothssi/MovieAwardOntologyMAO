from typing import Dict

WELL_KNOWN_PREFIXES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'swrl': 'http://www.w3.org/2003/11/swrl#',
    'swrlb': 'http://www.w3.org/2003/11/swrlb#',
    'dcterms': 'http://purl.org/dc/terms/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'foaf': 'http://xmlns.com/foaf/0.1/'
}
S_WK_P = frozenset(WELL_KNOWN_PREFIXES.items())
WELL_KNOWN_IRIS = {v: k for k, v in WELL_KNOWN_PREFIXES.items()}
WK_IRIS = frozenset(WELL_KNOWN_IRIS)

OWL_CLASS = 'owl:Class'
OWL_ANNOTATION_PROPERTY = 'owl:AnnotationProperty'
OWL_OBJECT_PROPERTY = 'owl:ObjectProperty'
OWL_DATA_PROPERTY = 'owl:DataProperty'
OWL_EQUIVALENT_CLASS = 'owl:equivalentClass'
OWL_RESTRICTION = 'owl:Restriction'
OWL_INDIVIDUAL = 'owl:Individual'
OWL_THING = 'owl:Thing'
OWL_INVERSE_OF = 'owl:inverseOf'

RDF_TYPE = 'rdf:type'
RDFS_SUBCLASS_OF = 'rdfs:subClassOf'
RDFS_SUBPROPERTY_OF = 'rdfs:subPropertyOf'
RDFS_RANGE = 'rdfs:range'
RDFS_DOMAIN = 'rdfs:domain'
ANNOTATIONS_KEY = 'annotations'

OWL_DISJOINT_WITH = 'owl:disjointWith'


def lookup_iri(prefix: str, lookup: dict = None) -> str:
    if lookup is None:
        return WELL_KNOWN_PREFIXES[prefix.lower()]
    lookup = dict(lookup)
    lookup.update(WELL_KNOWN_PREFIXES)
    return lookup[prefix.lower()]


def lookup_prefix(iri: str, lookup: dict = None) -> str:
    if lookup is None:
        return WELL_KNOWN_IRIS[iri.lower()]
    lookup = dict(lookup)
    lookup.update(WELL_KNOWN_IRIS)
    return lookup[iri]


def get_full_iri_from_prefix(prefix, short_name: str, lookup: dict = S_WK_P) -> str:
    return short_name.replace(f"{prefix}:", lookup_iri(prefix, lookup))


def build_prefixes(prefixes: Dict[str, str]) -> str:
    prefixes.update(WELL_KNOWN_PREFIXES)
    joined_prefixes = "".join([f"PREFIX {prefix}: <{prefixes[prefix]}>\n" for prefix in prefixes])
    return joined_prefixes
