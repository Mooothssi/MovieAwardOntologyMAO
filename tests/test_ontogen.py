from pathlib import Path
import os
from unittest import TestCase

from ontogen import Ontology, OwlIndividual
from ontogen.converter import YamlToOwlConverter
from ontogen.primitives import OwlClass, OwlObjectProperty
from ontogen.primitives.datatypes import Datatype
from ontogen.utils import ClassExpToConstruct

from settings import OWL_FILEPATH, OUT_PATH, OUT_FILENAME


def count_files(directory: str) -> int:
    return len([name for name in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, name))])


class TestOntogen(TestCase):
    converter: YamlToOwlConverter

    def setUp(self):
        self.converter = YamlToOwlConverter("data/mao.yaml")
        self.onto = Ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#")
        self.onto.create()
        self.parasite_film = OwlIndividual("mao:Parasite")
        self.i: OwlClass = self.converter.get_entity("mao:Film")

    def test_add_rule(self):
        self.test_realization()
        self.onto.add_rule("mao:ActingSituation(?p) ^ mao:hasActor(?p, ?a) -> mao:actsIn(?a, ?p)", "ActsIn")

    def test_assertion(self):
        self.test_instantiation()
        self.parasite_film.add_property_assertion("mao:hasTitle", "Parasite")
        self.parasite_film.actualize(self.onto)
        self.assertEqual("Parasite", self.parasite_film.properties_values["mao:hasTitle"])

    def test_instantiation(self):
        film: OwlClass = OwlClass("mao:Film")

        self.parasite_film.be_type_of(film)
        self.parasite_film.add_label("Parasite^^rdfs:Literal@en")
        self.parasite_film.add_property_assertion("mao:hasTitle", "Parasite")
        self.parasite_film.actualize(self.onto)
        self.parasite_film._imp.hasTitle = ""

    def test_realization(self):
        self.converter.export_to_ontology(self.onto)

    # Create an OWL ontology from scratch
    def test_create_ontology(self):
        self.test_assertion()
        self.test_add_rule()
        self.i = self.converter.export_to_ontology(self.onto)
        self.onto.save_to_file(str(Path(OUT_PATH) / OUT_FILENAME))

    def test_super_classes(self):
        film_making = self.converter.get_entity("mao:FilmMakingSituation")
        film_making.actualize(self.onto)
        event = self.converter.get_entity("mao:Event")
        event.actualize(self.onto)
        sit = self.converter.get_entity("mao:Situation")
        sit.actualize(self.onto)
        self.assertListEqual([event.actualized_entity, sit.actualized_entity], film_making.actualized_entity.is_a)


class TestOntogenPizza(TestCase):
    def test_pizza_ontology(self):
        converter = YamlToOwlConverter("test_cases/test_case1.yaml", "pizza")
        onto = converter.export_to_ontology()
        d = Datatype("Pizza:str")
        d.data_type = str
        d.actualize(onto)
        onto.add_license("MIT License")
        print(onto.implementation.world._props)
        from owlready2.base import _universal_abbrev_2_iri, _universal_iri_2_abbrev
        # print(_universal_abbrev_2_iri)
        # print(_universal_iri_2_abbrev)

        # print(onto.implementation.metadata.search(label="*"))
        pizza = converter.get_entity("pizza:Pizza")
        self.assertTrue(converter.get_entity("pizza:NamedPizza").is_subclass_of(pizza))
        onto.save_to_file("out/pizza.owl")

    def test_movie_ontology(self):
        o = Ontology.load_from_file(OWL_FILEPATH)
        print(o.implementation.metadata.deprecated)


FIXTURES = (
    ("(Mo) and (Ding)", "mao.Mo & mao.Ding"),
    ("{Male, Female, NonBinary}", "OneOf([mao.Male, mao.Female, mao.NonBinary])"),
    ("Ding and (hasPet some (Cat or Dog))", "mao.Ding & mao.hasPet.some(mao.Cat | mao.Dog)"),
    ("Mai and (hasPet some Cat)", "mao.Mai & mao.hasPet.some(mao.Cat)"),
    ("Mai and (hasPet exactly 1 Cat)", "mao.Mai & mao.hasPet.exactly(1, mao.Cat)"),
    ("(Mai and (hasPet exactly 1 Cat)) or (hasPet min 1 Cat)",
     "(mao.Mai & mao.hasPet.exactly(1, mao.Cat)) | mao.hasPet.min(1, mao.Cat)"),
    ("Mo or Ding or Bank", "mao.Mo | mao.Ding | mao.Bank"),
    ("(mao:Mai and mao:Student) or mao:SPP",
     "(mao.Mai & mao.Student) | mao.SPP"),
    ("(not(Dog or Cat)) and (Horse)",
     "Not(mao.Dog | mao.Cat) & mao.Horse"),
    ("(mao:Dog and not(mao:Croc or not(mao:Cat))) "
     "or mao:Cat or (mao:Person and mao:Film)",
     "(mao.Dog & Not(mao.Croc | Not(mao.Cat))) | mao.Cat | (mao.Person & mao.Film)"),
    ("(Horse) and (not(Dog or Cat))", "mao.Horse & Not(mao.Dog | mao.Cat)"),
    ("(Cat and Horse and Dog) and Chicken", "mao.Cat & mao.Horse & mao.Dog & mao.Chicken"),
    ("(mao:Dog and (mao:Done or (mao:Film and mao:Croc))) or mao:Cat or (mao:Person and mao:Film)",
     "(mao.Dog & (mao.Done | (mao.Film & mao.Croc))) | mao.Cat | (mao.Person & mao.Film)")
)


class OntogenClassExpressionTestCase(TestCase):
    def setUp(self):
        self.onto = Ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#")
        self.onto.create()
        obj_prop = OwlObjectProperty("mao:hasPet")
        obj_prop.actualize(self.onto)

    def test_basic(self):
        c = OwlClass("mao:Gender")
        i = OwlIndividual("mao:Male")
        i.be_type_of(c)
        i.actualize(self.onto)
        i = OwlIndividual("mao:Female")
        i.be_type_of(c)
        i.actualize(self.onto)
        i = OwlIndividual("mao:NonBinary")
        i.be_type_of(c)
        i.actualize(self.onto)
        cls = ClassExpToConstruct(self.onto)
        for fixture in FIXTURES:
            exp, expected = fixture
            with self.subTest(exp=exp, expected=expected):
                construct = cls.to_construct(exp)
                self.assertEqual(expected, str(construct))
