import unittest
from service_metadata.reader import ServiceMetadataReader


class TestServiceMetadataReader(unittest.TestCase):

    reader: ServiceMetadataReader

    def setUp(self):
        self.reader = ServiceMetadataReader()

    def test_read_simple_metadata_without_parameters(self):
        service_metadata = self.reader.read("test/service_metadata/service_medata_no_parameters.yaml")

        self.assertEqual("service", service_metadata.name)
        self.assertEqual("service description", service_metadata.description)

# TODO - more tests