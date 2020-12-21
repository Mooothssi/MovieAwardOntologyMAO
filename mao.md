version v2.1.0

# IRI
http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#

# Prefixes
## dc
http://purl.org/dc/elements/1.1/

## dcterms
http://purl.org/dc/terms/

## mao
http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#


# Class Hierarchy
- owl:Thing
  - mao:Abstract
    - mao:Classification
      - mao:AwardCategory
      - mao:ContentRatingClassification
      - mao:Gender
      - mao:Genre
      - mao:Nationality
      - mao:Race
    - mao:Language
  - mao:Event
    - mao:FilmMakingSituation
  - mao:Object
    - mao:Agent
      - mao:Character
      - mao:CharacterImportance
      - mao:CollectiveAgent
        - mao:Audience
        - mao:FilmCast
        - mao:FilmCrew
      - mao:Organization
        - mao:MovieStudio
      - mao:Person
    - mao:AggregateRating
    - mao:Award
    - mao:AwardCeremony
    - mao:ContentRatingCategory
    - mao:Film
      - mao:FilmEligibleForOscars
    - mao:Occupation
    - mao:Place
      - mao:City
      - mao:Country
    - mao:Rating
    - mao:Review
    - mao:Situation
      - mao:ActingSituation
      - mao:FilmMakingSituation
      - mao:NominationSituation
        - mao:AwardReceivedSituation
        - mao:NominatedForSituation
      - mao:VoiceActingSituation
  - mao:Value
    - mao:NormativeValue
      - mao:Criterion
      - mao:Requirement

# Property Hierarchy
### Object Property
- owl:TopObjectProperty
  - mao:actedBy
  - mao:actsIn
  - mao:appliesInCountry
  - mao:coparticipatesWith
  - mao:eligibleFor
  - mao:follow
  - mao:followedBy
  - mao:forFilm
  - mao:forOccupation
  - mao:hasActor
  - mao:hasArchetype
  - mao:hasAudience
  - mao:hasAuthor
  - mao:hasAward
  - mao:hasAwardCategory
  - mao:hasAwardCeremony
  - mao:hasCast
  - mao:hasCharacter
  - mao:hasCinematographer
  - mao:hasComposer
  - mao:hasContentRating
  - mao:hasCountryOfOrigin
  - mao:hasCrew
  - mao:hasDirector
  - mao:hasException
  - mao:hasFilm
  - mao:hasFilmStudio
  - mao:hasFilmingLocation
  - mao:hasGender
  - mao:hasGenre
  - mao:hasImportance
  - mao:hasLanguage
  - mao:hasMember
  - mao:hasOccupation
  - mao:hasOriginalLanguage
  - mao:hasPart
  - mao:hasParticipant
    - mao:involvesAgent
  - mao:hasPrequels
  - mao:hasProducer
  - mao:hasReviewAggregator
  - mao:hasRole
  - mao:hasSequels
  - mao:hasSetting
  - mao:hasSubGenre
  - mao:hasSubTitleInLanguage
  - mao:hasVoiceActor
  - mao:isAffectedByValidityOf
  - mao:isGivenTo
  - mao:isOccupationOf
  - mao:isPartOf
  - mao:isParticipantIn
    - mao:isAgentInvolvedIn
  - mao:isSatisfiedBy
  - mao:isSettingFor
  - mao:isSubGenreOf
  - mao:isValidFor
    - mao:isCriterionFor
    - mao:isRequirementFor
  - mao:isViolatedBy
  - mao:locatedIn
  - mao:presentedBy
  - mao:reviewOf
  - mao:satisfies
    - mao:satisfiesCriterion
    - mao:satisfiesRequirement
  - mao:satisfiesCriterionFor
  - mao:setBy
  - mao:violates
    - mao:violatesCriterion
    - mao:violatesRequirement
  - mao:violatesCriterionFor
  - owl:topObjectProperty

### Data Property
- owl:TopDataProperty
  - mao:dateHeld
  - mao:dateReleased
  - mao:hasAggregateRating
  - mao:hasContent
  - mao:hasCount
  - mao:hasDescription
  - mao:hasEditionNumber
  - mao:hasFeatureLengthInMinutes
  - mao:hasInitialReleaseYear
  - mao:hasMaxValue
  - mao:hasMinValue
  - mao:hasName
  - mao:hasNickname
  - mao:hasSource
  - mao:hasTitle
  - mao:hasValue
  - mao:hasWikipediaLink
  - mao:isAdult
  - mao:isBritishFilm
  - mao:win
  - mao:yearScreened
  - owl:topDataProperty

### Annotation Property
- dcterms:license
- dc:title

# Ontology Description
### Annotations
Title

| Language | Title |
|----------|-------|
| English  | Movie Awards Ontology |

License
  - Copyright 2020 MAO Team
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Version Info
  - 1.0.18

Label

| Language | Label |
|----------|-------|
| English  | Movie Awards Ontology |

Comment

| Language | Comment |
|----------|---------|
| English  | An ontology about movies and awards |


# Classes
## owl:Thing
## mao:Abstract
### Annotations
Comment
  - Any Entity that cannot be located in space-time. E.g. mathematical entities: formal semantics elements, regions within dimensional spaces, etc.

Label

| Language | Label |
|----------|-------|
| English  | Abstract |

### Description
Subclass of:
  - owl:Thing

