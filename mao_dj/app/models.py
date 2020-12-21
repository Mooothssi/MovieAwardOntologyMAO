from django.db import models
import typing
import re

# class MaxLenMixin:
#     @property
#     def max_len(self):
#         return max(map(self.choices, null=True), null=True)
from django.db.models import ManyToOneRel, AutoField, ForeignObjectRel, Field

# from dirs import ROOT_DIR
from mapping import OSCAR_MAPPING
from ontogen.decorators import include
from utils.dict import select_not_null
from wikidata_queries.base import (get_content_ratings_for_film, get_single_valued_prop,
                                   get_genre_with_subgenres, get_from_imdb_id)


class Gender(models.TextChoices):
    FEMALE = 'female'
    MALE = 'male'
    NON_BINARY = 'non-binary'


class CharacterImportance(models.TextChoices):
    MAIN = 'main'
    SIDE = 'side'
    EXTRA = 'extra'


_M = typing.TypeVar('_M', bound=models.Model)


class UpsertMixin:
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    @classmethod
    def upsert(cls: typing.Type[_M], **kwargs) -> _M:
        kwds = {}
        for rel in cls._meta.get_fields():
            rel: typing.Union[ManyToOneRel, AutoField]
            if isinstance(rel, Field):
                field = rel.name
            else:
                field = rel.field.name
            if '.' in field:
                field = field.split('.')[-1]
            v = kwargs.get(field)
            if v is not None:
                kwds[field] = v
        try:
            return cls.objects.get(**kwds)
        except cls.DoesNotExist:
            pass
        return cls.objects.create(**kwds)


class Agent(UpsertMixin, models.Model):
    # temp
    # label = models.CharField(max_length=255)

    # class Meta:
    #     abstract = True

    @classmethod
    def upsert_instance(cls,
                        hasAward: 'Award' = None,
                        yearHeld: str = None,
                        hasEditionNumber: int = None,
                        yearScreened: int = None
                        ) -> 'AwardCeremony':
        kwds = {
            'hasAward': hasAward,
            'yearHeld': yearHeld,
            'hasEditionNumber': hasEditionNumber,
            'yearScreened': yearScreened
        }
        try:
            return cls.objects.get(**select_not_null(kwds))
        except cls.DoesNotExist:
            pass
        return AwardCeremony.objects.create(**select_not_null(kwds))


class Occupation(models.Model):
    # object properties
    isOccupationof = models.ForeignKey('Person', on_delete=models.CASCADE, null=True)

    # temp
    label = models.CharField(max_length=255)


class Person(Agent):
    # object properties
    isParticipantIn = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE, null=True)
    hasGender = models.CharField(max_length=255, choices=Gender.choices, null=True)
    hasOccupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, null=True)
    eligibleFor = models.ForeignKey('Award', on_delete=models.CASCADE, null=True)

    # data properties
    hasName = models.CharField(max_length=255, null=True)

    # temp
    n_const = models.CharField(max_length=255, unique=True, null=True)


class CollectiveAgent(models.Model):
    # object properties
    # isParticipantIn = models.ForeignKey('Situation', on_delete=models.CASCADE, null=True)
    hasMember = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)


class FilmCast(CollectiveAgent):
    # object properties
    isParticipantIn = models.ForeignKey('ActingSituation', on_delete=models.CASCADE, null=True)


class FilmCrew(CollectiveAgent):
    # object properties
    isParticipantIn = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE, null=True)


class Situation(models.Model):
    # object properties
    isSettingFor = models.ForeignKey('Award', on_delete=models.CASCADE, null=True)  # actually owl:Thing


class ActingSituation(Situation):
    # object properties
    hasActor = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasCharacter = models.ForeignKey('Character', on_delete=models.CASCADE)
    hasFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    isPartOf = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE, null=True)


class FilmMakingSituation(Situation):
    # object proerties
    hasCast = models.ForeignKey(FilmCast, on_delete=models.CASCADE, null=True)
    hasCinematographer = models.ForeignKey(Person, on_delete=models.CASCADE,
                                           related_name='cinematographer_of_film_making_situation_set', null=True)
    hasComposer = models.ForeignKey(Person, on_delete=models.CASCADE,
                                    related_name='composer_of_film_making_situation_set', null=True)
    hasCrew = models.ForeignKey(FilmCrew, on_delete=models.CASCADE, null=True)
    hasDirector = models.ForeignKey(Person, on_delete=models.CASCADE,
                                    related_name='director_of_film_making_situation_set', null=True)
    hasFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    hasPart = models.ForeignKey(ActingSituation, on_delete=models.CASCADE, null=True)
    hasProducer = models.ForeignKey(Person, on_delete=models.CASCADE,
                                    related_name='producer_of_film_making_situation_set', null=True)


