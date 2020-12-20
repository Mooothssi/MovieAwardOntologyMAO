import dataclasses


@dataclasses.dataclass
class ContentRatingContract:
    label: str = ''
    hasDescription: str = ''
    appliesInCountry: str = ''
    value: str = ''


@dataclasses.dataclass
class FilmContract:
    title: str = ''
    hasCountryOfOrigin: str = ''
    hasOriginalLanguage: str = ''
    hasPublicationDate: str = ''
