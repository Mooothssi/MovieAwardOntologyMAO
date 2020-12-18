from django.db import models


# class MaxLenMixin:
#     @property
#     def max_len(self):
#         return max(map(self.choices))


class Gender(models.TextChoices):
    FEMALE = 'female'
    MALE = 'male'
    NON_BINARY = 'non-binary'


class CharacterImportance(models.TextChoices):
    MAIN = 'main'
    SIDE = 'side'
    EXTRA = 'extra'


class Occupation(models.Model):
    # object properties
    isOccupationof = models.ForeignKey('Person', on_delete=models.CASCADE)


class Person(models.Model):
    # object properties
    actsIn = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE)
    hasGender = models.CharField(max_length=255, choices=Gender.choices)
    hasOccupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    eligibleFor = models.ForeignKey('Award', on_delete=models.CASCADE)

    # data properties
    hasName = models.CharField(max_length=255)


class CollectiveAgent(models.Model):
    # object properties
    # isParticipantIn = models.ForeignKey('Situation', on_delete=models.CASCADE)
    hasMember = models.ForeignKey(Person, on_delete=models.CASCADE)


class FilmCast(CollectiveAgent):
    # object properties
    isParticipantIn = models.ForeignKey('ActingSituation', on_delete=models.CASCADE)


class FilmCrew(CollectiveAgent):
    # object properties
    isParticipantIn = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE)


class Situation(models.Model):
    # object properties
    isSettingFor = models.ForeignKey('Award', on_delete=models.CASCADE)  # actually owl:Thing


class ActingSituation(Situation):
    # object properties
    hasActor = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasCharacter = models.ForeignKey('Character', on_delete=models.CASCADE)
    hasFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    isPartOf = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE)


class FilmMakingSituation(Situation):
    # object proerties
    hasCast = models.ForeignKey(FilmCast, on_delete=models.CASCADE)
    hasCinematographer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='cinematographer_of_film_making_situation_set')
    hasComposer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='composer_of_film_making_situation_set')
    hasCrew = models.ForeignKey(FilmCrew, on_delete=models.CASCADE)
    hasDirector = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='director_of_film_making_situation_set')
    hasFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    hasPart = models.ForeignKey(ActingSituation, on_delete=models.CASCADE)
    hasProducer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='producer_of_film_making_situation_set')


class NominationSituation(Situation):
    # object properties
    forFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    hasAward = models.ForeignKey('Award', on_delete=models.CASCADE)
    hasAwardCategory = models.ForeignKey('AwardCategory', on_delete=models.CASCADE)
    hasAwardCeremony = models.ForeignKey('AwardCeremony', on_delete=models.CASCADE)
    isGivenTo = models.ForeignKey(Person, on_delete=models.CASCADE)

    # data properties
    win = models.BooleanField()


class ContentRating(models.Model):
    # data properties
    hasDescription = models.CharField(max_length=255)


class Place(models.Model):
    pass  # Nothing


class Country(Place):
    # annotation property
    label = models.CharField(max_length=255)


class Genre(models.Model):
    # object properties
    hasSubGenre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, related_name='isSubGenreOf')
    # isSubGenreOf = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, related_name='SubGenreOf_set')


class Language(models.Model):
    # annotation property
    label = models.CharField(max_length=255)


class AwardCeremony(models.Model):
    # object properties
    follow = models.ForeignKey('AwardCeremony', on_delete=models.SET_NULL, null=True, related_name='followedBy')
    # followedBy = models.ForeignKey('AwardCeremony', on_delete=models.SET_NULL, null=True)
    hasAward = models.ForeignKey('Award', on_delete=models.CASCADE)

    # data properties
    dateHeld = models.CharField(max_length=255)
    hasEditionNumber = models.IntegerField()
    yearScreened = models.IntegerField()


class AwardCategory(models.Model):
    # object properties
    forOccupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)


class Award(models.Model):
    # object properties
    hasAwardCategory = models.ForeignKey(AwardCategory, on_delete=models.CASCADE)
    hasPart = models.ForeignKey(AwardCeremony, on_delete=models.CASCADE)
    hasSetting = models.ForeignKey(NominationSituation, on_delete=models.CASCADE)
    presentedBy = models.ForeignKey('Organization', on_delete=models.CASCADE)

    # data properties
    hasNickname = models.CharField(max_length=255)


class Audience(models.Model):
    # temp
    label = models.CharField(max_length=255)


class Organization(models.Model):
    # temp
    label = models.CharField(max_length=255)


class MovieStudio(Organization):
    locatedIn = models.ForeignKey('Place', on_delete=models.CASCADE)


class Film(models.Model):
    # object properties
    hasAudience = models.ForeignKey(Audience, on_delete=models.CASCADE)
    hasContentRating = models.ForeignKey(ContentRating, on_delete=models.CASCADE)
    hasCountryOfOrigin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='origin_country_of_films')
    hasFilmingLocation = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='filming_location_of_films')  # may not be in use
    hasGenre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    hasLanguage = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='language_of_films')
    hasOriginalLanguage = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='original_language_of_films')
    hasPrequels = models.ForeignKey('Film', on_delete=models.SET_NULL, related_name='hasSequels', null=True)
    # hasSequels = models.ForeignKey('Film', on_delete=models.SET_NULL)
    hasSubTitleInLanguage = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='subtitle_of_films')
    eligibleFor = models.ForeignKey(Award, on_delete=models.CASCADE)

    # data properties
    dateReleased = models.CharField(max_length=255)  # models.DateField()
    hasFeatureLengthInMinutes = models.IntegerField()
    hasInitialReleaseYear = models.IntegerField()
    hasTitle = models.CharField(max_length=255)
    hasWikipediaLink = models.CharField(max_length=255)  # models.URLField()
    isBritishFilm = models.BooleanField()
    isAdult = models.BooleanField()

    # temp
    avg_rating = models.CharField(max_length=255)


class Character(models.Model):
    # object properties
    actedBy = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasGender = models.CharField(max_length=255, choices=Gender.choices)
    hasImportance = models.CharField(max_length=255, choices=CharacterImportance.choices)

    # data properties
    hasCharacterTitle = models.CharField(max_length=255)
    hasName = models.CharField(max_length=255)