Disjoint with:
  - mao:Event
  - mao:Object
  - mao:Value

## mao:ActingSituation
### Annotations
Comment
  - A set of circumstances in which one finds about acting

Label

| Language | Label |
|----------|-------|
| English  | ActingSituation |

### Description
Subclass of:
  - mao:Situation

Disjoint with:
  - mao:FilmMakingSituation
  - mao:NominationSituation
  - mao:VoiceActingSituation

### Object Properties
  - hasActor
  - hasCharacter
  - hasFilm
  - isPartOf

## mao:Agent
### Annotations
Comment
  - Additional comment: a computational agent can be considered as a PhysicalAgent that realizes a certain class of algorithms (that can be considered as instances of InformationObject) that allow to obtain some behaviors that are considered typical of agents in general. For an ontology of computational objects based on DOLCE see e.g. http://www.loa-cnr.it/COS/COS.owl, and http://www.loa-cnr.it/KCO/KCO.owl.

Label

| Language | Label |
|----------|-------|
| English  | Agent |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

## mao:AggregateRating
### Annotations
Comment
  - A whole formed by combining several rating

Label

| Language | Label |
|----------|-------|
| English  | AggregateRating |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:Award
  - mao:AwardCeremony
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

### Object Properties
  - hasPart
  - hasReviewAggregator

### Data Properties
  - hasCount
  - hasMaxValue
  - hasMinValue
  - hasName
  - hasSource
  - hasValue

## mao:Audience
### Annotations
Comment
  - The assembled spectators or listeners at a public event, such as a movie

Label

| Language | Label |
|----------|-------|
| English  | Audience |

### Description
Subclass of:
  - mao:CollectiveAgent

Disjoint with:
  - mao:FilmCast
  - mao:FilmCrew

## mao:Award
### Annotations
Comment
  - A prize or other mark of recognition given in honor of an achievement

Label

| Language | Label |
|----------|-------|
| English  | Award |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

### Object Properties
  - hasAwardCategory
  - hasPart
  - hasSetting
  - presentedBy

### Data Properties
  - hasNickname

## mao:AwardCategory
### Annotations
Comment
  - A class or division of award regarded as having particular shared characteristics

Label

| Language | Label |
|----------|-------|
| English  | AwardCategory |

### Description
Subclass of:
  - mao:Classification

Disjoint with:
  - mao:ContentRatingCategory
  - mao:Genre
  - mao:Gender
  - mao:Nationality
  - mao:Race

### Object Properties
  - forOccupation

## mao:AwardCeremony
### Annotations
Comment
  - A formal act or series of acts prescribed by ritual, protocol, or convention about award

Label

| Language | Label |
|----------|-------|
| English  | AwardCeremony |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

### Object Properties
  - follow
  - followedBy
  - hasAward

### Data Properties
  - dateHeld
  - hasEditionNumber
  - yearScreened

## mao:AwardReceivedSituation
### Annotations
Comment
  - A set of circumstances in which one finds about award receiving

Label

| Language | Label |
|----------|-------|
| English  | AwardReceivedSituation |

### Description
Subclass of:
  - mao:NominationSituation

Disjoint with:
  - mao:NominatedForSituation

Equivalent to:
  - mao:NominationSituation and (win value True)

## mao:Character
### Annotations
Comment
  - Character in film

Label

| Language | Label |
|----------|-------|
| English  | Character |

### Description
Subclass of:
  - mao:Agent

Disjoint with:
  - mao:CharacterImportance
  - mao:CollectiveAgent
  - mao:Organization
  - mao:Person

### Object Properties
  - actedBy
  - hasArchetype
  - hasGender
  - hasImportance
  - hasRole

### Data Properties
  - hasName

## mao:CharacterImportance
### Annotations
Comment
  - The state or fact of being of significance or value of character

Label

| Language | Label |
|----------|-------|
| English  | CharacterImportance |

### Description
Subclass of:
  - mao:Agent

Disjoint with:
  - mao:Character
  - mao:CollectiveAgent
  - mao:Organization
  - mao:Person

## mao:City
### Annotations
Comment
  - A large town

Label

| Language | Label |
|----------|-------|
| English  | City  |

### Description
Subclass of:
  - mao:Place

Disjoint with:
  - mao:Country

## mao:Classification
### Annotations
Comment
  - A special kind of Situation that allows to include time indexing for the classifies relation in situations

Label

| Language | Label |
|----------|-------|
| English  | Classification |

### Description
Subclass of:
  - mao:Abstract

Disjoint with:
  - mao:Language

## mao:CollectiveAgent
### Annotations
Comment
  - A SocialAgent that is actedBy agents that are (and act as) members of a Collective. A collective agent can have roles that are also roles of those agents

Label

| Language | Label |
|----------|-------|
| English  | CollectiveAgent |

### Description
Subclass of:
  - mao:Agent

Disjoint with:
  - mao:Character
  - mao:CharacterImportance
  - mao:Organization
  - mao:Person

### Object Properties
  - isParticipantIn
  - hasMember

## mao:ContentRatingCategory
### Annotations
Comment
  - A classification or ranking of content based on a comparative assessment of quality, standard, or performance

Label

| Language | Label |
|----------|-------|
| English  | Category |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

### Object Properties
  - appliesInCountry

### Data Properties
  - hasDescription

## mao:ContentRatingClassification
### Annotations
Comment
  - The action or process of classifying content rating according to shared qualities or characteristics

