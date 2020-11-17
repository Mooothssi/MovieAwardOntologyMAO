from pathlib import Path
import os
from unittest import TestCase

from ontogen import Ontology
from ontogen.converter import YamlToOwlConverter
from ontogen.primitives import OwlClass
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
        self.i: OwlClass = self.converter.get_entity("mao:Film")
        # self.onto = Ontology.load_from_file(OWL_FILEPATH)

    def test_add_rule(self):
        self.test_realization()
        self.onto.add_rule("mao:ActingSituation(?p), mao:hasActor(?p, ?a), "
                           "hasLocation(?p, ?s), mao:Film(?s) -> portrays(?s, ?a)")

    def test_assertion(self):
        self.test_instantiation()
        self.i.add_property_assertion("mao:hasTitle", "Parasite")
        self.assertEqual("Parasite", self.i.properties_values["mao:hasTitle"])

    def test_instantiation(self):
        self.i.instantiate(self.onto, "Parasite")
        self.i.add_label("Parasite^^rdfs:Literal@en")
        self.assertTrue(self.i.is_individual)
        self.assertEqual("mao.Film", str(self.i._internal_imp_instance.is_instance_of[0]))

    def test_realization(self):
        self.converter.to_owl_ontology(self.onto)

    # Create an OWL ontology from scratch
    def test_create_ontology(self):
        self.test_instantiation()
        self.i = self.converter.to_owl_ontology(self.onto)
        self.onto.save_to_file(str(Path(OUT_PATH) / OUT_FILENAME), "rdfxml")

    def test_super_classes(self):
        film_making = self.converter.get_entity("mao:FilmMakingSituation")
        film_making.actualize(self.onto)
        event = self.converter.get_entity("mao:Event")
        event.actualize(self.onto)
        sit = self.converter.get_entity("mao:Situation")
        sit.actualize(self.onto)
        self.assertListEqual([event.realized_entity, sit.realized_entity], film_making.realized_entity.is_a)

    def tearDown(self):
        pass


FIXTURES = (
    ("(mao:Dog and mao:Croc) or mao:Cat or (mao:Person and mao:Film)",
     "(mao.Dog & mao.Croc) | mao.Cat | (mao.Person & mao.Film)"),
    ("(not(Dog or Cat)) and (Horse)",
     "Not(mao.Dog | mao.Cat) & mao.Horse"),
    ("(mao:Dog and not(mao:Croc or not(mao:Cat))) "
     "or mao:Cat or (mao:Person and mao:Film)",
     "(mao.Dog & Not(mao.Croc | Not(mao.Cat))) | mao.Cat | (mao.Person & mao.Film)"),
    ("(Horse) and (not(Dog or Cat))", "mao.Horse & Not(mao.Dog | mao.Cat)"),
    ("(Mo) and (Ding)", "mao.Mo & mao.Ding"),
    ("Mo or Ding or Bank", "mao.Mo | mao.Ding | mao.Bank"),
    ("(Cat and Horse and Dog) and Chicken", "mao.Cat & mao.Horse & mao.Dog & mao.Chicken"),
    ("(mao:Dog and (mao:Done or (mao:Film and mao:Croc))) or mao:Cat or (mao:Person and mao:Film)",
     "(mao.Dog & (mao.Done | (mao.Film & mao.Croc))) | mao.Cat | (mao.Person & mao.Film)")
)


class OntogenClassExpressionTestCase(TestCase):
    def setUp(self):
        self.onto = Ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#")
        self.onto.create()

    def test_basic(self):
        cls = ClassExpToConstruct(self.onto)
        for fixture in FIXTURES:
            exp, expected = fixture
            with self.subTest(exp=exp, expected=expected):
                construct = cls.to_construct(exp)
                self.assertEqual(expected, str(construct))
