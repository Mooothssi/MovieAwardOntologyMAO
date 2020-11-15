import re

__all__ = ['get_pretty_label', 'get_language_from_code']


def get_pretty_label(ugly_label: str) -> str:
    """Returns a pretty human-readable label

    Args:
        ugly_label: The ugly machine label.

    Examples:
        >>> get_pretty_label('rdfs:label')
        'Label'
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
        >>> get_pretty_label('owl:equivalentClass')
        'Equivalent To'
        >>> get_pretty_label('dc:title')
        'Title'
        >>> get_pretty_label('dcterms:licence')
        'Licence'
        >>> get_pretty_label('rdf:type')
        'Characteristics'
        >>> get_pretty_label('rdfs:domain')
        'Domain'
        >>> get_pretty_label('owl:Restriction')
        ''
        >>> get_pretty_label('family:isSpouseOf')
        'isSpouseOf'
        >>> get_pretty_label('owl:inverseOf')
        'Inverse Of'
        >>> get_pretty_label('rdfs:range')
        'Range'
        >>> get_pretty_label('rdfs:comment')
        'Comment'
        >>> get_pretty_label('owl:topObjectProperty')
        'topObjectProperty'
        >>> get_pretty_label('owl:topDataProperty')
        'topDataProperty'
        >>> get_pretty_label('rules')
        'Rules'
        >>> get_pretty_label('owl:AnnotationProperty')
        'Annotation Property'
        >>> get_pretty_label('rdfs:Datatype')
        'Data type'
    """
    prefixes = ['rdfs', 'rdf', 'owl', 'dc', 'dcterms']
    exceptions = ['owl:topDataProperty', 'owl:topObjectProperty']
    sections = ['objectProperty', 'dataProperty']
    prefix_label = ugly_label.split(':')

    if ugly_label in exceptions:
        return prefix_label[1]

    if len(prefix_label) > 1:
        if prefix_label[1] == 'equivalentClass':
            return 'Equivalent To'
        elif prefix_label[1] == 'subClassOf':
            return 'Subclass Of'

    if (prefix_label[0] in prefixes) or (prefix_label[0] in sections):
        label = prefix_label[-1]
        label = re.sub(r'(?<!^)(?=[A-Z])', ' ', label)
        pretty_label = label.title()
        if pretty_label == 'Restriction':
            return ''
        elif pretty_label == 'Type':
            return 'Characteristics'
        elif pretty_label == 'Datatype':
            return 'Data type'
        elif pretty_label == 'Equivalent Class':
            return 'Equivalent To'
        return pretty_label
    else:
        if len(prefix_label) > 1:
            return prefix_label[1]
        return prefix_label[0].title()


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
    if language_code == 'pt':
        return 'Portugese'
    raise AssertionError(language_code)
