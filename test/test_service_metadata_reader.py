import unittest
import pytest
from service_metadata.reader import ServiceMetadataReader
from service_metadata.exceptions import MissingServiceNameException


class TestServiceMetadataReader(unittest.TestCase):

    reader: ServiceMetadataReader

    def setUp(self):
        self.reader = ServiceMetadataReader()

    def test_read_simple_metadata_without_parameters(self):
        service_metadata = self.reader.read("test/service_metadata/service_metadata_no_parameters.yaml")

        self.assertEqual("service", service_metadata.name)
        self.assertEqual("service description", service_metadata.description)

    def test_read_metadata_with_parameters(self):
        service_metadata = self.reader.read("test/service_metadata/service_metadata_with_parameters.yaml")

        self.assertEqual("service", service_metadata.name)
        self.assertEqual("service description", service_metadata.description)
        self.assertEqual({
            "param1": "value1",
            "param2": "value2",
            "param3": {
                "field1": 1,
                "field2": "f2"
            }
        }, service_metadata.parameters)

    def test_read_metadata_with_missing_name(self):
        with pytest.raises(MissingServiceNameException):
            self.reader.read("test/service_metadata/service_metadata_with_missing_name.yaml")

    def test_read_empty_metadata(self):
        with pytest.raises(MissingServiceNameException):
            self.reader.read("test/service_metadata/service_metadata_empty.yaml")

    def test_read_metadata_with_missing_description(self):           
        service_metadata = self.reader.read("test/service_metadata/service_metadata_with_missing_description.yaml")

        self.assertEqual("service", service_metadata.name)
        self.assertEqual("service", service_metadata.description)
