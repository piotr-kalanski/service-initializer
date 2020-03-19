import yaml
from service_metadata.model import ServiceMetadata
from service_metadata.exceptions import MissingServiceNameException


class ServiceMetadataReader:

    def read(self, file: str) -> ServiceMetadata:
        file_content = yaml.load(open(file))

        if not file_content or 'name' not in file_content:
            raise MissingServiceNameException()

        name = file_content['name']
        description = file_content['description'] if 'description' in file_content else name
        parameters = file_content['parameters'] if 'parameters' in file_content else {}

        service_metadata = ServiceMetadata(
            name=name,
            description=description,
            parameters=parameters
        )

        return service_metadata
