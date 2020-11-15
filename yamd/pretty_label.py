__all__ = ['get_pretty_label', 'get_language_from_code']


def get_pretty_label(ugly_label: str) -> str:
    """Returns a pretty human-readable label

    Args:
        ugly_label: The ugly machine label.

    Examples:
        >>> get_pretty_label('rdfs:label')
        'label'
        >>> get_pretty_label('owl:disjointWith')
        'Disjoint With'
        >>> get_pretty_label('annotations')
        'Annotations'
        >>> get_pretty_label('rdfs:subClassOf')
        'Subclass Of'
        >>> get_pretty_label('pizza:GorgonzolaTopping')
        'GorgonzolaTopping'
        >>> get_pretty_label('objectProperty')
        'Object Property'
        >>> get_pretty_label('dataProperty')
        'Data Property'
        >>> get_pretty_label('equivalentClass')
        'Equivalent To'
        >>> get_pretty_label('dc:title')
        'Title'
        >>> get_pretty_label('dcterms:licence')
        'Licence'
        >>> get_pretty_label('rdf:type')
        'Characteristics'
        >>> get_pretty_label('rdfs:domain')
        'Domain'
    """
    pass


def get_language_from_code(language_code: str) -> str:
    """Returns a pretty human-readable language from its code.

    Args:
        language_code: The language code

    Examples:
        >>> get_language_from_code('en')
        'English'
        >>> get_language_from_code('pt')
        'Portuguese'
    """
    if language_code == 'en':
        return 'English'
