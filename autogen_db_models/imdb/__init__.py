# import modules to run it through declarative base
from .name_basics import NameBasics
from .title_akas import TitleAkas
from .title_basics import TitleBasics
from .title_crew import TitleCrew
from .title_episode import TitleEpisode
from .title_principals import TitlePrincipals
from .title_ratings import TitleRatings
from .certificates import Certificates
from .countries import Countries
from .production_companies import ProductionCompanies

models = [NameBasics, TitleAkas, TitleAkas, TitleBasics, TitleBasics, TitleCrew, TitleEpisode, TitlePrincipals, TitleRatings, Certificates, Countries, ProductionCompanies]
