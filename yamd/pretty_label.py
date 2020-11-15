MAP = {
    'rdfs:label': 'label'
}


def get_pretty_label(ugly_label: str) -> str:
    """Returns a pretty human-readable label

    Args:
        ugly_label: The ugly machine label.

    Examples:
        >>> get_pretty_label('rdfs:label')
        'label'
        >>> get_pretty_label('owl:disjointWith')
        'Disjoint With'
    """
    pass