class NominationSituation(UpsertMixin, Situation):
    # object properties
    forFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    hasAward = models.ForeignKey('Award', on_delete=models.CASCADE)
    hasAwardCategory = models.ForeignKey('AwardCategory', on_delete=models.CASCADE)
    hasAwardCeremony = models.ForeignKey('AwardCeremony', on_delete=models.CASCADE)
    isGivenTo = models.ForeignKey(Agent, on_delete=models.CASCADE)

    # data properties
    win = models.BooleanField()


class ContentRatingCategory(UpsertMixin, models.Model):
    hasValue = models.CharField(max_length=255)
    isPartOf = models.OneToOneField('ContentRating', on_delete=models.CASCADE, related_name='hasPart')


class ContentRating(UpsertMixin, models.Model):
    hasDescription = models.CharField(max_length=255)
    # data properties
    appliesInCountry = models.ForeignKey('Country', on_delete=models.PROTECT, null=True)


class Place(models.Model):
    pass  # Nothing


class Country(Place, UpsertMixin):
    # annotation property
    label = models.CharField(max_length=255)
    alpha_2 = models.CharField(max_length=2)
    alpha_3 = models.CharField(max_length=3)


class Genre(models.Model, UpsertMixin):
    # object properties
    hasSubGenre = models.ManyToManyField('Genre', related_name='isSubGenreOf', null=True)
    # isSubGenreOf = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, related_name='SubGenreOf_set', null=True)

    # temp
    label = models.CharField(max_length=255)
    wikidata_id = models.CharField(max_length=13)

    @classmethod
    def populate_film_subgenres_from_wikidata(cls):
        for genre, subgenre in get_genre_with_subgenres():
            subgenre = cls.upsert(wikidata_id=subgenre.wikidata_id, label=subgenre.label)
            genre = cls.upsert(wikidata_id=genre.wikidata_id, label=genre.label)
            genre.hasSubGenre.add(subgenre)
            genre.save()


class Language(UpsertMixin, models.Model):
    # annotation property
    label = models.CharField(max_length=255)


class AwardCeremony(UpsertMixin, models.Model):
    # object properties
    # follow = models.ForeignKey('AwardCeremony', on_delete=models.SET_NULL, related_name='followedBy', null=True)
    # followedBy = models.ForeignKey('AwardCeremony', on_delete=models.SET_NULL, null=True, null=True)
    hasAward = models.ForeignKey('Award', on_delete=models.CASCADE, null=True)

    # data properties
    # dateHeld = models.CharField(max_length=255)
    yearHeld = models.IntegerField()
    hasEditionNumber = models.IntegerField()
    yearScreened = models.IntegerField()

    @property
    def follow(self) -> typing.Optional['AwardCeremony']:
        try:
            return self.objects.get(hasEditionNumber=self.hasEditionNumber - 1)
        except self.DoesNotExist:
            return None

    @property
    def followedBy(self) -> typing.Optional['AwardCeremony']:
        try:
            return self.objects.get(hasEditionNumber=self.hasEditionNumber + 1)
        except self.DoesNotExist:
            return None

    @classmethod
    def upsert(cls,
               hasAward: 'Award',
               yearHeld: int,
               hasEditionNumber: int,
               yearScreened: int) -> 'AwardCeremony':
        kwds = {
            'hasAward': hasAward,
            'yearHeld': yearHeld,
            'hasEditionNumber': hasEditionNumber,
            'yearScreened': yearScreened
        }
        return super().upsert(**kwds)


def read_wiki_oscar_categories(filename: str) -> typing.List[str]:
    lst = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
    for line in lines:
        if not line:
            continue
        category = line.split(':')[0]
        lst.append(category)
    return lst


class AwardCategory(models.Model, UpsertMixin):
    # wiki_categories: typing.ClassVar[typing.List[str]] = read_wiki_oscar_categories(
    #     'mapping/oscar-categories.txt')

    # object properties
    forOccupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, null=True)

    # temp
    label = models.CharField(max_length=255)

    @classmethod
    def get_instance_from_kaggle_oscar_data(cls, category: str) -> 'AwardCategory':
        return cls.upsert(label=OSCAR_MAPPING[category])

    @classmethod
    def get_instance_from_kaggle_bafta_data(cls, category: str) -> 'AwardCategory':
        matched_str = re.match(r'^Film | (?P<category>.*)in (.*$)', category)
        return AwardCategory.upsert(label=matched_str['category'])
        # return cls


