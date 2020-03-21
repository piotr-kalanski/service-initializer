import unittest
import os
from workflow.configuration.secrets_reader import SecretsReader


class TestSecretsReader(unittest.TestCase):

    secrets_reader: SecretsReader

    def setUp(self):
        self.secrets_reader = SecretsReader()

    def test_read_secrets_from_single_file(self):
        secrets = self.secrets_reader.read(
            environment_variables={},
            files=[
                "test/secrets/secrets.yaml"
            ]
        )

        self.assertEqual("value1", secrets["secret_key1"])
        self.assertEqual("value2", secrets["secret_key2"])

    def test_read_secrets_from_multiple_files(self):
        secrets = self.secrets_reader.read(
            environment_variables={},
            files=[
                "test/secrets/secrets.yaml",
                "test/secrets/secrets2.yaml"
            ]
        )

        self.assertEqual("value1", secrets["secret_key1"])
        self.assertEqual("value2", secrets["secret_key2"])
        self.assertEqual("value3", secrets["secret_key3"])
        self.assertEqual("value4", secrets["secret_key4"])

    def test_read_secrets_from_environment_variables(self):
        os.environ['ENV_VARIABLE'] = 'SECRET_VALUE'
        secrets = self.secrets_reader.read(
            environment_variables={
                'ENV_VARIABLE': 'SECRET_KEY'
            },
            files=[]
        )

        self.assertEqual("SECRET_VALUE", secrets["SECRET_KEY"])

    def test_read_secrets_from_environment_and_file(self):
        os.environ['ENV_VARIABLE'] = 'SECRET_VALUE'
        secrets = self.secrets_reader.read(
            environment_variables={
                'ENV_VARIABLE': 'SECRET_KEY'
            },
            files=[
                "test/secrets/secrets.yaml"
            ]
        )

        self.assertEqual("SECRET_VALUE", secrets["SECRET_KEY"])
        self.assertEqual("value1", secrets["secret_key1"])
        self.assertEqual("value2", secrets["secret_key2"])

    def test_read_secrets_from_environment_and_file_With_conflict(self):
        os.environ['ENV_VARIABLE'] = 'SECRET_VALUE'
        secrets = self.secrets_reader.read(
            environment_variables={
                'ENV_VARIABLE': 'secret_key1'
            },
            files=[
                "test/secrets/secrets.yaml"
            ]
        )

        self.assertEqual("SECRET_VALUE", secrets["secret_key1"])
        self.assertEqual("value2", secrets["secret_key2"])
        