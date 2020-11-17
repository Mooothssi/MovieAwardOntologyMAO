from pathlib import Path
import os
from owlready2 import get_ontology
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


class OntogenClassExpressionTestCase(TestCase):
    def test_horse(self):
        cls = ClassExpToConstruct()
        construct = cls.class_expression_to_construct("(mao:Dog and mao:Croc) or mao:Cat or (mao:Person and mao:Film)")
        self.assertEqual("(mao.Dog & mao.Croc) | mao.Cat | (mao.Person & mao.Film)", str(construct))

        construct = cls.class_expression_to_construct("(not(Dog or Cat)) and (Horse)")
        self.assertEqual("Not(mao.Dog or Cat) & mao.Horse", str(construct))

        construct = cls.class_expression_to_construct("(Horse) and (not(Dog or Cat))")
        self.assertEqual("mao.Horse & Not(mao.Dog or Cat)", str(construct))

        construct = cls.class_expression_to_construct("(Cat) and (Dog)")
        self.assertEqual("mao.Cat & mao.Dog", str(construct))

        construct = cls.class_expression_to_construct("(Cat and Horse and Dog) and Chicken")
        self.assertEqual("mao.Cat & mao.Horse & mao.Dog & mao.Chicken", str(construct))

