from pathlib import Path
import os
from owlready2 import get_ontology
from unittest import TestCase

from ontogen.converter import YamlToOwlConverter
from ontogen.primitives import OwlClass

from settings import OWL_FILEPATH, OUT_PATH, OUT_FILENAME


def count_files(directory: str) -> int:
    return len([name for name in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, name))])


class TestOntogen(TestCase):
    converter: YamlToOwlConverter

    def setUp(self):
        self.converter = YamlToOwlConverter("data/mao.yaml")
        self.onto = get_ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/proto-movie#")
        # self.onto = get_ontology(f"file:////{OWL_FILEPATH}")
        # self.onto.load()

    def test_assertion(self):
        self.test_instantiation()
        self.i.add_property_assertion("mao:hasTitle", "Parasite")
        self.assertEqual("Parasite", self.i.properties_values["mao:hasTitle"])

    def test_instantiation(self):
        self.i: OwlClass = self.converter.get_entity("mao:Film")
        self.i.instantiate(self.onto, "Parasite")
        self.i.add_label("Parasite^^rdfs:Literal@en")
        self.assertTrue(self.i.is_individual)
        self.assertEqual("proto-movie.Film", str(self.i._internal_imp_instance.is_instance_of[0]))

    # Create an OWL ontology from scratch
    def test_create_ontology(self):
        self.test_instantiation()
        self.i = self.converter.to_owl_ontology(self.onto)
        self.onto.save(file=str(Path(OUT_PATH) / OUT_FILENAME), format="rdfxml")

    def tearDown(self):
        pass
