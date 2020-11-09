from ..sources import ImdbDataSource, MapperDataSource


class Aggregator:
    sources: [MapperDataSource] = [ImdbDataSource]
    model = None

    def create_instances(self):
        pass

    def retrieve_instances_from(self, source: MapperDataSource):
        pass

