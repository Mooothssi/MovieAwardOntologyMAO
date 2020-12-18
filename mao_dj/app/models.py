from django.db import models


class MaxLenMixin:
    @property
    def max_len(self):
        return max(map(self.choices))


class Gender(MaxLenMixin, models.TextChoices):
    FEMALE = 'female'
    MALE = 'male'
    NON_BINARY = 'non-binary'


class CharacterImportance(MaxLenMixin, models.TextChoices):
    MAIN = 'main'
    SIDE = 'side'
    EXTRA = 'extra'


class Occupation(models.Model):
    # object properties
    isOccupationof = models.ForeignKey('Person', on_delete=models.CASCADE)


class Person(models.Model):
    # object properties
    actsIn = models.ForeignKey('FilmMakingSituation', on_delete=models.CASCADE)
    hasGender = models.CharField(max_length=Gender.max_len, choices=Gender.choices)
    hasOccupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    eligibleFor = models.ForeignKey('Award', on_delete=models.CASCADE)

    # data properties
    hasName = models.CharField()


class CollectiveAgent(models.Model):
    # object properties
    isParticipantIn = models.ForeignKey('Situation', on_delete=models.CASCADE)
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
    hasCinematographer = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasComposer = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasCrew = models.ForeignKey(FilmCrew, on_delete=models.CASCADE)
    hasDirector = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasFilm = models.ForeignKey('Film', on_delete=models.CASCADE)
    hasPart = models.ForeignKey(ActingSituation, on_delete=models.CASCADE)
    hasProducer = models.ForeignKey(Person, on_delete=models.CASCADE)


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
    hasDescription = models.CharField()


class Place(models.Model):
    pass  # Nothing


class Country(Place):
    # annotation property
    label = models.CharField()


class Genre(models.Model):
    # object properties
    hasSubGenre = models.ForeignKey('Genre', on_delete=models.SET_NULL)
    isSubGenreOf = models.ForeignKey('Genre', on_delete=models.SET_NULL)


class Language(models.Model):
    # annotation property
    label = models.CharField()


class AwardCeremony(models.Model):
    # object properties
    follow = models.ForeignKey('AwardCeremony', on_delete=models.SET_NULL)
    followedBy = models.ForeignKey('AwardCeremony', on_delete=models.SET_NULL)
    hasAward = models.ForeignKey('Award', on_delete=models.CASCADE)

    # data properties
    dateHeld = models.CharField()
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
    presentedBy = models.ForeignKey('', on_delete=models.CASCADE)

    # data properties
    hasNickname = models.CharField()


class Audience(models.Model):
    # temp
    label = models.CharField()


class Organization(models.Model):
    # temp
    label = models.CharField()


class MovieStudio(Organization):
    locatedIn = models.ForeignKey('Place', on_delete=models.CASCADE)


class Film(models.Model):
    # object properties
    hasAudience = models.ForeignKey(Audience, on_delete=models.CASCADE)
    hasContentRating = models.ForeignKey(ContentRating, on_delete=models.CASCADE)
    hasCountryOfOrigin = models.ForeignKey(Country, on_delete=models.CASCADE)
    hasFilmingLocation = models.ForeignKey(Place, on_delete=models.CASCADE)  # may not be in use
    hasGenre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    hasLanguage = models.ForeignKey(Language, on_delete=models.CASCADE)
    hasOriginalLanguage = models.ForeignKey(Language, on_delete=models.CASCADE)
    hasPrequels = models.ForeignKey('Film', on_delete=models.SET_NULL)
    hasSequels = models.ForeignKey('Film', on_delete=models.SET_NULL)
    hasSubTitleInLanguage = models.ForeignKey(Language, on_delete=models.CASCADE)
    eligibleFor = models.ForeignKey(Award, on_delete=models.CASCADE)

    # data properties
    dateReleased = models.CharField()  # models.DateField()
    hasFeatureLengthInMinutes = models.IntegerField()
    hasInitialReleaseYear = models.IntegerField()
    hasTitle = models.CharField()
    hasWikipediaLink = models.CharField()  # models.URLField()
    isBritishFilm = models.BooleanField()
    isAdult = models.BooleanField()

    # temp
    avg_rating = models.CharField()


class Character(models.Model):
    # object properties
    actedBy = models.ForeignKey(Person, on_delete=models.CASCADE)
    hasGender = models.CharField(max_length=Gender.max_len, choices=Gender.choices)
    hasImportance = models.CharField(max_length=CharacterImportance.max_len, choices=CharacterImportance.choices)

    # data properties
    hasCharacterTitle = models.CharField()
    hasName = models.CharField()
