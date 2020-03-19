import yaml
from service_metadata.model import ServiceMetadata


class ServiceMetadataReader:

    def read(self, file: str) -> ServiceMetadata:
        file_content = yaml.load(open(file))

        # TODO - validation and exceptions

        name = file_content['name']
        description = file_content['description']

        service_metadata = ServiceMetadata(
            name=name,
            description=description,
            parameters={} # TODO
        )

        return service_metadata
