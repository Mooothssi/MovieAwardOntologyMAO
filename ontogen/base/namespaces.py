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
    'xml': 'http://www.w3.org/XML/1998/namespace'
}
S_WK_P = frozenset(WELL_KNOWN_PREFIXES.items())
WELL_KNOWN_IRIS = {v: k for k, v in WELL_KNOWN_PREFIXES.items()}
WK_IRIS = frozenset(WELL_KNOWN_IRIS)

OWL_CLASS = 'owl:Class'
OWL_EQUIVALENT_CLASS = 'owl:equivalentClass'
OWL_RESTRICTION = 'owl:Restriction'
OWL_INDIVIDUAL = 'owl:Individual'
OWL_THING = 'owl:Thing'

RDF_TYPE = 'rdf:type'


def lookup_iri(prefix: str, lookup: dict = S_WK_P):
    lookup = dict(lookup)
    lookup.update(WELL_KNOWN_PREFIXES)
    return lookup[prefix.lower()]


def lookup_prefix(iri: str, lookup: dict = WK_IRIS):
    lookup = dict(lookup)
    lookup.update(WELL_KNOWN_IRIS)
    return lookup[iri]


def get_full_iri_from_prefix(prefix, short_name: str, lookup: dict = S_WK_P):
    return short_name.replace(f"{prefix}:", lookup_iri(prefix, lookup))


def build_prefixes(prefixes: Dict[str, str]) -> str:
    p = ""
    prefixes.update(WELL_KNOWN_PREFIXES)
    for prefix in prefixes:
        p += f"PREFIX {prefix}: <{prefixes[prefix]}>\n"
    return p