class Award(models.Model):
    # object properties
    hasAwardCategory = models.ForeignKey(AwardCategory, on_delete=models.CASCADE, null=True)
    hasPart = models.ForeignKey(AwardCeremony, on_delete=models.CASCADE, null=True)
    hasSetting = models.ForeignKey(NominationSituation, on_delete=models.CASCADE, null=True)
    presentedBy = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)

    # data properties
    hasNickname = models.CharField(max_length=255, null=True)

    # temp
    label = models.CharField(max_length=255)


class Audience(models.Model, UpsertMixin):
    # temp
    label = models.CharField(max_length=255)


class Organization(Agent):
    # data properties
    hasName = models.CharField(max_length=255)
    # temp
    label = models.CharField(max_length=255)


class MovieStudio(Organization):
    locatedIn = models.ForeignKey('Place', on_delete=models.CASCADE, null=True)


class Film(models.Model):
    # object properties
    # hasAudience = models.ForeignKey(Audience, on_delete=models.CASCADE, null=True)
    # TODO:  fetched from wikidata
    hasContentRating = models.ManyToManyField(ContentRatingCategory, null=True)
    # TODO:  fetched from wikidata
    hasCountryOfOrigin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='origin_country_of_films',
                                           null=True)
    # TODO:  fetched from wikidata
    hasFilmingLocation = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='filming_location_of_films',
                                           null=True)  # may not be in use
    hasGenre = models.ManyToManyField(Genre, null=True)
    # TODO: wikidata, imdb.TitleBasics
    hasLanguage = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='language_of_films', null=True)

    hasOriginalLanguage = models.ForeignKey(Language, on_delete=models.CASCADE,
                                            related_name='original_language_of_films', null=True)
    hasPrequels = models.ForeignKey('Film', on_delete=models.SET_NULL, related_name='hasSequels', null=True)
    # TODO: wikidata
    # hasSequels = models.ForeignKey('Film', on_delete=models.SET_NULL, null=True)
    # hasSubTitleInLanguage = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='subtitle_of_films', null=True)
    # eligibleFor = models.ForeignKey(Award, on_delete=models.CASCADE, null=True)

    # data properties
    dateReleased = models.CharField(max_length=255, null=True)  # models.DateField(, null=True)
    hasFeatureLengthInMinutes = models.IntegerField(null=True)
    hasInitialReleaseYear = models.IntegerField(null=True)
    hasTitle = models.CharField(max_length=255, null=True)
  #  hasWikipediaLink = models.CharField(max_length=255, null=True)  # models.URLField(, null=True)
    # isBritishFilm = models.BooleanField(null=True)
    isAdult = models.BooleanField(null=True)

    # wikidata
    hasWikidataId = models.CharField(null=True, max_length=13)

    # temp
    avg_rating = models.CharField(max_length=255, null=True)
    t_const = models.CharField(max_length=255, unique=True)

    @include
    def sync_from_wikidata(self):
        try:
            print(f'Syncing {self.hasTitle} with {self.t_const}')
            self.update_wikidata_id_from_imdb()
            self.update_content_rating_from_wikidata()
            self.update_country_of_origin_from_wikidata()
            print(f'Synced {self.hasTitle} with {self.t_const} [{self.hasWikidataId}]')
        except KeyError:
            pass

    def update_wikidata_id_from_imdb(self):
        self.hasWikidataId = get_from_imdb_id(self.t_const)
        if not self.hasWikidataId:
            raise ValueError("<WikidataId> Not found")
        self.save()

    def update_content_rating_from_wikidata(self):

            for cr in get_content_ratings_for_film(self.hasWikidataId):
                cr_model = ContentRating.upsert(appliesInCountry=Country.upsert(label=cr.appliesInCountry))
                category = ContentRatingCategory.upsert(hasValue=cr.value, isPartOf=cr_model)
                self.hasContentRating.add(category)
            self.save()

    def update_country_of_origin_from_wikidata(self):
        f = get_single_valued_prop(self.hasWikidataId)
        self.dateReleased = f.hasPublicationDate
        self.hasCountryOfOrigin = Country.upsert(label=f.hasCountryOfOrigin)
        self.hasOriginalLanguage = Language.upsert(label=f.hasOriginalLanguage)
        self.save()


class Character(models.Model):
    # object properties
    actedBy = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    hasGender = models.CharField(max_length=255, choices=Gender.choices, null=True)
    hasImportance = models.CharField(max_length=255, choices=CharacterImportance.choices, null=True)

    # data properties
    # hasCharacterTitle = models.CharField(max_length=255, null=True)
    hasName = models.CharField(max_length=255, null=True)