Label

| Language | Label |
|----------|-------|
| English  | Classification |

### Description
Subclass of:
  - mao:Classification

Disjoint with:
  - mao:AwardCategory
  - mao:Gender
  - mao:Genre
  - mao:Nationality
  - mao:Race

### Object Properties
  - isPartOf

### Data Properties
  - hasValue

## mao:Country
### Annotations
Comment
  - A nation with its own government, occupying a particular territory

Label

| Language | Label |
|----------|-------|
| English  | Country |

### Description
Subclass of:
  - mao:Place

Disjoint with:
  - mao:City

## mao:Criterion
### Annotations
Comment
  - A principle or standard which may be judged or decided

Label

| Language | Label |
|----------|-------|
| English  | Criterion |

### Description
Subclass of:
  - mao:NormativeValue

Disjoint with:
  - mao:Requirement

### Object Properties
  - isCriterionFor
  - setBy

## mao:Event
### Annotations
Comment
  - Any physical, social, or mental process, event, or state.
More theoretically, events can be classified in different ways, possibly based on 'aspect' (e.g. stative, continuous, accomplishement, achievement, etc.), on 'agentivity' (e.g. intentional, natural, etc.), or on 'typical participants' (e.g. human, physical, abstract, food, etc.). Here no special direction is taken, and the following explains why: events are related to observable situations, and they can have different views at a same time. If a position has to be suggested here anyway, the participant-based classification of events seems the most stable and appropriate for many modelling problems.
(1) Alternative aspectual views
Consider a same event 'rock erosion in the Sinni valley': it can be conceptualized as an accomplishment (what has brought a certain state to occur), as an achievement (the state resulting from a previous accomplishment), as a punctual event (if we collapse the time interval of the erosion into a time point), or as a transition (something that has changed from a state to a different one). In the erosion case, we could therefore have good motivations to shift from one aspect to another: a) causation focus, b) effectual focus, c) historical condensation, d) transition (causality).
The different views refer to the same event, but are still different: how to live with this seeming paradox? A typical solution e.g. in linguistics (cf. Levin's aspectual classes) and in DOLCE Full (cf. WonderWeb D18 axiomatization) is to classify events based on aspectual differences. But this solution would create different identities for a same event, where the difference is only based on the modeller's attitude. An alternative solution is applied here, and exploits the notion of (observable) Situation; a Situation is a view, consistent with a Description, which can be observed of a set of entities. It can also be seen as a 'relational context' created by an observer on the basis of a 'frame'. Therefore, a Situation allows to create a context where each particular view can have a proper identity, while the Event preserves its own identity. For example, ErosionAsAccomplishment is a Situation where rock erosion is observed as a process leading to a certain achievement: the conditions (roles, parameters) that suggest such view are stated in a Description, which acts as a 'theory of accomplishments'. Similarly, ErosionAsTransition is a Situation where rock erosion is observed as an event that has changed a state to another: the conditions for such interpretation are stated in a different Description, which acts as a 'theory of state transitions'. Consider that in no case the actual event is changed or enriched in parts by the aspectual view.
(2) Alternative intentionality views
Similarly to aspectual views, several intentionality views can be provided for a same Event. For example, one can investigate if an avalanche has been caused by immediate natural forces, or if there is any hint of an intentional effort to activate those natural forces. Also in this case, the Event as such has not different identities, while the causal analysis generates situations with different identities, according to what Description is taken for interpreting the Event. On the other hand, if the possible actions of an Agent causing the starting of an avalanche are taken as parts of the Event, then this makes its identity change, because we are adding a part to it. Therefore, if intentionality is a criterion to classify events or not, this depends on if an ontology designer wants to consider causality as a relevant dimension for events' identity.
(3) Alternative participant views
A slightly different case is when we consider the basic participants to an Event. In this case, the identity of the Event is affected by the participating objects, because it depends on them. For example, if snow, mountain slopes, wind, waves, etc. are considered as an avalanche basic participants, or if we also want to add water, human agents, etc., that makes the identity of an avalanche change. Anyway, this approach to event classification is based on the designer's choices, and more accurately mirrors lexical or commonsense classifications (see. e.g. WordNet 'supersenses' for verb synsets).
Ultimately, this discussion has no end, because realists will keep defending the idea that events in reality are not changed by the way we describe them, while constructivists will keep defending the idea that, whatever 'true reality' is about, it can't be modelled without the theoretical burden of how we observe and describe it. Both positions are in principle valid, but, if taken too radically, they focus on issues that are only partly relevant to the aim of computational ontologies, which only attempt to assist domain experts in representing what they want to conceptualize a certain portion of reality according to their own ideas. For this reason, in this ontology both events and situations are allowed, together with descriptions, in order to encode the modelling needs, independently from the position (if any) chosen by the designer.

Label

| Language | Label |
|----------|-------|
| English  | Event |

### Description
Subclass of:
  - owl:Thing

Disjoint with:
  - mao:Abstract
  - mao:Object
  - mao:Value

### Object Properties
  - hasParticipant
  - involvesAgent

## mao:Film
### Annotations
Comment
  - The moving picture

Label

| Language | Label |
|----------|-------|
| English  | Film  |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

### Object Properties
  - hasAudience
  - hasContentRating
  - hasCountryOfOrigin
  - hasFilmingLocation
  - hasGenre
  - hasLanguage
  - hasOriginalLanguage
  - hasPrequels
  - hasSequels
  - hasSubTitleInLanguage
  - eligibleFor

### Data Properties
  - dateReleased
  - hasAggregateRating
  - hasFeatureLengthInMinutes
  - hasInitialReleaseYear
  - hasTitle
  - hasWikipediaLink
  - isAdult
  - isBritishFilm

## mao:FilmCast
### Annotations
Comment
  - The process of making casts or molds about filming

Label

| Language | Label |
|----------|-------|
| English  | FilmCast |

### Description
Subclass of:
  - mao:CollectiveAgent

Disjoint with:
  - mao:Audience
  - mao:FilmCrew

Equivalent to:
  - mao:CollectiveAgent and (isParticipantIn some ActingSituation)

## mao:FilmCrew
### Annotations
Comment
  - A group of people who work closely together about filming

Label

| Language | Label |
|----------|-------|
| English  | FilmCrew |

### Description
Subclass of:
  - mao:CollectiveAgent

Disjoint with:
  - mao:Audience
  - mao:FilmCast

Equivalent to:
  - mao:CollectiveAgent and (isParticipantIn some FilmMakingSituation)

## mao:FilmMakingSituation
### Annotations
Comment
  - A set of circumstances in which one finds about film making

Label

| Language | Label |
|----------|-------|
| English  | FilmMakingSituation |

### Description
Subclass of:
  - mao:Event
  - mao:Situation

### Object Properties
  - hasCast
  - hasCinematographer
  - hasComposer
  - hasCrew
  - hasDirector
  - hasFilm
  - hasPart
  - hasProducer

## mao:Gender
### Annotations
Comment
  - The socially constructed roles and behaviors that a society typically associates with males and females

Label

| Language | Label |
|----------|-------|
| English  | Gender |

### Description
Subclass of:
  - mao:Classification

Disjoint with:
  - mao:AwardCategory
  - mao:ContentRatingClassification
  - mao:Genre
  - mao:Nationality
  - mao:Race

Equivalent to:
  - mao:{Female, Male, Non-binary}

## mao:Genre
### Annotations
Comment
  - A category of composition characterized by similarities in form, style, or subject matter

Label

| Language | Label |
|----------|-------|
| English  | Genre |

### Description
Subclass of:
  - mao:Classification

Disjoint with:
  - mao:AwardCategory
  - mao:ContentRatingClassification
  - mao:Gender
  - mao:Nationality
  - mao:Race

### Object Properties
  - hasSubGenre
  - isSubGenreOf

## mao:Language
### Annotations
Comment
  - The principal method of human communication

Label

| Language | Label |
|----------|-------|
| English  | Language |

### Description
Subclass of:
  - mao:Abstract

Disjoint with:
  - mao:Classification

## mao:MovieStudio
### Annotations
Comment
  - A room, building, or group of buildings where movies are produced

Label

| Language | Label |
|----------|-------|
| English  | MovieStudio |

### Description
Subclass of:
  - mao:Organization

### Object Properties
  - locatedIn

## mao:Nationality
### Annotations
Comment
  - The status of belonging to a particular nation

Label

| Language | Label |
|----------|-------|
| English  | Nationality |

### Description
Subclass of:
  - mao:Classification

Disjoint with:
  - mao:AwardCategory
  - mao:ContentRatingClassification
  - mao:Gender
  - mao:Genre
  - mao:Race

## mao:NominatedForSituation
### Annotations
Comment
  - Being suggested by someone for a set of circumstances

Label

| Language | Label |
|----------|-------|
| English  | NominatedForSituation |

### Description
Subclass of:
  - mao:NominationSituation

Disjoint with:
  - mao:AwardReceivedSituation

Equivalent to:
  - mao:NominationSituation and (win value False)

## mao:NominationSituation
### Annotations
Comment
  - A set of circumstances in which one finds about nomination

Label

| Language | Label |
|----------|-------|
| English  | NominationSituation |

### Description
Subclass of:
  - mao:Situation

Disjoint with:
  - mao:ActingSituation
  - mao:FilmMakingSituation
  - mao:VoiceActingSituation

### Object Properties
  - forFilm
  - hasAward
  - hasAwardCategory
  - hasAwardCeremony
  - isGivenTo

### Data Properties
  - win

## mao:NormativeValue
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | Value that can serve as a norm, standard, codex, requirement, criterion etc. |

Label

| Language | Label |
|----------|-------|
| English  | Normative value |

### Description
Subclass of:
  - mao:Value

## mao:Object
### Annotations
Comment
  - Any physical, social, or mental object, or a substance. Following DOLCE Full, objects are always participating in some event (at least their own life), and are spatially located.

Label

| Language | Label |
|----------|-------|
| English  | Object |

### Description
Subclass of:
  - owl:Thing

Disjoint with:
  - mao:Abstract
  - mao:Event
  - mao:Value

### Object Properties
  - coparticipatesWith
  - isParticipantIn

## mao:Occupation
### Annotations
Comment
  - A job or profession

Label

| Language | Label |
|----------|-------|
| English  | Occupation |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Place
  - mao:Rating
  - mao:Review
  - mao:Situation

### Object Properties
  - isOccupationOf

## mao:Organization
### Annotations
Comment
  - An organized body of people with a particular purpose

Label

| Language | Label |
|----------|-------|
| English  | Organization |

### Description
Subclass of:
  - mao:Agent

Disjoint with:
  - mao:Character
  - mao:CharacterImportance
  - mao:CollectiveAgent
  - mao:Person

### Data Properties
  - hasName

## mao:Place
### Annotations
Comment
  - A location, in a very generic sense: a political geographic entity, a non-material location determined by the presence of other entities, pivot events or signs, complements of other entities, etc. In this generic sense, a Place is an approximate location.

Label

| Language | Label |
|----------|-------|
| English  | Place |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Rating
  - mao:Review
  - mao:Situation

## mao:Person
### Annotations
Comment
  - Persons in commonsense intuition, which does not apparently distinguish between either natural or social persons.

Label

| Language | Label |
|----------|-------|
| English  | Person |

### Description
Subclass of:
  - mao:Agent

Disjoint with:
  - mao:Character
  - mao:CharacterImportance
  - mao:CollectiveAgent
  - mao:Organization

### Object Properties
  - isParticipantIn
  - hasGender
  - hasOccupation
  - eligibleFor

### Data Properties
  - hasName

## mao:Race
### Annotations
Comment
  - A group of people sharing the same culture, history, language, etc.

Label

| Language | Label |
|----------|-------|
| English  | Race  |

### Description
Subclass of:
  - mao:Classification

Disjoint with:
  - mao:AwardCategory
  - mao:ContentRatingClassification
  - mao:Gender
  - mao:Genre
  - mao:Nationality

## mao:Rating
### Annotations
Comment
  - A classification or ranking based on a comparative assessment of quality, standard, or performance

Label

| Language | Label |
|----------|-------|
| English  | Rating |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Review
  - mao:Situation

### Object Properties
  - hasAuthor
  - hasReviewAggregator
  - isPartOf
  - reviewOf

### Data Properties
  - hasMaxValue
  - hasMinValue
  - hasValue

## mao:Requirement
### Annotations
Comment
  - A thing that is compulsory

Label

| Language | Label |
|----------|-------|
| English  | Requirement |

### Description
Subclass of:
  - mao:NormativeValue

Disjoint with:
  - mao:Criterion

### Object Properties
  - isRequirementFor
  - satisfiesRequirement
  - violatesRequirement

## mao:Review
### Annotations
Comment
  - A published critical appraisal

Label

| Language | Label |
|----------|-------|
| English  | Review |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Situation

### Object Properties
  - hasAuthor
  - hasLanguage
  - hasPart
  - hasReviewAggregator
  - reviewOf

### Data Properties
  - hasContent

## mao:Situation
### Annotations
Comment
  - A view, consistent with ('satisfying') a Description, on a set of entities. It can also be seen as a 'relational context' created by an observer on the basis of a 'frame' (i.e. a Description). For example, a PlanExecution is a context including some actions executed by agents according to certain parameters and expected tasks to be achieved from a Plan; a DiagnosedSituation is a context of observed entities that is interpreted on the basis of a Diagnosis, etc. Situation is also able to represent reified n-ary relations, where isSettingFor is the top-level relation for all binary projections of the n-ary relation. If used in a transformation pattern for n-ary relations, the designer should take care of creating only one subclass of Situation for each n-ary relation, otherwise the 'identification constraint' (Calvanese et al., IJCAI 2001) could be violated.

Label

| Language | Label |
|----------|-------|
| English  | Situation |

### Description
Subclass of:
  - mao:Object

Disjoint with:
  - mao:Agent
  - mao:AggregateRating
  - mao:Award
  - mao:AwardCeremony
  - mao:ContentRatingCategory
  - mao:Film
  - mao:Occupation
  - mao:Place
  - mao:Rating
  - mao:Review

### Object Properties
  - isSettingFor

## mao:Value
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | Value is everything that has validity for something and what determines how it would be satisfied. Examples: self-interest, reliability, warranty, benefit, norm, requirement, criterion, recommendation... |

Label

| Language | Label |
|----------|-------|
| English  | Value |

### Description
Subclass of:
  - owl:Thing

Disjoint with:
  - mao:Abstract
  - mao:Event
  - mao:Object

### Object Properties
  - hasException
  - isAffectedByValidityOf
  - isSatisfiedBy
  - isValidFor
  - isViolatedBy
  - satisfies
  - violates

## mao:VoiceActingSituation
### Annotations
Comment
  - A set of circumstances in which one finds about voice acting

Label

| Language | Label |
|----------|-------|
| English  | VoiceActingSituation |

### Description
Subclass of:
  - mao:Situation

Disjoint with:
  - mao:ActingSituation
  - mao:FilmMakingSituation
  - mao:NominationSituation

### Object Properties
  - hasVoiceActor
  - hasCharacter
  - hasFilm
  - isPartOf

## mao:FilmEligibleForOscars
### Description
Subclass of:
  - mao:Film

Equivalent to:
  - mao:Film and (satisfiesCriterionFor some Award) and (not(violatesCriterionFor some Award))


# Object Properties
## owl:topObjectProperty
## mao:actedBy
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | acted by |

### Description
Range:
  - mao:Person

## mao:actsIn
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | acts in |

### Description
Range:
  - mao:FilmMakingSituation

## mao:appliesInCountry
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | applies in country |

### Description
Range:
  - mao:Country

## mao:coparticipatesWith
### Annotations
Comment
  - A relation between two objects participating in a same Event; e.g., 'Vitas and Jimmy are playing tennis'.

Label

| Language | Label |
|----------|-------|
| English  | co-participates with |

### Description
Domain:
  - mao:Object

Range:
  - mao:Object

## mao:eligibleFor
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | eligible for |

### Description
Range:
  - mao:AwardCategory

## mao:follow
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | follow |

### Description
Range:
  - mao:AwardCeremony

## mao:followedBy
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | followed by |

### Description
Range:
  - mao:AwardCategory

## mao:forFilm
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | for film |

### Description
Domain:
  - mao:NominationSituation

Range:
  - mao:Film

## mao:forOccupation
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | for occupation |

### Description
Domain:
  - mao:AwardCategory

Range:
  - mao:Occupation

## mao:hasActor
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has actor |

### Description
Range:
  - mao:Person

## mao:hasArchetype
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has archetype |

## mao:hasAudience
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has audience |

### Description
Range:
  - mao:Audience

## mao:hasAuthor
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has author |

### Description
Range:
  - mao:Agent

## mao:hasAward
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has award |

### Description
Range:
  - mao:Award

## mao:hasAwardCategory
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has award category |

### Description
Range:
  - mao:AwardCategory

## mao:hasAwardCeremony
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has award ceremony |

### Description
Range:
  - mao:AwardCeremony

## mao:hasCast
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has cast |

### Description
Range:
  - mao:FilmCast

## mao:hasCharacter
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has character |

### Description
Range:
  - mao:Character

## mao:hasCinematographer
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has cinematographer |

### Description
Range:
  - mao:Person

## mao:hasComposer
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has composer |

### Description
Range:
  - mao:Person

## mao:hasContentRating
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has content rating |

### Description
Range:
  - mao:ContentRatingClassification

## mao:hasCountryOfOrigin
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has country of origin |

### Description
Range:
  - mao:Country

## mao:hasCrew
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has crew |

### Description
Range:
  - mao:FilmCrew

## mao:hasDirector
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has director |

### Description
Range:
  - mao:Person

## mao:hasException
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has exception |

### Description
Domain:
  - mao:Value

Range:
  - owl:Thing

## mao:hasFilm
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has Film |

### Description
Range:
  - mao:Film

## mao:hasFilmingLocation
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has filming location |

### Description
Range:
  - mao:Place

## mao:hasFilmStudio
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has film studio |

### Description
Range:
  - mao:MovieStudio

## mao:hasGender
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has gender |

### Description
Range:
  - mao:Gender

## mao:hasGenre
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has genre |

### Description
Range:
  - mao:Genre

## mao:hasImportance
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has importance |

### Description
Range:
  - mao:CharacterImportance

## mao:hasLanguage
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has language |

### Description
Range:
  - mao:Language

## mao:hasMember
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has member |

### Description
Range:
  - mao:Person

## mao:hasOccupation
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has occupation |

### Description
Range:
  - mao:Occupation

## mao:hasOriginalLanguage
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has original language |

### Description
Range:
  - mao:Language

## mao:hasPart
### Annotations
Comment
  - A schematic relation between any entities, e.g. 'the human body has a brain as part', '20th century contains year 1923', 'World War II includes the Pearl Harbour event'. Subproperties and restrictions can be used to specialize hasPart for objects, events, etc.

Label

| Language | Label |
|----------|-------|
| English  | has part |

### Description
Domain:
  - owl:Thing

Range:
  - owl:Thing

## mao:hasPrequels
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has prequels |

### Description
Range:
  - mao:Film

## mao:hasProducer
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has producer |

## mao:hasReviewAggregator
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has review aggregator |

### Description
Range:
  - mao:Organization

## mao:hasRole
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has role |

## mao:hasSequels
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has sequels |

### Description
Range:
  - mao:Film

## mao:hasSetting
### Annotations
Comment
  - A relation between entities and situations, e.g. 'this morning I've prepared my coffee with a new fantastic Arabica', i.e.: (an amount of) a new fantastic Arabica hasSetting the preparation of my coffee this morning.

Label

| Language | Label |
|----------|-------|
| English  | has setting |

### Description
Domain:
  - owl:Thing

Range:
  - mao:Situation

## mao:hasSubGenre
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has sub-genre |

### Description
Range:
  - mao:Genre

## mao:hasSubTitleInLanguage
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has sub title in language |

### Description
Range:
  - mao:Language

## mao:hasParticipant
### Annotations
Comment
  - A relation between an object and a process, e.g. 'John took part in the discussion', 'a large mass of snow fell during the avalanche', or 'a cook, some sugar, flour, etc. are all present in the cooking of a cake'.

Label

| Language | Label |
|----------|-------|
| English  | has participant |

### Description
Domain:
  - mao:Event

Range:
  - mao:Object

## mao:hasVoiceActor
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has voice actor |

### Description
Range:
  - mao:Person

## mao:involvesAgent
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | involves agent |

### Description
Domain:
  - mao:Event

Range:
  - mao:Agent

Sub-properties:
  - mao:hasParticipant

## mao:isAffectedByValidityOf
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is affected by validity of |

### Description
Domain:
  - mao:Value

Range:
  - owl:Thing

## mao:isAgentInvolvedIn
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is agent involved in |

### Description
Domain:
  - mao:Agent

Range:
  - mao:Event

Sub-properties:
  - mao:isParticipantIn

## mao:isCriterionFor
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is criterion for |

### Description
Sub-properties:
  - mao:isValidFor

## mao:isGivenTo
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is given to |

### Description
Domain:
  - mao:NominationSituation

Range:
  - mao:Object

## mao:isOccupationOf
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is occupation of |

### Description
Range:
  - mao:Person

## mao:isPartOf
### Annotations
Comment
  - A relation between any entities, e.g.'brain is a part of the human body'.

Label

| Language | Label |
|----------|-------|
| English  | is part of |

### Description
Domain:
  - owl:Thing

Range:
  - owl:Thing

## mao:isParticipantIn
### Annotations
Comment
  - A relation between an object and a process, e.g. 'John took part in the discussion', 'a large mass of snow fell during the avalanche', or 'a cook, some sugar, flour, etc. are all present in the cooking of a cake'.

Label

| Language | Label |
|----------|-------|
| English  | is participant in |

### Description
Domain:
  - mao:Object

Range:
  - mao:Event

## mao:isRequirementFor
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is requirement for |

### Description
Range:
  - owl:Thing

Sub-properties:
  - mao:isValidFor

## mao:isSatisfiedBy
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is satisfied by |

### Description
Domain:
  - owl:Thing

Range:
  - mao:Value

## mao:isSettingFor
### Annotations
Comment
  - A relation between situations and entities, e.g. 'this morning I've prepared my coffee with a new fantastic Arabica', i.e.: the preparation of my coffee this morning is the setting for (an amount of) a new fantastic Arabica.

Label

| Language | Label |
|----------|-------|
| English  | is setting for |

### Description
Domain:
  - mao:Situation

Range:
  - owl:Thing

## mao:isSubGenreOf
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is sub-genre of |

### Description
Range:
  - mao:Genre

## mao:isValidFor
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | A value is always valid for some specific thing. This relation should point to an entity which is expected to satisfy a given value. Sometimes a temporal or spatial context needs to be provided, e.g. Non-EU students, 2011 graduates etc. Exceptions describing special conditions affecting the validity of a value can be described using the 'has exception' relation. |

Label

| Language | Label |
|----------|-------|
| English  | is valid for |

### Description
Domain:
  - mao:Value

Range:
  - owl:Thing

## mao:isViolatedBy
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is violated by |

### Description
Domain:
  - mao:Value

Range:
  - owl:Thing

## mao:locatedIn
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | located in |

### Description
Range:
  - mao:Place

## mao:presentedBy
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | presented by |

### Description
Range:
  - mao:Organization

## mao:reviewOf
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | review of |

### Description
Range:
  - mao:Object

## mao:satisfies
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | satisfies |

### Description
Domain:
  - owl:Thing

Range:
  - mao:Value

## mao:satisfiesCriterion
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | satisfies criterion |

### Description
Range:
  - mao:Criterion

Sub-properties:
  - mao:satisfies

## mao:satisfiesRequirement
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | satisfies requirement |

### Description
Range:
  - mao:Requirement

Sub-properties:
  - mao:satisfies

## mao:setBy
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | set by |

### Description
Range:
  - mao:Agent

## mao:violates
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | violates |

### Description
Domain:
  - owl:Thing

Range:
  - mao:Value

## mao:violatesCriterion
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | violates criterion |

### Description
Range:
  - mao:Criterion

Sub-properties:
  - mao:violates

## mao:violatesRequirement
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | violates requirement |

### Description
Range:
  - mao:Requirement

Sub-properties:
  - mao:violates

## mao:satisfiesCriterionFor
### Description
Domain:
  - mao:Film

Range:
  - mao:Award

## mao:violatesCriterionFor
### Description
Domain:
  - mao:Film

Range:
  - mao:Award


# Data Properties
## owl:topDataProperty
## mao:dateHeld
### Annotations
Comment
  - An attribute, quality, or characteristic of data

Label

| Language | Label |
|----------|-------|
| English  | date held |

### Description
Range:
  - xsd:date

## mao:dateReleased
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | date released |

### Description
Range:
  - xsd:dateTime

## mao:hasAggregateRating
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has aggregate rating |

### Description
Range:
  - xsd:decimal

## mao:hasContent
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has content |

### Description
Range:
  - xsd:string

## mao:hasCount
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has count |

### Description
Range:
  - xsd:integer

## mao:hasDescription
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has description |

### Description
Range:
  - xsd:string

## mao:hasEditionNumber
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has edition number |

### Description
Range:
  - xsd:integer

## mao:hasFeatureLengthInMinutes
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has feature length in minutes |

### Description
Range:
  - xsd:integer

## mao:hasInitialReleaseYear
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has initial release year |

### Description
Range:
  - xsd:integer

## mao:hasMaxValue
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has max value |

### Description
Range:
  - xsd:decimal

## mao:hasMinValue
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has min value |

### Description
Range:
  - xsd:decimal

## mao:hasName
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has name |

### Description
Range:
  - xsd:string

## mao:hasNickname
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has nickname |

### Description
Range:
  - xsd:string

## mao:hasTitle
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has title |

### Description
Range:
  - xsd:string

## mao:hasSource
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has source |

### Description
Range:
  - xsd:string

## mao:hasValue
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has value |

### Description
Range:
  - xsd:decimal

## mao:hasWikipediaLink
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | has Wikipedia link |

### Description
Range:
  - xsd:string

## mao:isAdult
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is adult |

### Description
Range:
  - xsd:boolean

## mao:isBritishFilm
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | is British film |

### Description
Range:
  - xsd:boolean

## mao:yearScreened
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | year screened |

### Description
Range:
  - xsd:integer

## mao:win
### Annotations
Label

| Language | Label |
|----------|-------|
| English  | win   |

### Description
Range:
  - xsd:boolean


# Annotation Properties
## dc:title
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | A name given to the resource |

## dcterms:license
### Annotations
Comment

| Language | Comment |
|----------|---------|
| English  | A legal document giving official permission to do something with the resource. |

Label

| Language | Label |
|----------|-------|
| English  | License |


# Rules
## filmEligible
```
mao:Film(?m) ^ mao:satisfiesCriterion(?m, ?c) ^ mao:isCriterionFor(?c, ?award) -> mao:eligibleFor(?m, ?award)
```
## satisfyFeatureLengthOscarCriterion
```
mao:Film(?m) ^ mao:hasFeatureLengthInMinutes(?m, ?t) ^ swrlb:greaterThanOrEqual(?t, 40) -> mao:satisfiesCriterion(?m, mao:FeatureLengthOscarCriterion)
```
## violateFeatureLengthOscarCriterion
```
mao:Film(?m) ^ mao:hasFeatureLengthInMinutes(?m, ?t) ^ swrlb:lessThan(?t, 40) -> mao:violatesCriterion(?m, mao:FeatureLengthOscarCriterion)
```
## satisfyShortFilmOscarCriterion
```
mao:Film(?m) ^ mao:hasFeatureLengthInMinutes(?m, ?t) ^ swrlb:lessThanOrEqual(?t, 40) -> mao:satisfiesCriterion(?m, mao:ShortFilmOscarCriterion)
```
## satisfyFeatureLengthBaftaCriterion
```
mao:Film(?m) ^ mao:hasFeatureLengthInMinutes(?m, ?t) ^ swrlb:greaterThanOrEqual(?t, 70) -> mao:satisfiesCriterion(?m, mao:FeatureLengthBaftaCriterion)
```
## hasEnglishSubTitle
```
mao:Film(?f) ^ mao:AwardReceivedSituation(?as) ^ mao:hasAward(?as, mao:Oscars) ^ mao:forFilm(?as, ?f) -> mao:hasSubTitleInLanguage(?f, mao:English)
```
## occupationForperson
```
NominationSituation(?ns) ^ hasAwardCategory(?ns, ?ac) ^ forOccupation(?ac, ?o) ^ isGivenTo(?ns, ?p) ^ -> hasOccupation(?p, ?o)
```
## mainCharacterOscarActor
```
mao:NominationSituation(?n) ^ mao:hasAwardCategory(?n, mao:OscarBestActor) ^ mao:isGivenTo(?n, ?p) ^ mao:forFilm(?n, ?m) ^ mao:FilmMakingSituation(?fm) ^ mao:hasFilm(?fm, ?m) ^ mao:hasPart(?fm, ?ac) ^ mao:hasActor(?ac, ?p) ^ mao:hasCharacter(?ac, ?char) -> mao:hasImportance(?char, mao:MainCharacter)
```
## mainCharacterOscarActress
```
mao:NominationSituation(?n) ^ mao:hasAwardCategory(?n, mao:OscarBestActress) ^ mao:isGivenTo(?n, ?p) ^ mao:forFilm(?n, ?m) ^ mao:FilmMakingSituation(?fm) ^ mao:hasFilm(?fm, ?m) ^ mao:hasPart(?fm, ?ac) ^ mao:hasActor(?ac, ?p) ^ mao:hasCharacter(?ac, ?char) -> mao:hasImportance(?char, mao:MainCharacter)
```
## sideCharacterOscarActor
```
mao:NominationSituation(?n) ^ mao:hasAwardCategory(?n, mao:OscarBestSupportingActor) ^ mao:isGivenTo(?n, ?p) ^ mao:forFilm(?n, ?m) ^ mao:FilmMakingSituation(?fm) ^ mao:hasFilm(?fm, ?m) ^ mao:hasPart(?fm, ?ac) ^ mao:hasActor(?ac, ?p) ^ mao:hasCharacter(?ac, ?char) -> mao:hasImportance(?char, mao:SideCharacter)
```
## sideCharacterOscarActress
```
mao:NominationSituation(?n) ^ mao:hasAwardCategory(?n, mao:OscarBestSupportingActress) ^ mao:isGivenTo(?n, ?p) ^ mao:forFilm(?n, ?m) ^ mao:FilmMakingSituation(?fm) ^ mao:hasFilm(?fm, ?m) ^ mao:hasPart(?fm, ?ac) ^ mao:hasActor(?ac, ?p) ^ mao:hasCharacter(?ac, ?char) -> mao:hasImportance(?char, mao:SideCharacter)
```
## satisfiesCriterionFor
```
mao:satisfiesCriterion(?film, ?c) ^ mao:isCriterionFor(?c, ?award) -> mao:satisfiesCriterionFor(?film, ?award)
```
## violatesCriterionFor
```
mao:violatesCriterion(?film, ?c) ^ mao:isCriterionFor(?c, ?award) -> mao:violatesCriterionFor(?film, ?award)
```
