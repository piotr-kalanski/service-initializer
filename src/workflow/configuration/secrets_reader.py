import os
from typing import List
import yaml


class SecretsReader:

    def read(self, environment_variables: dict, files: List[str]) -> dict:
        result = {}

        for file in files:
            result.update(yaml.load(open(file), Loader=yaml.FullLoader))

        for (environment_variable_name,secret_key) in environment_variables.items():
            result[secret_key] = os.environ[environment_variable_name]

        return result
