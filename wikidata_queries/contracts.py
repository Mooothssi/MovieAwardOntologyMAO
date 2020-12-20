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
    wikidata_id: str = ''
    hasCountryOfOrigin: str = ''
    hasOriginalLanguage: str = ''
    hasPublicationDate: str = ''
    isPrequel: bool = False
    isSequel: bool = False
